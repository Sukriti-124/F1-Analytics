# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Run environment config
# MAGIC %run ../00-common/01.environment-config

# COMMAND ----------

# DBTITLE 1,v_2026_wdc_predictions
# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW formula1.gold.v_driver_predictions_2026
# MAGIC AS
# MAGIC SELECT
# MAGIC     predicted_pos,
# MAGIC     driver_name,
# MAGIC     constructor_name                    AS team,
# MAGIC     ROUND(prediction_score, 1)          AS prediction_score,
# MAGIC     ROUND(drv_score * 100, 1)           AS driver_score,
# MAGIC     ROUND(con_score * 100, 1)           AS constructor_score,
# MAGIC     driver_rookie                       AS is_rookie,
# MAGIC     constructor_rookie                  AS is_new_team
# MAGIC FROM formula1.gold.pred_2026_drivers
# MAGIC ORDER BY predicted_pos;

# COMMAND ----------

# DBTITLE 1,v_2026_wcc_predictions
# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW formula1.gold.v_constructor_predictions_2026
# MAGIC AS
# MAGIC SELECT
# MAGIC     predicted_pos,
# MAGIC     team,
# MAGIC     ROUND(team_score, 1)                AS team_score,
# MAGIC     ROUND(best_driver_score, 1)         AS best_driver_score,
# MAGIC     ROUND(second_driver_score, 1)       AS second_driver_score
# MAGIC FROM formula1.gold.pred_2026_constructors
# MAGIC ORDER BY predicted_pos;
