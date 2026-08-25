# Power BI Direct Lake setup

## Target architecture

```text
Fabric Lakehouse
  └── Delta table: gold_daily_country_sales
          |
          v
Power BI semantic model: Direct Lake on OneLake
          |
          v
Power BI report: Retail Executive Pulse
```

## Create the model

1. Open the Fabric workspace that contains the Retail Lakehouse.
2. Open the Lakehouse and confirm that the Gold table is a managed Delta table under `Tables`, not only a file under `Files`.
3. Select **New semantic model** or open Power BI Desktop and use the OneLake catalog.
4. Select `gold_daily_country_sales` and any dimensions such as `dim_date`, `dim_country`, and `dim_product`.
5. Confirm that the table storage mode is **Direct Lake on OneLake**. Use Direct Lake on SQL only when SQL endpoint security or SQL views are a deliberate requirement.
6. Add relationships in a star schema. Keep the Gold fact table on the many side and dimensions on the one side.
7. Create the measures from `measures.dax`, hide technical columns, format currency and percentages, then publish the report to the same workspace.

## Recommended model

| Table | Grain | Key |
| --- | --- | --- |
| `fact_daily_country_sales` | one row per order date and country | `order_date`, `country` |
| `dim_date` | one row per calendar date | `date` |
| `dim_country` | one row per country | `country` |

If the first iteration only has the Gold aggregate, it is acceptable to use that single table. For a stronger model, add the dimensions before taking the recruiter screenshot.

## Refresh and performance checks

Direct Lake refresh is primarily metadata framing: it points the semantic model at the newest Delta table files instead of copying the full dataset as Import mode does. After a pipeline run, refresh the semantic model and verify that the report reflects the newest Gold version.

In the model settings, review whether any table or expression causes a DirectQuery fallback. Keep the report based on physical Delta tables for the cleanest Direct Lake demonstration, avoid unnecessary SQL views in the Direct Lake path, and use a small number of explicit measures instead of expensive visual-level calculations.

## Recruiter-ready report pages

### Executive Pulse

Use KPI cards for Revenue, Completed Orders, Units Sold, and Average Order Value. Add a line chart for daily revenue, a bar chart for revenue by country, and a date slicer. Put the architecture or data freshness note in a small footer.

### Market Detail

Use a country drill-through page with revenue, order count, average order value, and a product table. Add a tooltip page showing the selected date range and last pipeline run.

### Data Reliability

Show last successful load time, source row count, Silver row count, rejected row count, and quality status. This page makes the project look like an engineering system rather than a decorative dashboard.

## What to capture

Take screenshots of the Fabric workspace, Lakehouse Tables area, semantic model storage mode, lineage view, and the final Power BI pages. Remove tenant IDs and any personal information. In GitHub, commit only sanitized screenshots under `powerbi/screenshots/` and never commit a `.pbix` file containing credentials.
