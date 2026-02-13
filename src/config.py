from pathlib import Path


# Project-level defaults used across CLI, library code, and web UI.
DEFAULT_CSV_PATH = Path("data/S&P 500 Historical Data.csv")
DEFAULT_DOWN_THRESHOLD = -0.002
DEFAULT_UP_THRESHOLD = 0.002

# Web UI defaults.
DEFAULT_WEB_HOST = "127.0.0.1"
DEFAULT_WEB_PORT = 5000
DEFAULT_SIMULATION_STEPS = 10
DEFAULT_SIMULATION_TRIALS = 1000
