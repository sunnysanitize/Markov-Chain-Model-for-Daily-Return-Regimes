from src.forecast import forecast_next_day


def print_forecast_report(csv_path: str) -> None:
    result = forecast_next_day(csv_path)
    probs = result["next_day_probabilities"]

    print(f"Last observed date: {result['last_date'].date()}")
    print(f"Current state: {result['current_state']}")
    print("Next-day state probabilities:")
    for state, p in probs.items():
        print(f"  {state}: {p:.2%}")
    print(f"Predicted next-day state: {result['predicted_state']}")
