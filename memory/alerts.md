# Alerts

## 2026-04-09 14:17 UTC — Kamibots strategy containers broken

**Symptom**: All strategy types (harvestAndRest, auto_v2) crash immediately after container creation with:
```
Error: supabaseKey is required.
    at new SupabaseClient (/app/node_modules/@supabase/supabase-js/dist/main/SupabaseClient.js:45:19)
    at createClient (/app/node_modules/@supabase/supabase-js/dist/main/index.js:38:12)
    at file:///app/dist/src/services/supabaseClient.js:3:18
```

**Impact**: Cannot run any Kamibots strategies. All 20 kamis idle.
**Cause**: Server-side Supabase configuration issue in Kamibots container images. Not fixable by agent.
**Action taken**: Cleaned up all dead strategy containers. Scheduled short retry interval (2h).
**Workaround**: If persistent, implement direct on-chain harvest start/stop in executor.
