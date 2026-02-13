import argparse

from src.config import DEFAULT_CSV_PATH
from src.reports import print_forecast_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a Markov-chain next-day behavior forecast from price CSV data."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=str(DEFAULT_CSV_PATH),
        help="Path to CSV containing Date and Price/Close columns.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print_forecast_report(args.csv_path)


if __name__ == "__main__":
    main()
