# Microsoft Fabric notebook source
# ruff: noqa: F821

from pyspark.sql import functions as F

silver_path = "Tables/silver_orders"
gold_path = "Tables/gold_daily_country_sales"

silver = spark.read.format("delta").load(silver_path)

gold = (
    silver.filter(F.col("status") == "completed")
    .groupBy("order_date", "country")
    .agg(
        F.countDistinct("order_id").alias("completed_orders"),
        F.sum("gross_amount").alias("revenue"),
        F.sum("quantity").alias("units_sold"),
        F.avg("gross_amount").alias("average_order_value"),
    )
)

gold.write.mode("overwrite").format("delta").save(gold_path)
