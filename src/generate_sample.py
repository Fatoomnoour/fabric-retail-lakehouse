from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

PRODUCTS = [("P100", "Laptop Stand", 42.0), ("P200", "USB Hub", 28.5), ("P300", "Desk Lamp", 35.0), ("P400", "Keyboard", 74.0)]


def generate(rows: int) -> pd.DataFrame:
    dates = pd.date_range("2025-01-01", periods=max(rows, 1), freq="h")[:rows]
    records = []
    for i, created_at in enumerate(dates, start=1):
        product_id, product_name, unit_price = PRODUCTS[(i - 1) % len(PRODUCTS)]
        quantity = (i % 4) + 1
        records.append(
            {
                "order_id": f"O{i:06d}",
                "created_at": created_at.isoformat(),
                "customer_id": f"C{((i - 1) % 20) + 1:04d}",
                "country": "EG" if i % 3 else "SA",
                "product_id": product_id,
                "product_name": product_name,
                "quantity": quantity,
                "unit_price": unit_price,
                "status": "completed" if i % 7 else "cancelled",
            }
        )
    return pd.DataFrame(records)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=500)
    parser.add_argument("--output", type=Path, default=Path("data/orders.csv"))
    args = parser.parse_args()
    if args.rows < 1:
        raise SystemExit("--rows must be positive")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    generate(args.rows).to_csv(args.output, index=False)
    print(f"wrote {args.rows} rows to {args.output}")


if __name__ == "__main__":
    main()
