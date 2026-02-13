import pandas as pd


def transition_counts(states: pd.Series) -> pd.DataFrame:
    """Count transitions from state_t -> state_{t+1}."""
    if len(states) < 2:
        raise ValueError("Need at least 2 states to build transitions")

    current = states.iloc[:-1].reset_index(drop=True)
    nxt = states.iloc[1:].reset_index(drop=True)
    counts = pd.crosstab(current, nxt)
    counts = counts.sort_index().reindex(sorted(counts.columns), axis=1, fill_value=0)
    return counts


def transition_matrix(states: pd.Series) -> pd.DataFrame:
    """
    Convert transition counts to row-normalized probabilities.
    Each row sums to 1 when that source state has observed transitions.
    """
    counts = transition_counts(states)
    row_sums = counts.sum(axis=1)
    matrix = counts.div(row_sums, axis=0)
    return matrix.fillna(0.0)


def next_state_probabilities(matrix: pd.DataFrame, current_state: str) -> pd.Series:
    """Return P(next_state | current_state)."""
    if current_state not in matrix.index:
        raise ValueError(f"State '{current_state}' not found in transition matrix")
    return matrix.loc[current_state]
