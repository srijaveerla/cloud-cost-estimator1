"""Streamlit dashboard: Cloud Cost Estimator with AI forecasting for the ShopNest scenario."""
import json
from pathlib import Path

import pandas as pd
import streamlit as st

from estimator.ai import detect_anomalies, forecast_costs
from estimator.calculator import Workload, compare, savings_vs_on_demand
from estimator.optimizer import recommend

DATA = Path(__file__).parent / "data"
st.set_page_config(page_title="Cloud Cost Estimator", page_icon="☁️", layout="wide")
st.title("☁️ Cloud Cost Estimator + AI Forecasting")
st.caption("Scenario: ShopNest, an online store moving to the cloud. Sample data for learning purposes.")

scenario = json.loads((DATA / "scenario.json").read_text())["workload"]
tab1, tab2, tab3 = st.tabs(["1. Cost estimate", "2. AI forecast & anomalies", "3. Savings advisor"])

# ---------- Tab 1: estimator ----------
with tab1:
    with st.sidebar:
        st.header("Workload")
        w = Workload(
            vm_count=st.number_input("Number of VMs", 1, 100, scenario["vm_count"]),
            vcpu_per_vm=st.selectbox("vCPU per VM", [2, 4, 8], index=[2, 4, 8].index(scenario["vcpu_per_vm"])),
            ram_gb_per_vm=st.selectbox("RAM per VM (GB)", [4, 8, 16, 32], index=[4, 8, 16, 32].index(scenario["ram_gb_per_vm"])),
            hours_per_month=st.slider("Running hours / month", 100, 730, scenario["hours_per_month"]),
            block_storage_gb=st.number_input("Block storage (GB)", 0, 100000, scenario["block_storage_gb"]),
            object_storage_gb=st.number_input("Object storage (GB)", 0, 100000, scenario["object_storage_gb"]),
            db_storage_gb=st.number_input("Database storage (GB)", 0, 100000, scenario["db_storage_gb"]),
            egress_gb=st.number_input("Data transfer out (GB/month)", 0, 100000, scenario["egress_gb"]),
        )
        model = st.selectbox("Pricing model", ["on_demand", "reserved_1y", "reserved_3y", "spot"])
    results = compare(w, model)
    best = results[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Cheapest provider", best["provider"])
    c2.metric("Monthly estimate", f"${best['monthly']:,.2f}")
    c3.metric("Annual estimate", f"${best['annual']:,.2f}")
    table = pd.DataFrame([{"Provider": r["provider"], "Instance": r["instance"], **r["items"],
                           "Monthly total": r["monthly"]} for r in results])
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.bar_chart(pd.DataFrame({r["provider"]: r["items"] for r in results}).T)
    st.subheader(f"Savings vs on-demand ({best['provider']})")
    st.bar_chart(pd.Series(savings_vs_on_demand(best["provider"], w), name="Monthly saving (USD)"))
    st.download_button("Download comparison (CSV)", table.to_csv(index=False), "comparison.csv", "text/csv")

# ---------- Tab 2: AI ----------
with tab2:
    history = pd.read_csv(DATA / "billing_history.csv", parse_dates=["date"])
    days = st.slider("Forecast horizon (days)", 7, 90, 30)
    fc = forecast_costs(history, days)
    chart = pd.concat([history.set_index("date")["cost"].rename("actual"),
                       fc.set_index("date")[["forecast", "lower", "upper"]]], axis=1)
    st.subheader("Daily cost: history and forecast")
    st.line_chart(chart.tail(180))
    st.metric(f"Forecast spend, next {days} days", f"${fc['forecast'].sum():,.0f}")
    st.subheader("Anomalous days")
    an = detect_anomalies(history)
    if an.empty:
        st.success("No anomalies detected.")
    else:
        st.warning(f"{len(an)} unusual cost spike(s) found")
        st.dataframe(an[["date", "cost", "z_score"]], use_container_width=True, hide_index=True)
    st.caption("Model: linear regression on trend + weekday + sale-season; anomalies via Isolation Forest on residuals.")

# ---------- Tab 3: advisor ----------
with tab3:
    inv = pd.read_csv(DATA / "resources.csv")
    recs = recommend(inv)
    st.metric("Potential monthly saving", f"${recs['est_monthly_saving'].sum():,.2f}")
    st.dataframe(recs, use_container_width=True, hide_index=True)
    with st.expander("Resource inventory"):
        st.dataframe(inv, use_container_width=True, hide_index=True)
