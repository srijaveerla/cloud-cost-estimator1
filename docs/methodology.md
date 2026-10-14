# Methodology

## Formula
```
Compute  = hourly_rate x hours_per_month x vm_count x (1 - discount)
Storage  = GB x price_per_GB_month   (block, object, database)
Egress   = GB_out x price_per_GB
Monthly  = Compute + Storage + Egress
Annual   = Monthly x 12
```

## Instance selection
For each provider the tool picks the cheapest instance type that meets the requested vCPU and RAM.

## Pricing models
On-demand, 1-year reserved, 3-year reserved and spot are modelled as flat discounts on compute only.

## Assumptions and limitations
- Linux VMs, one US region, no free tier.
- Prices in `data/pricing.json` are sample values; update them from official calculators.
- Excludes support plans, taxes, load balancers, monitoring and inter-region traffic.

## Future work
Live pricing via provider APIs, Terraform plan parsing, budget alerts, more regions.

## AI components
- **Forecast:** `LinearRegression` on [day index, 7 weekday dummies, sale flag]. Prediction band = forecast +/- 1.96 x robust sigma (MAD of residuals).
- **Anomalies:** `IsolationForest(contamination=0.03)` on residuals, kept only if the robust z-score exceeds 4.
- **Advisor:** transparent rules (CPU below 3% = idle; dev/test up over 90% = schedule off-hours; CPU below 20% with 4+ vCPU = right-size).
