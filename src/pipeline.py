from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .quality import run_quality_checks

SILVER_COLUMNS = [
    "order_id", "order_date", "customer_id", "country", "product_id",
    "product_name", "quantity", "unit_price", "gross_amount", "status",
]


def transform_to_silver(raw: pd.DataFrame) -> pd.DataFrame:
    frame = raw.copy()
    frame["created_at"] = pd.to_datetime(frame["created_at"], errors="coerce", utc=True)
    frame["quantity"] = pd.to_numeric(frame["quantity"], errors="coerce")
    frame["unit_price"] = pd.to_numeric(frame["unit_price"], errors="coerce")
    frame["gross_amount"] = frame["quantity"] * frame["unit_price"]
    frame["order_date"] = frame["created_at"].dt.date.astype("string")
    frame = frame[SILVER_COLUMNS]
    return frame.dropna(subset=["order_id", "order_date", "quantity", "unit_price"])


def transform_to_gold(silver: pd.DataFrame) -> pd.DataFrame:
    valid = silver[silver["status"].eq("completed")]
    return (
        valid.groupby(["order_date", "country"], as_index=False)
        .agg(
            completed_orders=("order_id", "nunique"),
            revenue=("gross_amount", "sum"),
            units_sold=("quantity", "sum"),
            average_order_value=("gross_amount", "mean"),
        )
        .sort_values(["order_date", "country"])
    )


def run(input_path: Path, output_dir: Path) -> dict[str, int]:
    raw = pd.read_csv(input_path)
    silver = transform_to_silver(raw)
    report = run_quality_checks(raw, silver)
    if not report["passed"]:
        raise ValueError(f"quality gate failed: {report}")
    gold = transform_to_gold(silver)
    bronze_path = output_dir / "bronze/orders.csv"
    silver_path = output_dir / "silver/orders.parquet"
    gold_path = output_dir / "gold/daily_country_sales.parquet"
    for path in (bronze_path, silver_path, gold_path):
        path.parent.mkdir(parents=True, exist_ok=True)
    raw.to_csv(bronze_path, index=False)
    silver.to_parquet(silver_path, index=False)
    gold.to_parquet(gold_path, index=False)
    report_path = output_dir / "quality_report.json"
    report_path.write_text(pd.Series(report).to_json(), encoding="utf-8")
    return {"bronze_rows": len(raw), "silver_rows": len(silver), "gold_rows": len(gold)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/orders.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/warehouse"))
    args = parser.parse_args()
    print(run(args.input, args.output_dir))


if __name__ == "__main__":
    main()
