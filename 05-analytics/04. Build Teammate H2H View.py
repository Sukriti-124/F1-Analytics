# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Run environment config
# MAGIC %run ../00-common/01.environment-config

# COMMAND ----------

# DBTITLE 1,v_teammate_h2h
# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW formula1.gold.v_teammate_h2h AS
# MAGIC WITH driver_season_stats AS (
# MAGIC     SELECT
# MAGIC         r.season,
# MAGIC         r.constructor_id,
# MAGIC         c.constructor_name                                          AS team,
# MAGIC         r.driver_id,
# MAGIC         d.driver_name,
# MAGIC         COUNT(*)                                                    AS races,
# MAGIC         SUM(r.points)                                               AS total_points,
# MAGIC         COUNT_IF(r.is_win)                                          AS wins,
# MAGIC         COUNT_IF(r.is_podium)                                       AS podiums,
# MAGIC         ROUND(AVG(NULLIF(r.final_position, 0)), 1)                 AS avg_finish,
# MAGIC         ROUND(AVG(NULLIF(r.grid_position,   0)), 1)                AS avg_grid
# MAGIC     FROM formula1.gold.fact_session_results r
# MAGIC     JOIN formula1.gold.dim_drivers      d ON r.driver_id      = d.driver_id
# MAGIC     JOIN formula1.gold.dim_constructors c ON r.constructor_id = c.constructor_id
# MAGIC     WHERE r.session_type = 'RACE'
# MAGIC     GROUP BY r.season, r.constructor_id, c.constructor_name, r.driver_id, d.driver_name
# MAGIC ),
# MAGIC h2h_races AS (
# MAGIC     SELECT
# MAGIC         r1.season,
# MAGIC         r1.constructor_id,
# MAGIC         r1.driver_id                                                                     AS driver1_id,
# MAGIC         r2.driver_id                                                                     AS driver2_id,
# MAGIC         COUNT_IF(r1.final_position > 0 AND r2.final_position > 0
# MAGIC                  AND r1.final_position < r2.final_position)                             AS driver1_ahead,
# MAGIC         COUNT_IF(r1.final_position > 0 AND r2.final_position > 0
# MAGIC                  AND r2.final_position < r1.final_position)                             AS driver2_ahead
# MAGIC     FROM formula1.gold.fact_session_results r1
# MAGIC     JOIN formula1.gold.fact_session_results r2
# MAGIC         ON  r1.season         = r2.season
# MAGIC         AND r1.round          = r2.round
# MAGIC         AND r1.constructor_id = r2.constructor_id
# MAGIC         AND r1.driver_id      < r2.driver_id
# MAGIC         AND r1.session_type   = 'RACE'
# MAGIC         AND r2.session_type   = 'RACE'
# MAGIC     GROUP BY r1.season, r1.constructor_id, r1.driver_id, r2.driver_id
# MAGIC )
# MAGIC SELECT
# MAGIC     s1.season,
# MAGIC     s1.team,
# MAGIC     s1.driver_name                                                  AS driver1,
# MAGIC     s2.driver_name                                                  AS driver2,
# MAGIC     s1.total_points                                                 AS driver1_points,
# MAGIC     s2.total_points                                                 AS driver2_points,
# MAGIC     s1.wins                                                         AS driver1_wins,
# MAGIC     s2.wins                                                         AS driver2_wins,
# MAGIC     s1.podiums                                                      AS driver1_podiums,
# MAGIC     s2.podiums                                                      AS driver2_podiums,
# MAGIC     s1.avg_finish                                                   AS driver1_avg_finish,
# MAGIC     s2.avg_finish                                                   AS driver2_avg_finish,
# MAGIC     s1.avg_grid                                                     AS driver1_avg_grid,
# MAGIC     s2.avg_grid                                                     AS driver2_avg_grid,
# MAGIC     s1.races                                                        AS driver1_races,
# MAGIC     s2.races                                                        AS driver2_races,
# MAGIC     COALESCE(h.driver1_ahead, 0)                                   AS driver1_races_ahead,
# MAGIC     COALESCE(h.driver2_ahead, 0)                                   AS driver2_races_ahead,
# MAGIC     CASE
# MAGIC         WHEN s1.total_points > s2.total_points THEN s1.driver_name
# MAGIC         WHEN s2.total_points > s1.total_points THEN s2.driver_name
# MAGIC         ELSE 'Tied'
# MAGIC     END                                                             AS points_winner,
# MAGIC     CASE
# MAGIC         WHEN COALESCE(h.driver1_ahead, 0) > COALESCE(h.driver2_ahead, 0) THEN s1.driver_name
# MAGIC         WHEN COALESCE(h.driver2_ahead, 0) > COALESCE(h.driver1_ahead, 0) THEN s2.driver_name
# MAGIC         ELSE 'Tied'
# MAGIC     END                                                             AS h2h_winner
# MAGIC FROM driver_season_stats s1
# MAGIC JOIN driver_season_stats s2
# MAGIC     ON  s1.season         = s2.season
# MAGIC     AND s1.constructor_id = s2.constructor_id
# MAGIC     AND s1.driver_id      < s2.driver_id
# MAGIC LEFT JOIN h2h_races h
# MAGIC     ON  s1.season         = h.season
# MAGIC     AND s1.constructor_id = h.constructor_id
# MAGIC     AND s1.driver_id      = h.driver1_id
# MAGIC     AND s2.driver_id      = h.driver2_id
# MAGIC WHERE s1.races >= 5
# MAGIC   AND s2.races >= 5
# MAGIC ORDER BY s1.season DESC, s1.team;

# COMMAND ----------

# DBTITLE 1,v_teammate_h2h_long
# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW formula1.gold.v_teammate_h2h_long AS
# MAGIC SELECT
# MAGIC     season, team,
# MAGIC     driver1             AS driver,
# MAGIC     driver1_points      AS points,
# MAGIC     driver1_wins        AS wins,
# MAGIC     driver1_podiums     AS podiums,
# MAGIC     driver1_races_ahead AS races_ahead,
# MAGIC     driver1_avg_finish  AS avg_finish
# MAGIC FROM formula1.gold.v_teammate_h2h
# MAGIC UNION ALL
# MAGIC SELECT
# MAGIC     season, team,
# MAGIC     driver2             AS driver,
# MAGIC     driver2_points      AS points,
# MAGIC     driver2_wins        AS wins,
# MAGIC     driver2_podiums     AS podiums,
# MAGIC     driver2_races_ahead AS races_ahead,
# MAGIC     driver2_avg_finish  AS avg_finish
# MAGIC FROM formula1.gold.v_teammate_h2h
# MAGIC ORDER BY season DESC, team, driver;
