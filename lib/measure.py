#!/usr/bin/env python3
"""QuickSilver measure: time N GETs per target, p50/p95, stable JSON output."""
import json, subprocess, sys, time, statistics, pathlib, datetime

cfg = json.load(open(sys.argv[1]))
label = "before"
if "--label" in sys.argv:
    label = sys.argv[sys.argv.index("--label") + 1]

results = []
for t in cfg["targets"]:
    times = []
    for _ in range(cfg.get("n", 5)):
        t0 = time.perf_counter()
        cmd = ["curl", "-s", "-o", "/dev/null", "-m", "30"]
        if cfg.get("auth_header"):
            cmd += ["-H", cfg["auth_header"]]
        cmd.append(t)
        subprocess.run(cmd, check=False)
        times.append((time.perf_counter() - t0) * 1000)
    results.append({
        "target": t,
        "n": len(times),
        "p50_ms": round(statistics.median(times), 1),
        "p95_ms": round(statistics.quantiles(times, n=20)[18], 1) if len(times) >= 4 else round(max(times), 1),
        "mean_ms": round(statistics.mean(times), 1),
    })

outdir = pathlib.Path(cfg.get("report_out", "reports")); outdir.mkdir(exist_ok=True)
run_id = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
payload = {"run_id": run_id, "label": label, "app": cfg["app_name"], "results": results}
(outdir / f"{run_id}-{label}.json").write_text(json.dumps(payload, indent=2))
print(json.dumps(payload, indent=2))
