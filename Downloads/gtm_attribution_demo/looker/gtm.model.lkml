connection: 'YOUR_CONNECTION'

include: '*.view.lkml'
include: 'dashboards/*.dashboard.lkml'
explore: opportunities {
  joins: [touch_attribution] 
}