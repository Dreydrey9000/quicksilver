#!/usr/bin/env python3
"""QuickSilver compare: pair the latest before/after runs into one table."""
import json, pathlib, sys

rep = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "reports")
files = sorted(rep.glob("*.json"))
befores = [f for f in files if "before" in f.name]
afters = [f for f in files if "after" in f.name]
if not befores or not afters:
    sys.exit("need at least one before and one after report")
b = json.loads(befores[-1].read_text()); a = json.loads(afters[-1].read_text())
bm = {r["target"]: r for r in b["results"]}; am = {r["target"]: r for r in a["results"]}
print(f"{'target':38} {'before':>9} {'after':>9} {'delta':>8}")
for t, br in bm.items():
    if t in am:
        d = 100 * (am[t]["p50_ms"] - br["p50_ms"]) / br["p50_ms"]
        print(f"{t[:38]:38} {br['p50_ms']:>7.0f}ms {am[t]['p50_ms']:>7.0f}ms {d:>7.0f}%")
