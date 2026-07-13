// ============================================================================
// grade-readiness — Supabase Edge Function (Deno)
// ----------------------------------------------------------------------------
// The ONLY writer to public.readiness_attempts. Flow:
//   1. Verify the caller's Supabase JWT (GitHub-OAuth session) -> student id/email.
//   2. Read the submitted { check_id, lesson_day, question_ids, chosen }.
//   3. Grade SERVER-SIDE against public.question_keys (clients can't read it).
//   4. Insert one immutable attempt row (service role).
//   5. Return { score, total, per_question_correct, explanations }.
//
// Because grading + insert happen here with the service-role key, a student
// cannot forge a score, replay a fake attempt, or delete history.
// ============================================================================
import { createClient } from "jsr:@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "content-type": "application/json" },
  });
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);

  const authHeader = req.headers.get("Authorization") ?? "";
  if (!authHeader.startsWith("Bearer ")) return json({ error: "unauthenticated" }, 401);
  const token = authHeader.slice("Bearer ".length);

  // Service-role client: validates the caller's JWT, reads keys, and writes the
  // attempt (bypasses RLS). Only needs SUPABASE_URL + SERVICE_ROLE_KEY (auto-injected).
  const admin = createClient(SUPABASE_URL, SERVICE_ROLE);
  const { data: userData, error: userErr } = await admin.auth.getUser(token);
  if (userErr || !userData?.user) return json({ error: "invalid session" }, 401);
  const user = userData.user;

  let payload: {
    check_id?: string;
    lesson_day?: string;
    question_ids?: number[];
    chosen?: number[];
    client_meta?: Record<string, unknown>;
  };
  try {
    payload = await req.json();
  } catch {
    return json({ error: "bad json" }, 400);
  }

  const { check_id, lesson_day, question_ids, chosen, client_meta } = payload;
  if (
    typeof check_id !== "string" ||
    !Array.isArray(question_ids) || !Array.isArray(chosen) ||
    question_ids.length === 0 || question_ids.length !== chosen.length
  ) {
    return json({ error: "malformed submission" }, 400);
  }

  const { data: keys, error: keyErr } = await admin
    .from("question_keys")
    .select("question_id, correct_index, explain")
    .eq("check_id", check_id)
    .in("question_id", question_ids);
  if (keyErr) return json({ error: "key lookup failed" }, 500);
  if (!keys || keys.length === 0) return json({ error: "unknown check_id" }, 404);

  const keyBy = new Map<number, { correct_index: number; explain: string | null }>();
  for (const k of keys) keyBy.set(k.question_id, k);

  const per_question_correct: boolean[] = [];
  const explanations: string[] = [];
  const correct_indices: number[] = [];
  let score = 0;
  for (let i = 0; i < question_ids.length; i++) {
    const k = keyBy.get(question_ids[i]);
    if (!k) return json({ error: `no key for question ${question_ids[i]}` }, 400);
    const ok = chosen[i] === k.correct_index;
    per_question_correct.push(ok);
    correct_indices.push(k.correct_index);
    explanations.push(k.explain ?? "");
    if (ok) score++;
  }
  const total = question_ids.length;

  const { error: insErr } = await admin.from("readiness_attempts").insert({
    student_id: user.id,
    student_email: user.email,
    check_id,
    lesson_day: lesson_day ?? null,
    question_ids,
    chosen,
    per_question_correct,
    score,
    total,
    client_meta: client_meta ?? null,
  });
  if (insErr) return json({ error: "could not persist attempt" }, 500);

  // Return grading result (incl. correct indices + explanations) so the widget
  // can reveal feedback. The stored record is what instructors see.
  return json({ score, total, per_question_correct, correct_indices, explanations });
});
