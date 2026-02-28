import argparse
import csv
from pathlib import Path


def slice_csv(input_path: Path, output_path: Path, limit: int) -> None:
    if limit < 0:
        raise ValueError("limit must be >= 0")

    with input_path.open("r", newline="", encoding="utf-8-sig") as src:
        reader = csv.reader(src)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError(f"Input CSV is empty: {input_path}")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="", encoding="utf-8") as dst:
            writer = csv.writer(dst)
            writer.writerow(header)
            for idx, row in enumerate(reader):
                if idx >= limit:
                    break
                writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write the first N email rows from a CSV into a new CSV file."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "emails.csv",
        help="Path to source CSV (default: repository emails.csv)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "emails_first_500.csv",
        help="Path to output CSV",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="How many data rows to copy (default: 500)",
    )
    args = parser.parse_args()

    slice_csv(args.input, args.output, args.limit)
    print(f"Wrote first {args.limit} rows to: {args.output}")


if __name__ == "__main__":
    main()
