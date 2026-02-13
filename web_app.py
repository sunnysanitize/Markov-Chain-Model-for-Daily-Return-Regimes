import argparse
from pathlib import Path
import webbrowser

import numpy as np
import pandas as pd
from flask import Flask, render_template, request

from src.config import (
    DEFAULT_CSV_PATH,
    DEFAULT_DOWN_THRESHOLD,
    DEFAULT_SIMULATION_STEPS,
    DEFAULT_SIMULATION_TRIALS,
    DEFAULT_UP_THRESHOLD,
    DEFAULT_WEB_HOST,
    DEFAULT_WEB_PORT,
)
from src.io import load_prices
from src.markov import transition_matrix
from src.returns import add_simple_returns
from src.states import assign_return_states

app = Flask(__name__)


def _simulate_paths(
    matrix: pd.DataFrame,
    start_state: str,
    steps: int = DEFAULT_SIMULATION_STEPS,
    trials: int = DEFAULT_SIMULATION_TRIALS,
) -> dict[str, float]:
    counts: dict[str, int] = {}

    if start_state not in matrix.index:
        return {}

    states = list(matrix.columns)
    for _ in range(trials):
        state = start_state
        for _ in range(steps):
            if state not in matrix.index:
                break
            probs = matrix.loc[state].values
            if probs.sum() <= 0:
                break
            state = np.random.choice(states, p=probs)
        counts[state] = counts.get(state, 0) + 1

    return {k: v / trials for k, v in sorted(counts.items())}


def _build_view_model(csv_path: str, down: float, up: float) -> dict:
    raw_df = pd.read_csv(csv_path)
    clean_df = load_prices(csv_path)
    ret_df = add_simple_returns(clean_df)
    ret_df["state"] = assign_return_states(ret_df["return"], down_threshold=down, up_threshold=up)

    matrix = transition_matrix(ret_df["state"])
    current_state = ret_df["state"].iloc[-1]
    probs = matrix.loc[current_state]
    predicted_state = probs.idxmax()
    simulation = _simulate_paths(matrix, current_state)

    return {
        "csv_path": csv_path,
        "down_threshold": down,
        "up_threshold": up,
        "raw_count": len(raw_df),
        "clean_count": len(clean_df),
        "start_date": clean_df["date"].iloc[0].date(),
        "end_date": clean_df["date"].iloc[-1].date(),
        "current_state": current_state,
        "predicted_state": predicted_state,
        "next_probs": [(k, float(v)) for k, v in probs.items()],
        "simulation_probs": list(simulation.items()),
        "raw_html": raw_df.to_html(index=False, classes="data-table"),
        "recent_html": ret_df.tail(30).to_html(index=False, classes="data-table"),
        "matrix_html": matrix.to_html(classes="data-table"),
    }


@app.get("/")
def index():
    csv_path = request.args.get("csv_path", str(DEFAULT_CSV_PATH))
    down = float(request.args.get("down", str(DEFAULT_DOWN_THRESHOLD)))
    up = float(request.args.get("up", str(DEFAULT_UP_THRESHOLD)))

    try:
        vm = _build_view_model(csv_path, down, up)
        return render_template("index.html", vm=vm, error=None)
    except Exception as exc:  # noqa: BLE001
        return render_template(
            "index.html",
            vm={
                "csv_path": csv_path,
                "down_threshold": down,
                "up_threshold": up,
            },
            error=str(exc),
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run browser UI for the Markov project.")
    parser.add_argument("--host", default=DEFAULT_WEB_HOST, help="Host for the web server")
    parser.add_argument("--port", default=DEFAULT_WEB_PORT, type=int, help="Port for the web server")
    parser.add_argument("--open", action="store_true", help="Open browser automatically")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.open:
        webbrowser.open(f"http://{args.host}:{args.port}/")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
