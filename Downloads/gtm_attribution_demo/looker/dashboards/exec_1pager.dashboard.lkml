dashboard: exec_1pager {
  title: "GTM Exec 1-Pager"
  layout: tile
  element: velocity {
    title: "Avg Days to Close (Won)"
    query: {
      model: gtm
      explore: opportunities
      fields: [opportunities.closed_date, opportunities.won_deals]
      filters: [opportunities.is_closed_won: "yes"]
    }
    type: single_value
  }
  element: by_channel {
    title: "Attributed Revenue by Channel"
    query: { model: gtm explore: opportunities fields: [touch_attribution.channel, touch_attribution.attributed_revenue] }
    type: bar
  }
}