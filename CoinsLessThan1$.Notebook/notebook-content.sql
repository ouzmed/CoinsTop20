-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "synapse_pyspark"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "0dcd85f6-4c23-469f-9009-7e5da08bef8f",
-- META       "default_lakehouse_name": "lakehouse_coingecko",
-- META       "default_lakehouse_workspace_id": "457f9acf-c73d-42d8-935d-4b650cc966b5"
-- META     }
-- META   }
-- META }

-- CELL ********************

CREATE OR REPLACE TEMP VIEW vw_coins
AS SELECT * FROM lakehouse_coingecko.coins100

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }

-- CELL ********************

SELECT symbol, name, current_price, market_cap, ath, atl, cast(last_updated as date) as last_updated, market_cap_rank as rank
FROM vw_coins
WHERE current_price <= 1
ORDER BY rank asc

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }

-- CELL ********************


CREATE OR REPLACE TABLE coinc_less_1dollar
AS SELECT * FROM vw_coins

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }

-- CELL ********************

-- window function example:

with cte as (
select *, row_number() over( order by current_price asc) as rn
from coinc_less_1dollar
)

SELECT *
from cte
where rn <=10 and rn >=2

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }
