DROP VIEW IF EXISTS v_stage_conversion;
CREATE VIEW v_stage_conversion AS
WITH b AS (SELECT stage, COUNT(*) cnt FROM opportunities GROUP BY stage)
SELECT 'Prospecting→Closed Won' path,
       (SELECT IFNULL(SUM(is_closed_won),0) FROM opportunities)*1.0/(SELECT IFNULL(COUNT(*),1) FROM opportunities) rate;

DROP VIEW IF EXISTS v_velocity;
CREATE VIEW v_velocity AS
SELECT AVG(julianday(closed_at) - julianday(created_at)) AS avg_days_to_close
FROM opportunities WHERE is_closed_won=1;

DROP VIEW IF EXISTS v_sla_buckets;
CREATE VIEW v_sla_buckets AS
SELECT CASE
         WHEN first_response_minutes <= 60 THEN '<= 1h'
         WHEN first_response_minutes <= 240 THEN '1-4h'
         WHEN first_response_minutes <= 1440 THEN '4-24h'
         ELSE '> 24h' END AS sla_bucket,
       COUNT(*) AS leads
FROM leads GROUP BY 1;

DROP VIEW IF EXISTS v_attrib_by_channel;
CREATE VIEW v_attrib_by_channel AS
SELECT model, channel, SUM(amount) AS attributed_revenue
FROM touch_attribution GROUP BY model, channel;

DROP VIEW IF EXISTS v_attrib_by_campaign;
CREATE VIEW v_attrib_by_campaign AS
SELECT model, campaign, SUM(amount) AS attributed_revenue
FROM touch_attribution GROUP BY model, campaign;


-- Stage-to-stage conversion rates based on stage_history timelines
DROP VIEW IF EXISTS v_stage_conversion_full;
CREATE VIEW v_stage_conversion_full AS
WITH stages AS (
  SELECT DISTINCT stage FROM stage_history
),
pairs AS (
  SELECT 'Prospecting' AS from_stage, 'Qualification' AS to_stage UNION ALL
  SELECT 'Qualification','Proposal' UNION ALL
  SELECT 'Proposal','Negotiation' UNION ALL
  SELECT 'Negotiation','Closed Won'
),
base AS (
  SELECT p.from_stage, p.to_stage, sh1.opp_id
  FROM pairs p
  JOIN stage_history sh1 ON sh1.stage = p.from_stage
  JOIN stage_history sh2 ON sh2.opp_id = sh1.opp_id AND sh2.stage = p.to_stage AND sh2.ts > sh1.ts
  GROUP BY p.from_stage, p.to_stage, sh1.opp_id
),
denoms AS (
  SELECT from_stage, COUNT(DISTINCT opp_id) AS denom
  FROM (
    SELECT 'Prospecting' AS from_stage, opp_id FROM stage_history WHERE stage='Prospecting'
    UNION ALL SELECT 'Qualification', opp_id FROM stage_history WHERE stage='Qualification'
    UNION ALL SELECT 'Proposal', opp_id FROM stage_history WHERE stage='Proposal'
    UNION ALL SELECT 'Negotiation', opp_id FROM stage_history WHERE stage='Negotiation'
  )
  GROUP BY from_stage
)
SELECT b.from_stage || '→' || b.to_stage AS path,
       COUNT(DISTINCT b.opp_id) * 1.0 / d.denom AS conversion_rate,
       d.denom AS at_stage,
       COUNT(DISTINCT b.opp_id) AS progressed
FROM base b
JOIN denoms d ON d.from_stage = b.from_stage
GROUP BY path;
