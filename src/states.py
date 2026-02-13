import pandas as pd

from src.config import DEFAULT_DOWN_THRESHOLD, DEFAULT_UP_THRESHOLD


def assign_return_states(
    returns: pd.Series,
    down_threshold: float = DEFAULT_DOWN_THRESHOLD,
    up_threshold: float = DEFAULT_UP_THRESHOLD,
) -> pd.Series:
    """
    Map numeric returns to 3 states:
    - 'down': return < down_threshold
    - 'flat': down_threshold <= return <= up_threshold
    - 'up':   return > up_threshold
    """
    if down_threshold > up_threshold:
        raise ValueError("down_threshold must be <= up_threshold")

    states = pd.Series(index=returns.index, dtype="object")
    states[returns < down_threshold] = "down"
    states[(returns >= down_threshold) & (returns <= up_threshold)] = "flat"
    states[returns > up_threshold] = "up"
    return states
