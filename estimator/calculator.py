"""Core cost-estimation logic: pure functions, no UI, easy to test."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

HOURS_PER_MONTH = 730
PRICING_FILE = Path(__file__).resolve().parent.parent / "data" / "pricing.json"


@dataclass
class Workload:
    """Description of the application to be hosted in the cloud."""
    vm_count: int = 2
    vcpu_per_vm: int = 2
    ram_gb_per_vm: int = 8
    hours_per_month: int = HOURS_PER_MONTH
    block_storage_gb: int = 200
    object_storage_gb: int = 500
    db_storage_gb: int = 100
    egress_gb: int = 300


def load_pricing(path: Path = PRICING_FILE) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def pick_instance(instances: list[dict], vcpu: int, ram_gb: int) -> dict:
    """Return the cheapest instance that satisfies the vCPU and RAM need."""
    fits = [i for i in instances if i["vcpu"] >= vcpu and i["ram_gb"] >= ram_gb]
    if not fits:
        raise ValueError(f"No instance offers {vcpu} vCPU / {ram_gb} GB RAM")
    return min(fits, key=lambda i: i["hourly"])


def estimate(provider: str, w: Workload, model: str = "on_demand",
             pricing: dict | None = None) -> dict:
    """Monthly cost breakdown for one provider and one pricing model."""
    pricing = pricing or load_pricing()
    p = pricing["providers"][provider]
    discount = pricing["reserved_discount"][model]

    inst = pick_instance(p["instances"], w.vcpu_per_vm, w.ram_gb_per_vm)
    compute = inst["hourly"] * w.hours_per_month * w.vm_count * (1 - discount)

    items = {
        "Compute": round(compute, 2),
        "Block storage": round(w.block_storage_gb * p["block_gb_month"], 2),
        "Object storage": round(w.object_storage_gb * p["object_gb_month"], 2),
        "Database storage": round(w.db_storage_gb * p["db_gb_month"], 2),
        "Data transfer out": round(w.egress_gb * p["egress_gb"], 2),
    }
    monthly = round(sum(items.values()), 2)
    return {
        "provider": provider,
        "model": model,
        "instance": inst["name"],
        "items": items,
        "monthly": monthly,
        "annual": round(monthly * 12, 2),
    }


def compare(w: Workload, model: str = "on_demand") -> list[dict]:
    """Estimate every provider and sort from cheapest to most expensive."""
    pricing = load_pricing()
    results = [estimate(name, w, model, pricing) for name in pricing["providers"]]
    return sorted(results, key=lambda r: r["monthly"])


def savings_vs_on_demand(provider: str, w: Workload) -> dict[str, float]:
    """Monthly saving of each pricing model compared with on-demand."""
    pricing = load_pricing()
    base = estimate(provider, w, "on_demand", pricing)["monthly"]
    return {
        m: round(base - estimate(provider, w, m, pricing)["monthly"], 2)
        for m in pricing["reserved_discount"]
    }
