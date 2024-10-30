# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "0dcd85f6-4c23-469f-9009-7e5da08bef8f",
# META       "default_lakehouse_name": "lakehouse_coingecko",
# META       "default_lakehouse_workspace_id": "457f9acf-c73d-42d8-935d-4b650cc966b5"
# META     }
# META   }
# META }

# MARKDOWN ********************

# ## Display the 10 coins crypto in the market

# CELL ********************

from pyspark.sql.functions import col

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.table("lakehouse_coingecko.coins100")
# we can also write: df=spark.sql("select * from coins100")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#df.count() --> 100
df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# filter only the 10 coins with the useful information

df20 = df.filter(col("market_cap_rank") <= 20 ).select("symbol","name","current_price","ath","atl","last_updated")\
        .withColumn("last_updated", col("last_updated").cast("date"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df20)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df20.write.format("delta").mode("overwrite").saveAsTable("lakehouse_coingecko.top20")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
