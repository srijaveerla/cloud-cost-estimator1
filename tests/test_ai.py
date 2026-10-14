import pandas as pd

from estimator.ai import detect_anomalies, forecast_costs
from estimator.data_gen import ANOMALY_DATES, make_billing_history, make_resource_inventory
from estimator.optimizer import recommend


def test_forecast_shape_and_band():
    fc = forecast_costs(make_billing_history(), days=30)
    assert len(fc) == 30
    assert (fc["lower"] < fc["forecast"]).all() and (fc["forecast"] < fc["upper"]).all()


def test_forecast_follows_upward_trend():
    hist = make_billing_history()
    fc = forecast_costs(hist, days=30)
    assert fc["forecast"].mean() > hist["cost"].head(30).mean()


def test_detects_injected_anomalies():
    found = set(detect_anomalies(make_billing_history())["date"].dt.strftime("%Y-%m-%d"))
    assert len(found & set(ANOMALY_DATES)) >= 2


def test_sale_days_are_not_flagged():
    flagged = detect_anomalies(make_billing_history())
    assert flagged["sale_flag"].sum() == 0


def test_recommendations_cover_idle_and_nonprod():
    recs = recommend(make_resource_inventory())
    assert "Terminate (idle)" in set(recs["action"])
    assert "Schedule off-hours" in set(recs["action"])
    assert recs["est_monthly_saving"].is_monotonic_decreasing
