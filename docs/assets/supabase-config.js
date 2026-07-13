/* Public Supabase config for readiness-check persistence.
   The publishable ("anon") key is DESIGNED to be exposed in client code — it only
   permits what Row-Level Security allows (students read their own attempts; all
   writes go through the server-side grade-readiness function). Safe to commit.
   Do NOT put the service-role key or DB connection string here. */
window.OX_SUPABASE = {
  url: "https://vzlbdkwswfosiszeyypl.supabase.co",
  key: "sb_publishable_poEAtdEbogTdTZjzhqh0DQ_XAembje9",
  functionUrl: "https://vzlbdkwswfosiszeyypl.supabase.co/functions/v1/grade-readiness"
};
