
# ☁️ Cloud Cost Estimator with AI Forecasting

An AI-powered cloud cost estimation and optimization platform that compares AWS, Azure, and Google Cloud Platform (GCP), forecasts future spending, detects unusual cost spikes, and recommends potential savings.

## 📌 Project Scenario

**ShopNest**, an online store migrating to the cloud, faces growing traffic, festival-sale spikes, and unpredictable cloud bills.

This project helps ShopNest estimate cloud expenses, predict future spending, identify unusual cost increases, and optimize cloud resources.

Read [docs/scenario.md](docs/scenario.md) for the complete business scenario.

## ✨ Features

| Module | Description |
|---|---|
| Cloud Cost Estimator | Estimates workload costs across AWS, Azure, and GCP for compute, storage, databases, and data transfer. Supports on-demand, reserved, and spot pricing where configured. |
| AI Forecasting | Uses regression features such as time trends, weekdays, and sale-season indicators to forecast spending 7–90 days ahead. |
| Anomaly Detection | Uses Isolation Forest and residual-based statistical checks to identify unusual spending patterns. |
| Savings Advisor | Identifies potential opportunities involving idle resources, oversized instances, and continuously running non-production environments. |
| Interactive Dashboard | Presents estimates, forecasts, anomalies, and savings recommendations through a Streamlit interface. |
| Automated Testing | Uses pytest and GitHub Actions to support repeatable testing and continuous integration. |

## 🛠️ Technology Stack

- **Language:** Python
- **Dashboard:** Streamlit
- **Machine Learning:** Regression and Isolation Forest
- **Testing:** pytest
- **Continuous Integration:** GitHub Actions
- **Data:** CSV and JSON

The technologies and features listed above describe the intended project design. Confirm that each feature is implemented in the current codebase before presenting it as completed functionality.

## 🗂️ Project Structure

```text
cloud-cost-estimator/
├── app.py
├── estimator/
│   ├── calculator.py
│   ├── ai.py
│   ├── optimizer.py
│   └── data_gen.py
├── data/
│   ├── pricing.json
│   └── billing_history.csv
├── tests/
├── docs/
│   ├── scenario.md
│   └── methodology.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

*Note: This is the intended structure. Your actual files and folders may differ.*

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- pip

### 1. Clone the repository

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username and use the correct repository URL.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/cloud-cost-estimator1.git
cd cloud-cost-estimator1
```

If you already have the project locally, skip cloning and navigate to your existing project directory.

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux or macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Generate sample billing data (optional)

```bash
python -m estimator.data_gen
```

Run this only if the data generator exists and you intend to generate or replace the sample data.

### 5. Start the dashboard

```bash
streamlit run app.py
```

Open the local URL printed in your terminal, usually `http://localhost:8501`.

### 6. Run automated tests

```bash
pytest
```

If a command fails, check the error message and confirm that the corresponding module, dependency, or test configuration exists.

## 🧠 Methodology

### Cloud Cost Estimation

The estimator combines the costs of configured compute, storage, database, and data-transfer resources.

A simplified compute formula is:

```text
Compute Cost =
Hourly Rate × Runtime Hours × Number of Instances × Discount Factor

Estimated Total Cost =
Compute + Storage + Database + Data Transfer
```

Actual costs depend on resource configurations, billing periods, regional prices, discounts, and the calculation logic implemented in the project.

See [docs/methodology.md](docs/methodology.md) for further details.

### AI Forecasting

The planned forecasting approach considers:

- Historical spending trends
- Day-of-week effects
- Sale-season indicators
- Historical billing data

The model is designed to forecast spending over horizons of 7–90 days. Prediction intervals should be evaluated against held-out data before making claims about their coverage or accuracy.

### Anomaly Detection

Isolation Forest and residual-based statistical checks can help identify spending that differs from expected patterns.

The goal is to distinguish unexpected cost increases from ordinary variations, including seasonal sales. Actual performance depends on the model, its thresholds, and the quality of the training data.

### Savings Recommendations

The optimizer can evaluate potential savings opportunities involving:

- Idle resources
- Oversized instances
- Always-on non-production environments
- Alternative pricing plans

Savings estimates are indicative and should be validated against actual resource usage and current cloud-provider prices.

## 📊 Sample Data and Pricing

The sample billing history is synthetic and intended for demonstration rather than production billing analysis.

Illustrative pricing values may be stored in `data/pricing.json`. Verify current rates using the official calculators:

- [AWS Pricing Calculator](https://calculator.aws/)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator)

For real-world analysis, replace synthetic data with verified billing exports and adapt the application to the export schema.

The example billing CSV schema is:

```csv
date,cost,sale_flag
2026-01-01,120.50,0
2026-01-02,135.75,0
2026-01-03,210.00,1
```

These rows are illustrative examples, not actual cloud billing records. Ensure the CSV columns and data types match what your implementation expects.

## ⚠️ Limitations

- Sample prices may not reflect current provider rates.
- Synthetic billing data may not represent actual workloads.
- Forecast quality depends on data quality and changing usage patterns.
- Anomaly detection may produce false positives or miss unexpected events.
- Savings recommendations require validation against actual resource utilization.
- Cloud prices, discounts, taxes, and regional charges vary.
- Forecast intervals are estimates and are not guaranteed to provide a particular coverage rate.

## 🛣️ Roadmap

- [ ] Integrate verified live cloud pricing APIs.
- [ ] Import AWS Cost Explorer and Azure Cost Management exports.
- [ ] Support Google Cloud billing exports.
- [ ] Add an LLM-generated plain-English cost report.
- [ ] Support multiple cloud regions.
- [ ] Evaluate forecast accuracy using historical holdout data.
- [ ] Improve anomaly explanations and alerting.
- [ ] Add more realistic business workload scenarios.
- [ ] Add dashboard export and downloadable reports.

## 👩‍💻 Author

**Name:** Your Name  
**College:** Your College  
**Project:** Cloud Cost Estimator with AI Forecasting

Replace the placeholders with your actual details before publishing.

## 📄 License

This project is intended to use the MIT License. Include a valid `LICENSE` file containing the MIT License text before claiming the repository is licensed under MIT.
