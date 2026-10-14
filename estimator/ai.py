"""Machine-learning features: cost forecasting and anomaly detection."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression


def _features(dates: pd.Series, sale_flag: np.ndarray, start: pd.Timestamp) -> np.ndarray:
    t = (dates - start).dt.days.to_numpy().reshape(-1, 1)
    dow = np.eye(7)[dates.dt.dayofweek.to_numpy()]          # one-hot day of week
    return np.hstack([t, dow, np.asarray(sale_flag).reshape(-1, 1)])


def fit_model(history: pd.DataFrame) -> tuple[LinearRegression, np.ndarray]:
    """Fit trend + weekday + sale-season regression. Returns model and residuals."""
    start = history["date"].min()
    X = _features(history["date"], history["sale_flag"].to_numpy(), start)
    model = LinearRegression().fit(X, history["cost"].to_numpy())
    residuals = history["cost"].to_numpy() - model.predict(X)
    return model, residuals


def forecast_costs(history: pd.DataFrame, days: int = 30) -> pd.DataFrame:
    """Forecast daily cost for the next `days` days with a 95% prediction band."""
    model, residuals = fit_model(history)
    start = history["date"].min()
    future = pd.DataFrame({"date": pd.date_range(history["date"].max() + pd.Timedelta(days=1),
                                                 periods=days, freq="D")})
    X = _features(future["date"], np.zeros(days), start)
    future["forecast"] = model.predict(X).round(2)
    # robust spread estimate so injected anomalies do not inflate the band
    sigma = 1.4826 * np.median(np.abs(residuals - np.median(residuals)))
    future["lower"] = (future["forecast"] - 1.96 * sigma).round(2)
    future["upper"] = (future["forecast"] + 1.96 * sigma).round(2)
    return future


def detect_anomalies(history: pd.DataFrame, contamination: float = 0.03) -> pd.DataFrame:
    """Flag days with unusually high spend after removing trend, weekday and sale effects."""
    _, residuals = fit_model(history)
    iso = IsolationForest(contamination=contamination, random_state=42)
    flagged = iso.fit_predict(residuals.reshape(-1, 1)) == -1
    sigma = 1.4826 * np.median(np.abs(residuals - np.median(residuals)))
    z = (residuals - np.median(residuals)) / sigma
    out = history.assign(residual=residuals.round(2), z_score=z.round(1))
    return out[flagged & (z > 4)].reset_index(drop=True)
