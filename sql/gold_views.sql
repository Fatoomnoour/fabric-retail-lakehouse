-- Fabric Warehouse / Lakehouse SQL endpoint serving layer

CREATE OR ALTER VIEW gold.vw_daily_country_sales AS
SELECT
    order_date,
    country,
    completed_orders,
    revenue,
    units_sold,
    average_order_value
FROM gold_daily_country_sales;

CREATE OR ALTER VIEW gold.vw_country_rank AS
SELECT
    country,
    SUM(revenue) AS total_revenue,
    SUM(completed_orders) AS completed_orders,
    RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM gold_daily_country_sales
GROUP BY country;
