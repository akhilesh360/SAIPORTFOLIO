view: stage_history {
  sql_table_name: stage_history ;;
  dimension: opp_id { type: string sql: ${TABLE}.opp_id ;; }
  dimension: stage { type: string sql: ${TABLE}.stage ;; }
  dimension_group: ts { type: time timeframes: [time, date, week, month] sql: ${TABLE}.ts ;; }
}