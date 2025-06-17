SELECT
    locations.name AS location_name,
    ROUND(SUM(impressions.ad_revenue), 2) AS total_revenue
FROM clicks
INNER JOIN impressions ON clicks.impression_id = impressions.id
INNER JOIN locations ON impressions.location_id = locations.id
GROUP BY locations.name
ORDER BY total_revenue DESC;
