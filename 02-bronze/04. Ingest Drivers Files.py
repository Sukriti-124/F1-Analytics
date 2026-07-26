# Databricks notebook source
# MAGIC %run ../00-common/01.environment-config

# COMMAND ----------

# MAGIC %run ../00-common/02.bronze-helpers
# MAGIC

# COMMAND ----------

source_file = f"{landing_folder_path}/drivers.json"
table_name = f"{catalog_name}.{bronze_schema}.drivers"


# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, DateType

name_schema = StructType([
    StructField('givenName', StringType()),
    StructField('familyName', StringType())
])

drivers_schema = StructType([
    StructField('driverId', StringType()),
    StructField('name', name_schema),
    StructField('dateOfBirth', DateType()),
    StructField('nationality', StringType()),
    StructField('url', StringType())
])

# COMMAND ----------

drivers_df = (
    spark.read
       .format('json')
       .schema(drivers_schema)
       .option('mode', 'FAILFAST')
       .load(source_file)
)

# COMMAND ----------

drivers_final_df = add_ingestion_metadata(drivers_df)


# COMMAND ----------

(
    drivers_final_df
        .write
        .format('delta')
        .mode('overwrite')
        .saveAsTable(table_name)
)


# COMMAND ----------

display(spark.table(table_name))
