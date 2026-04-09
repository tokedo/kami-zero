# Alerts

### 2026-04-09 ~17:24 UTC — Kamibots platform-wide infra reset (ACTIVE)
Reported by human operator via ad-hoc session trigger. Kamibots team performed a
platform-wide reset that removed all running strategies across accounts. Our
`auto_v2` strategy `b4e3430a-391f-4175-b9bd-854d97db1770` (20 kamis, node 47) is
likely gone. On-chain harvest state should be unaffected — this is an off-chain
container reset only. Action: verify and relaunch the strategy this session.

## Resolved

### 2026-04-09 14:17 UTC — Kamibots strategy containers broken (RESOLVED session 2)
Supabase key error. Fixed server-side by Kami team. auto_v2 working as of 2026-04-09 17:14 UTC.
