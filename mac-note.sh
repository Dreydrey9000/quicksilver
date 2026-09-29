#!/bin/bash
# append QuickSilver note to agent instruction files on this Mac
NOTE='
## QuickSilver (performance agent, added 2026-09-29)
QuickSilver is the org performance department: it measures an app most-hit endpoints, finds the single biggest bottleneck, builds the smallest safe fix, and proves it with a before/after table. One bottleneck per run, no whack-a-mole. Never deploy to prod without Drey yes. Never claim a speedup that was not measured.
- OpenBot agent and channel: quicksilver (permitted in all department channels)
- Open-source kit: ~/workspace/quicksilver on the VPS (repo Dreydrey9000/quicksilver once pushed)
- Public page: https://jax.dreytools.com/quicksilver/
- If Drey asks for app-speed work, follow the QuickSilver loop and its hard rules.
'
for f in ~/.claude/CLAUDE.md ~/CLAUDE.md ~/.codex/AGENTS.md ~/AGENTS.md; do
  if [ -f "$f" ] && ! grep -q "QuickSilver" "$f"; then
    printf '%s\n' "$NOTE" >> "$f"
    echo "appended: $f"
  else
    echo "skipped: $f"
  fi
done
