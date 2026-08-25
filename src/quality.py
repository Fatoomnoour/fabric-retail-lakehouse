from __future__ import annotations

import pandas as pd

REQUIRED = {
    "order_id", "created_at", "customer_id", "country", "product_id",
    "product_name", "quantity", "unit_price", "status",
}


def run_quality_checks(raw: pd.DataFrame, silver: pd.DataFrame) -> dict[str, object]:
    checks = {
        "required_columns": REQUIRED.issubset(raw.columns),
        "unique_order_ids": bool(silver["order_id"].is_unique),
        "positive_quantity": bool((silver["quantity"] > 0).all()),
        "positive_price": bool((silver["unit_price"] > 0).all()),
        "gross_amount_reconciles": bool(
            (silver["gross_amount"] == silver["quantity"] * silver["unit_price"]).all()
        ),
    }
    return {"passed": all(checks.values()), "checks": checks}
