"""Rule-based optimisation advisor that turns a resource inventory into savings actions."""
from __future__ import annotations

import pandas as pd

OFF_HOURS_SAVING = 0.65     # fraction saved by shutting non-prod down nights/weekends
DOWNSIZE_SAVING = 0.50      # moving to an instance half the size


def recommend(resources: pd.DataFrame) -> pd.DataFrame:
    recs = []
    for r in resources.itertuples():
        if r.avg_cpu_pct < 3:
            recs.append((r.name, "Terminate (idle)", r.monthly_cost, "CPU below 3%"))
        elif r.env in ("dev", "test") and r.uptime_pct > 90:
            recs.append((r.name, "Schedule off-hours", r.monthly_cost * OFF_HOURS_SAVING,
                         "Non-prod running 24x7"))
        elif r.avg_cpu_pct < 20 and r.vcpu >= 4:
            recs.append((r.name, "Right-size (downsize)", r.monthly_cost * DOWNSIZE_SAVING,
                         f"Average CPU only {r.avg_cpu_pct}%"))
    out = pd.DataFrame(recs, columns=["resource", "action", "est_monthly_saving", "reason"])
    out["est_monthly_saving"] = out["est_monthly_saving"].round(2)
    return out.sort_values("est_monthly_saving", ascending=False).reset_index(drop=True)
