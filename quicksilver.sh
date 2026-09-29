#!/usr/bin/env bash
# QuickSilver - one performance pass: measure -> diagnose -> propose fix -> prove
# Safe by default: --measure is read-only; fixes are diffs until you approve.
set -euo pipefail
cd "$(dirname "$0")"

MODE="${1:-full}"
CONFIG="${QUICKSILVER_CONFIG:-config.json}"

[ -f "$CONFIG" ] || { echo "no config.json (copy config.example.json)"; exit 1; }

measure() {
  python3 lib/measure.py "$CONFIG" --label "$1"
}

case "$MODE" in
  --measure)
    measure before
    ;;
  full|--full)
    measure before
    # diagnosis + fix proposal are agent work: feed prompts/agent.md + the
    # before.json report to any agent runtime (Hermes, Claude Code, Codex).
    # The agent MUST re-run `./quicksilver.sh --after <run_id>` after applying
    # its fix to produce the before/after table.
    echo "before/ before.json written. Run an agent with prompts/agent.md to diagnose + fix."
    ;;
  --after)
    measure after
    python3 lib/compare.py reports/ --latest
    ;;
  --report)
    measure before
    echo "report written to reports/"
    ;;
  *) echo "usage: quicksilver.sh [--measure|full|--after|--report]"; exit 2;;
esac
