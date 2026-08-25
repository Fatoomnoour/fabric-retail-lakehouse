# Microsoft Fabric notebook source
# ruff: noqa: F821
# This source is intentionally kept readable for copy/paste into a Fabric notebook.

from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType

# In Fabric, replace this path with the Lakehouse Files path.
bronze_path = "Files/bronze/orders/"
silver_path = "Tables/silver_orders"

raw = spark.read.option("header", True).csv(bronze_path)

silver = (
    raw.withColumn("created_at", F.to_timestamp("created_at"))
    .withColumn("quantity", F.col("quantity").cast("int"))
    .withColumn("unit_price", F.col("unit_price").cast(DecimalType(12, 2)))
    .withColumn("gross_amount", F.col("quantity") * F.col("unit_price"))
    .withColumn("order_date", F.to_date("created_at"))
    .filter(
        F.col("order_id").isNotNull()
        & F.col("quantity").isNotNull()
        & (F.col("quantity") > 0)
        & F.col("unit_price").isNotNull()
        & (F.col("unit_price") > 0)
    )
    .dropDuplicates(["order_id"])
)

silver.write.mode("overwrite").format("delta").save(silver_path)
