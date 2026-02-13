import pandas as pd

from src.states import assign_return_states


def test_assign_return_states_three_buckets():
    returns = pd.Series([-0.01, -0.001, 0.0, 0.001, 0.01])
    states = assign_return_states(returns, down_threshold=-0.002, up_threshold=0.002)
    assert states.tolist() == ["down", "flat", "flat", "flat", "up"]
