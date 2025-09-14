view: opportunities {
  sql_table_name: opportunities ;;
  dimension: opp_id { primary_key: yes type: string sql: ${TABLE}.opp_id ;; }
  dimension: lead_id { type: string sql: ${TABLE}.lead_id ;; }
  dimension_group: created { type: time timeframes: [date, week, month] sql: ${TABLE}.created_at ;; }
  dimension_group: closed { type: time timeframes: [date, week, month] sql: ${TABLE}.closed_at ;; }
  measure: won_deals { type: count filters: [is_closed_won: '1'] }
  measure: total_amount { type: sum sql: ${TABLE}.amount ;; }
}