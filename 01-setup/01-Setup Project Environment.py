-- Databricks notebook source
-- MAGIC %fs ls abfss://formula1@databricksextdlf1.dfs.core.windows.net/

-- COMMAND ----------

SHOW CATALOGS;

-- COMMAND ----------

-- DBTITLE 1,Create formula1 catalog
CREATE CATALOG IF NOT EXISTS formula1
MANAGED LOCATION 'abfss://formula1@databricksextdlf1.dfs.core.windows.net/managed/formula1';

-- COMMAND ----------

-- DBTITLE 1,Create landing schema
CREATE SCHEMA IF NOT EXISTS formula1.landing;

-- COMMAND ----------

USE CATALOG formula1;

-- COMMAND ----------

SHOW SCHEMAS;

-- COMMAND ----------

-- DBTITLE 1,Create external volume
CREATE EXTERNAL VOLUME formula1.landing.files
LOCATION 'abfss://formula1@databricksextdlf1.dfs.core.windows.net/landing';

-- COMMAND ----------

-- MAGIC %fs ls /Volumes/formula1/landing/files
