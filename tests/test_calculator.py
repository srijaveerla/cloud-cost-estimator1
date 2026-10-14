import pytest

from estimator.calculator import Workload, compare, estimate, pick_instance, load_pricing


def test_pick_instance_chooses_cheapest_fit():
    inst = load_pricing()["providers"]["AWS"]["instances"]
    assert pick_instance(inst, 2, 8)["name"] == "m5.large"


def test_pick_instance_raises_when_nothing_fits():
    inst = load_pricing()["providers"]["AWS"]["instances"]
    with pytest.raises(ValueError):
        pick_instance(inst, 64, 512)


def test_reserved_is_cheaper_than_on_demand():
    w = Workload()
    assert estimate("AWS", w, "reserved_3y")["monthly"] < estimate("AWS", w, "on_demand")["monthly"]


def test_compare_is_sorted_ascending():
    totals = [r["monthly"] for r in compare(Workload())]
    assert totals == sorted(totals)


def test_zero_usage_costs_nothing_but_compute():
    w = Workload(block_storage_gb=0, object_storage_gb=0, db_storage_gb=0, egress_gb=0)
    r = estimate("GCP", w)
    assert r["monthly"] == r["items"]["Compute"]
