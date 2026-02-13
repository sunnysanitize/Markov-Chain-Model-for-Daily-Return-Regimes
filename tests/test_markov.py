import math

import pandas as pd

from src.markov import next_state_probabilities, transition_counts, transition_matrix


def test_transition_counts_and_matrix():
    # transitions: down->up, up->up, up->flat, flat->down
    states = pd.Series(["down", "up", "up", "flat", "down"])
    counts = transition_counts(states)

    assert counts.loc["down", "up"] == 1
    assert counts.loc["up", "up"] == 1
    assert counts.loc["up", "flat"] == 1
    assert counts.loc["flat", "down"] == 1

    matrix = transition_matrix(states)
    assert math.isclose(matrix.loc["down", "up"], 1.0)
    assert math.isclose(matrix.loc["flat", "down"], 1.0)
    assert math.isclose(matrix.loc["up", "up"], 0.5)
    assert math.isclose(matrix.loc["up", "flat"], 0.5)


def test_next_state_probabilities():
    states = pd.Series(["down", "up", "up", "flat", "down"])
    matrix = transition_matrix(states)
    probs = next_state_probabilities(matrix, "up")
    assert math.isclose(probs["up"], 0.5)
    assert math.isclose(probs["flat"], 0.5)
