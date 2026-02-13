import pandas as pd


def add_simple_returns(df: pd.DataFrame, price_col: str = "close") -> pd.DataFrame:
    """
    Add a simple daily return column:
    return_t = (price_t / price_{t-1}) - 1
    """
    if price_col not in df.columns:
        raise ValueError(f"Missing '{price_col}' column in input DataFrame")

    out = df.copy()
    out["return"] = out[price_col].pct_change()
    return out.dropna(subset=["return"]).reset_index(drop=True)
