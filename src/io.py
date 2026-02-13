from pathlib import Path
import pandas as pd


def _to_float(s: pd.Series) -> pd.Series:
    # Remove commas and convert to float
    return pd.to_numeric(s.astype(str).str.replace(",", "", regex=False), errors="coerce")


def load_prices(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Case-insensitive column mapping
    cols = {c.lower().strip(): c for c in df.columns}

    if "date" not in cols:
        raise ValueError("CSV must contain a 'Date' column")

    # Accept 'price' or 'close' or 'adj close'
    price_col = None
    for candidate in ("price", "close", "adj close"):
        if candidate in cols:
            price_col = cols[candidate]
            break

    if price_col is None:
        raise ValueError("CSV must contain 'Price' (or 'Close'/'Adj Close') column")

    df = df.rename(columns={cols["date"]: "date", price_col: "close"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["close"] = _to_float(df["close"])

    df = df.dropna(subset=["date", "close"]).sort_values("date").reset_index(drop=True)

    if len(df) < 3:
        raise ValueError("Not enough clean rows. Need at least 3 dates to compute transitions.")

    return df
