view: product_events {
  sql_table_name: product_events ;;
  dimension: event_id { primary_key: yes type: string sql: ${TABLE}.event_id ;; }
  dimension: lead_id { type: string sql: ${TABLE}.lead_id ;; }
  dimension: event_type { type: string sql: ${TABLE}.event_type ;; }
  dimension_group: ts { type: time timeframes: [time, date, week, month] sql: ${TABLE}.ts ;; }
}