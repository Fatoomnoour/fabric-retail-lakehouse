import pandas as pd

from src.generate_sample import generate
from src.pipeline import transform_to_gold, transform_to_silver
from src.quality import run_quality_checks


def test_sample_has_stable_schema() -> None:
    raw = generate(12)
    assert len(raw) == 12
    assert raw["order_id"].is_unique


def test_silver_reconciles_amounts() -> None:
    silver = transform_to_silver(generate(12))
    report = run_quality_checks(generate(12), silver)
    assert report["passed"] is True
    assert (silver["gross_amount"] == silver["quantity"] * silver["unit_price"]).all()


def test_gold_contains_completed_orders_only() -> None:
    silver = transform_to_silver(generate(20))
    gold = transform_to_gold(silver)
    assert isinstance(gold, pd.DataFrame)
    assert int(gold["completed_orders"].sum()) == int(silver["status"].eq("completed").sum())
