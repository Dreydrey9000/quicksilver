# QuickSilver ⚡

**Find out what's slowing down your app. Build the fix. Show how much faster it runs.**

QuickSilver is a drop-in agent that runs on a schedule (or on demand) and does one loop, every time:

1. **Measure** — times your app's most-hit endpoints or pages, before anything changes
2. **Diagnose** — finds the single biggest bottleneck (slow query, N+1, missing cache, bloated bundle, blocking call)
3. **Fix** — builds the smallest safe fix, never touches prod without your approval
4. **Prove** — re-measures the exact same targets and hands you a before/after table

```
endpoint              before    after     delta
/api/members          840ms     120ms     -86%
GET / (LCP)           3.1s      1.2s      -61%
/api/seats            210ms      95ms     -55%
```

## Why

Most performance work dies in the "we should look into that" phase. QuickSilver removes the decision: it shows up every week with one measurement, one bottleneck, one fix, and proof it worked. You just say yes.

## How it works

- Runs as a scheduled agent (cron) or a one-shot CLI in your CI
- Ships as a plain prompt + script kit, so it works with any agent runtime that can run shell commands (Hermes Agent, Claude Code, Codex CLI, plain bash)
- Safe by default: read-only diagnostics everywhere; fixes are proposed as diffs and applied only on explicit approval; production deploys always require a human yes

## Setup

Requirements: bash, curl, python3, and (optionally) a schedule runner.

1. Point it at your app: copy `config.example.json` to `config.json` and list your targets:

```json
{
  "app_name": "my-app",
  "targets": [
    "https://myapp.com/",
    "https://myapp.com/api/members",
    "https://myapp.com/api/orders"
  ],
  "n": 5,
  "repo_root": "/path/to/app"
}
```

2. Run a pass:

```bash
./quicksilver.sh            # full pass: measure -> diagnose -> propose fix
./quicksilver.sh --measure  # measurement only (read-only, safe anywhere)
```

3. Schedule it (example: Fridays 9am):

```
0 9 * * 5 /path/to/quicksilver.sh --report
```

## What's in the box

- `quicksilver.sh` — the pass runner (measure / diagnose / fix-propose / report)
- `lib/measure.py` — curl-based timing, percentiles, stable before/after comparison
- `prompts/agent.md` — the agent system prompt (works with any agent runtime)
- `config.example.json` — target list format

## Limitations (honest)

- v1 targets HTTP endpoints and page loads; DB-level profiling lands by looking at your app's own slow-query log
- It proposes one fix per pass on purpose. Whack-a-mole is what this exists to prevent.
- Authenticated routes need a token in config (never committed)

## License

MIT. Use it, ship it, sell the result.
