# Markov Market Forecast

A lightweight Python project that models daily market return regimes (`down`, `flat`, `up`) with a first-order Markov chain and produces next-day state probabilities from historical price data.

## What This Project Does

- Loads historical price data from CSV.
- Cleans and normalizes date/price columns.
- Computes simple daily returns.
- Maps returns into three regimes using configurable thresholds.
- Learns transition probabilities between regimes.
- Forecasts next-day regime probabilities from the most recent observed state.
- Exposes both:
- a command-line report (`main.py`)
- a Flask dashboard (`web_app.py`)

## Project Structure

```text
.
├── data/
│   └── S&P 500 Historical Data.csv
├── src/
│   ├── config.py      # Defaults (thresholds, file path, web settings)
│   ├── io.py          # CSV loading + cleaning
│   ├── returns.py     # Daily return calculation
│   ├── states.py      # Return-to-state mapping
│   ├── markov.py      # Transition counts/probabilities
│   ├── forecast.py    # End-to-end forecast pipeline
│   └── reports.py     # CLI reporting
├── templates/
│   └── index.html     # Flask dashboard template
├── tests/
│   ├── test_markov.py
│   └── test_states.py
├── main.py            # CLI entrypoint
└── web_app.py         # Web app entrypoint
```

## Requirements

- Python 3.10+ recommended
- Packages:
- `pandas`
- `numpy`
- `flask`
- `pytest` (for tests)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas numpy flask pytest
```

## CLI Usage

Run with default dataset:

```bash
python main.py
```

Run with a custom CSV:

```bash
python main.py path/to/your_prices.csv
```

The CLI prints:

- Last observed date
- Current inferred state
- Next-day probabilities for each state
- Most likely next-day state

## Web Dashboard Usage

Start server:

```bash
python web_app.py
```

Optional flags:

```bash
python web_app.py --host 127.0.0.1 --port 5000 --open
```

In the browser UI you can:

- Set `csv_path`
- Adjust `down` and `up` thresholds
- View dataset stats and date range
- Inspect next-day probabilities and predicted state
- See a transition matrix
- Run a 10-step, 1,000-trial simulation demo
- Review processed and raw tables

## Input Data Format

CSV must include:

- `Date` column (case-insensitive)
- Price column named one of:
- `Price`
- `Close`
- `Adj Close`

Notes:

- Price values may include commas (they are cleaned).
- Rows with invalid date/price are dropped.
- At least 3 clean rows are required.

## Model Details

1. Compute simple return:

```text
return_t = (price_t / price_{t-1}) - 1
```

2. Assign state by thresholds:

- `down` if `return < down_threshold`
- `flat` if `down_threshold <= return <= up_threshold`
- `up` if `return > up_threshold`

3. Build transition counts from `state_t -> state_{t+1}`.
4. Row-normalize counts into transition probabilities.
5. Use latest state row as `P(next_state | current_state)`.

Default thresholds are defined in `src/config.py`:

- `DEFAULT_DOWN_THRESHOLD = -0.002`
- `DEFAULT_UP_THRESHOLD = 0.002`

## Testing

Run tests:

```bash
pytest -q
```

Current test suite validates:

- Transition counts and normalized matrix behavior
- Next-state probability lookup
- Return-to-state bucketing logic

## Notes and Limitations

- This is a simple educational Markov regime model, not trading advice.
- Uses a first-order assumption (next state depends only on current state).
- No transaction costs, execution model, risk controls, or walk-forward validation are included by default.

## License

No license file is currently included in this repository.
