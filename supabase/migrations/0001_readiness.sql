-- ============================================================================
-- Readiness-check persistence — append-only, tamper-proof, instructor-visible
-- ============================================================================
-- Design (score integrity):
--   * Students NEVER write to these tables directly. The `grade-readiness` Edge
--     Function (service role) is the ONLY writer. It grades server-side against
--     `question_keys` (which clients can never read) and inserts one immutable
--     row per attempt.
--   * RLS lets a student SELECT only their own attempts; instructors SELECT all.
--   * There is NO UPDATE or DELETE policy for anon/authenticated roles, so a
--     student cannot alter or erase their history — satisfying requirement 5.
-- ============================================================================

create extension if not exists "pgcrypto";

-- ── Instructors -------------------------------------------------------------
-- A user is an instructor iff their auth uid is listed here. Seed manually
-- (see supabase/README.md) or via the Supabase dashboard.
create table if not exists public.instructors (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  email      text,
  added_at   timestamptz not null default now()
);

create or replace function public.is_instructor(uid uuid)
returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.instructors where user_id = uid);
$$;

-- ── Answer keys (server-only) ----------------------------------------------
-- Populated by scripts/build_readiness_keys.py from the lesson pools.
-- RLS is enabled with NO policies, so clients (anon/authenticated) get zero
-- rows. Only the service-role Edge Function can read it.
create table if not exists public.question_keys (
  check_id       text    not null,   -- e.g. 'week-04-m3-readiness'
  question_id    int     not null,   -- 0-based index into the authored pool
  correct_index  int     not null,   -- 0-based index of the correct option
  explain        text,
  primary key (check_id, question_id)
);
alter table public.question_keys enable row level security;
-- (intentionally no policies → no client access)

-- ── Attempts (append-only) --------------------------------------------------
create table if not exists public.readiness_attempts (
  id                    uuid primary key default gen_random_uuid(),
  student_id            uuid not null references auth.users (id) on delete cascade,
  student_email         text,
  check_id              text not null,
  lesson_day            text,
  question_ids          int[]  not null,   -- pool indices drawn this attempt
  chosen                int[]  not null,   -- option index the student picked
  per_question_correct  boolean[] not null,
  score                 int  not null,
  total                 int  not null,
  attempted_at          timestamptz not null default now(),
  client_meta           jsonb
);

create index if not exists readiness_attempts_student_time_idx
  on public.readiness_attempts (student_id, attempted_at desc);
create index if not exists readiness_attempts_check_idx
  on public.readiness_attempts (check_id);

alter table public.readiness_attempts enable row level security;

-- Students may READ their own attempts.
create policy "own attempts readable"
  on public.readiness_attempts for select
  to authenticated
  using (student_id = auth.uid());

-- Instructors may READ every attempt.
create policy "instructors read all attempts"
  on public.readiness_attempts for select
  to authenticated
  using (public.is_instructor(auth.uid()));

-- NOTE: deliberately NO insert/update/delete policies for authenticated/anon.
-- Writes happen exclusively through the service-role Edge Function, which
-- bypasses RLS. This makes the history append-only and student-tamper-proof.

-- ── Instructor rollup view --------------------------------------------------
-- Per-student, per-check progress: attempts, best/last score, trend.
create or replace view public.readiness_progress as
  select
    student_id,
    max(student_email)                          as student_email,
    check_id,
    count(*)                                    as attempts,
    max(score::numeric / nullif(total,0))       as best_ratio,
    (array_agg(score::numeric / nullif(total,0)
       order by attempted_at desc))[1]          as last_ratio,
    min(attempted_at)                           as first_attempt,
    max(attempted_at)                           as last_attempt
  from public.readiness_attempts
  group by student_id, check_id;
