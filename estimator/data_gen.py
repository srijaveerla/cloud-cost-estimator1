"""Generate synthetic billing history and a resource inventory for the ShopNest scenario.

Run:  python -m estimator.data_gen
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Days where a runaway resource (misconfiguration) is injected, used to test detection.
ANOMALY_DATES = ["2026-02-11", "2026-05-19", "2026-08-03"]
SALE_WINDOWS = [("2025-10-15", "2025-10-25"), ("2026-01-24", "2026-01-27"), ("2026-06-10", "2026-06-14")]


def make_billing_history(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2025-10-01", "2026-09-30", freq="D")
    t = np.arange(len(dates))
    cost = 150 + 0.15 * t                                  # steady growth
    cost = cost + np.where(dates.dayofweek >= 5, 12, 0)    # busier weekends
    sale = np.zeros(len(dates), dtype=int)
    for start, end in SALE_WINDOWS:
        sale[(dates >= start) & (dates <= end)] = 1
    cost = cost + sale * 70                                # sale-season traffic spikes
    cost = cost + rng.normal(0, 4, len(dates))             # noise
    for d in ANOMALY_DATES:
        cost[dates == pd.Timestamp(d)] += rng.uniform(150, 220)
    return pd.DataFrame({"date": dates, "cost": cost.round(2), "sale_flag": sale})


def make_resource_inventory() -> pd.DataFrame:
    rows = [
        ("web-prod-1", "vm", "prod", 4, 62, 96.0, 100),
        ("web-prod-2", "vm", "prod", 4, 58, 96.0, 100),
        ("api-prod", "vm", "prod", 8, 14, 190.0, 100),
        ("worker-batch", "vm", "prod", 4, 9, 96.0, 100),
        ("web-dev", "vm", "dev", 2, 7, 48.0, 100),
        ("api-test", "vm", "test", 4, 11, 96.0, 100),
        ("old-demo-vm", "vm", "dev", 2, 1, 48.0, 100),
        ("cache-prod", "vm", "prod", 4, 71, 96.0, 100),
    ]
    return pd.DataFrame(rows, columns=[
        "name", "type", "env", "vcpu", "avg_cpu_pct", "monthly_cost", "uptime_pct"])


if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    make_billing_history().to_csv(DATA_DIR / "billing_history.csv", index=False)
    make_resource_inventory().to_csv(DATA_DIR / "resources.csv", index=False)
    print("Wrote data/billing_history.csv and data/resources.csv")
