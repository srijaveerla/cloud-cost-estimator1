# ☁️ Cloud Cost Estimator with AI Forecasting

Estimate, forecast and optimise cloud spend for a realistic business scenario.

**Scenario:** *ShopNest*, an online store migrating to the cloud, faces growing traffic, festival-sale spikes and
unpredictable bills. See [docs/scenario.md](docs/scenario.md).

## Features
| Module | What it does |
|---|---|
| **Cost estimator** | Compares AWS, Azure and GCP for a workload (compute, storage, database, egress) under on-demand, reserved and spot pricing |
| **AI forecasting** | Regression model (trend + weekday + sale season) predicts the next 7 to 90 days of spend with a 95% band |
| **Anomaly detection** | Isolation Forest on model residuals flags sudden cost spikes, such as a forgotten instance |
| **Savings advisor** | Finds idle, over-sized and always-on non-production resources and estimates monthly savings |

Dashboard built with Streamlit; core logic is separate from the UI and covered by pytest. CI runs on every push (GitHub Actions).

## Project structure
```
├── app.py                    # Streamlit dashboard (3 tabs)
├── estimator/
│   ├── calculator.py         # cost engine
│   ├── ai.py                 # forecasting + anomaly detection
│   ├── optimizer.py          # savings recommendations
│   └── data_gen.py           # synthetic billing data generator
├── data/                     # pricing, scenario, billing history, resources
├── tests/                    # 10 unit tests
├── docs/                     # scenario + methodology
└── .github/workflows/ci.yml  # automated tests
```

## Run it
```bash
git clone https://github.com/<your-username>/cloud-cost-estimator.git
cd cloud-cost-estimator
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m estimator.data_gen      # optional: regenerate sample data
streamlit run app.py
pytest
```

## Method (short)
- Cost = compute (hourly rate x hours x VMs x discount) + storage + egress. See [docs/methodology.md](docs/methodology.md).
- Forecast = linear regression on day index, day-of-week and a sale-season flag; band from a robust residual spread.
- Anomaly = Isolation Forest on residuals AND a z-score above 4, which avoids flagging normal sale spikes.

## Limitations
- Prices in `data/pricing.json` are illustrative samples; verify with the official AWS, Azure and GCP calculators.
- Billing history is synthetic. Replace `data/billing_history.csv` with a real export (columns: `date`, `cost`, `sale_flag`).

## Roadmap
- [ ] Live pricing via provider APIs
- [ ] Import real AWS Cost Explorer / Azure Cost Management exports
- [ ] LLM-generated plain-English cost report
- [ ] Multi-region support

## Author
<Your Name> · <college> · Internship at <company>

## License
MIT
