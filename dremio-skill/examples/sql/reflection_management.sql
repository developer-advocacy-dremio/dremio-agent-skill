-- Dremio Reflection Management "Golden Path"
-- Best practices for creating and managing reflections to accelerate queries.

-- 1. Raw Reflection: Accelerate detailed queries (filtering, sorting)
-- Typically used on the "Physical Dataset" (PDS) or a base view.
ALTER DATASET "Source"."Raw_Data"."Sales"
CREATE RAW REFLECTION "Sales_Raw_Acceleration"
USING DISPLAY (
    "transaction_id",
    "customer_id",
    "product_id",
    "sale_date",
    "amount"
)
DISTRIBUTE BY ("customer_id")
PARTITION BY ("sale_date")
LOCALSORT BY ("sale_date", "transaction_id");

-- 2. Aggregation Reflection: Accelerate BI dashboards (GROUP BY, SUM, COUNT)
-- Typically used on the "Virtual Dataset" (VDS) served to BI tools.
ALTER DATASET "Space"."Analytics"."Monthly_Sales_Summary"
CREATE AGGREGATE REFLECTION "Sales_Agg_Acceleration"
USING 
DIMENSIONS (
    "sale_year",
    "sale_month",
    "region",
    "product_category"
)
MEASURES (
    "total_revenue" (SUM),
    "transaction_count" (COUNT),
    "avg_sale_amount" (SUM, COUNT) -- COUNT and SUM needed for AVG
)
DISTRIBUTE BY ("region")
PARTITION BY ("sale_year");

-- 3. Maintenance: Trigger a refresh manually (if not on schedule)
ALTER DATASET "Space"."Analytics"."Monthly_Sales_Summary"
REFRESH METADATA AUTO PROMOTION;

-- 4. Check Status (Metadata Query)
-- Use this to verify if reflections are ready
SELECT * 
FROM sys.reflections 
WHERE dataset_name = 'Monthly_Sales_Summary';
