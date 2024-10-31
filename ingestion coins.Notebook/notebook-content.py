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

# PARAMETERS CELL ********************

# parametres
myKey=""

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Import Libraries

# CELL ********************

import requests
import json
from pyspark.sql.functions import *
from pyspark.sql.types import *

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## function to call the api and fetch the data

# CELL ********************

def get_data(url, headers=None):

    response = requests.get(url, headers)
    if response.status_code == 200:
        return response
    else:
        print(f"code error {response.status_code}: {response.text}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# the information about the api:

currency ="usd"
#myKey ="xxxxx"
url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}"

headers = {
    'accept':'application/json',
    "x-cg-demo-api-key": myKey
}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# apply the function get_data:

data = get_data(url, headers).json()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

type(data)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(data[0])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

id=[]
symbol=[]
name=[] 
image=[]
current_price=[]
market_cap=[]
market_cap_rank=[]
fully_diluted_valuation=[]
total_volume=[]
high_24h=[]
low_24h=[]
price_change_24h=[]
price_change_percentage_24h=[]
market_cap_change_24h=[]
market_cap_change_percentage_24h=[]
circulating_supply=[]
total_supply=[]
max_supply=[]
ath=[]
ath_date=[]
atl=[]
atl_date=[]
last_updated=[]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

for ligne in data:

    id.append(ligne['id']),
    symbol.append(ligne['symbol']),
    name.append(ligne['name']),
    image.append(ligne['image']),
    current_price.append(ligne['current_price']),
    market_cap.append(ligne['market_cap']),
    market_cap_rank.append(ligne['market_cap_rank']),
    fully_diluted_valuation.append(ligne['fully_diluted_valuation']),
    total_volume.append(ligne['total_volume']),
    high_24h.append(ligne['high_24h']),
    low_24h.append(ligne['low_24h']),
    price_change_24h.append(ligne['price_change_24h']),
    price_change_percentage_24h.append(ligne['price_change_percentage_24h']),
    market_cap_change_24h.append(ligne['market_cap_change_24h']),
    market_cap_change_percentage_24h.append(ligne['market_cap_change_percentage_24h']),
    circulating_supply.append(ligne['circulating_supply']),
    total_supply.append(ligne['total_supply']),
    max_supply.append(ligne['max_supply']),
    ath.append(ligne['ath']),
    ath_date.append(ligne['ath_date']),
    atl.append(ligne['atl']),
    atl_date.append(ligne['atl_date']),
    last_updated.append(ligne['last_updated'])


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# the data:
data1 = list(zip(id, symbol, name, image, current_price, market_cap, market_cap_rank, fully_diluted_valuation, total_volume, high_24h, low_24h, price_change_24h, price_change_percentage_24h, market_cap_change_24h, market_cap_change_percentage_24h, circulating_supply, total_supply, max_supply, ath, ath_date, atl, atl_date, last_updated))

# creating the schema:
schema = StructType([
    StructField('id', StringType()),
    StructField('symbol', StringType()),
    StructField('name', StringType()),
    StructField('image', StringType()),
    StructField('current_price', StringType()),
    StructField('market_cap', LongType()),
    StructField('market_cap_rank', IntegerType()),
    StructField('fully_diluted_valuation', LongType()),
    StructField('total_volume', LongType()),
    StructField('high_24h', StringType()),
    StructField('low_24h', StringType()),
    StructField('price_change_24h', FloatType()),
    StructField('price_change_percentage_24h', FloatType()),
    StructField('market_cap_change_24h', StringType()),
    StructField('market_cap_change_percentage_24h', FloatType()),
    StructField('circulating_supply', FloatType()),
    StructField('total_supply', FloatType()),
    StructField('max_supply', FloatType()),
    StructField('ath', StringType()),
    StructField('ath_date', StringType()),
    StructField('atl', StringType()),
    StructField('atl_date', StringType()),
    StructField('last_updated', StringType()),
])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Creation of the dataframe

# CELL ********************

df_coins = spark.createDataFrame(data = data1, schema = schema)
display(df_coins)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_coins.write.format("delta").mode("overwrite").saveAsTable("lakehouse_coingecko.coins100")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
