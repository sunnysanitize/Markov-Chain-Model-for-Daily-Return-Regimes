from pathlib import Path

import pandas as pd

from src.config import DEFAULT_DOWN_THRESHOLD, DEFAULT_UP_THRESHOLD
from src.io import load_prices
from src.markov import next_state_probabilities, transition_matrix
from src.returns import add_simple_returns
from src.states import assign_return_states


def forecast_next_day(
    csv_path: str | Path,
    down_threshold: float = DEFAULT_DOWN_THRESHOLD,
    up_threshold: float = DEFAULT_UP_THRESHOLD,
) -> dict:
    """
    End-to-end pipeline:
    load prices -> returns -> states -> Markov matrix -> next-day probabilities.
    """
    prices = load_prices(csv_path)
    ret_df = add_simple_returns(prices)
    ret_df["state"] = assign_return_states(
        ret_df["return"], down_threshold=down_threshold, up_threshold=up_threshold
    )

    matrix = transition_matrix(ret_df["state"])
    current_state = ret_df["state"].iloc[-1]
    probs = next_state_probabilities(matrix, current_state)
    most_likely_state = probs.idxmax()

    return {
        "last_date": ret_df["date"].iloc[-1],
        "current_state": current_state,
        "transition_matrix": matrix,
        "next_day_probabilities": probs,
        "predicted_state": most_likely_state,
    }
