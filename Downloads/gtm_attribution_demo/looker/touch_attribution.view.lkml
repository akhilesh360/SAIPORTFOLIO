view: touch_attribution {
  sql_table_name: touch_attribution ;;
  dimension: opp_id { type: string sql: ${TABLE}.opp_id ;; }
  dimension: model { type: string sql: ${TABLE}.model ;; }
  dimension: channel { type: string sql: ${TABLE}.channel ;; }
  dimension: campaign { type: string sql: ${TABLE}.campaign ;; }
  measure: attributed_revenue { type: sum sql: ${TABLE}.amount ;; }
}