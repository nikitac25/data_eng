SELECT
    impressions.device,
    COUNT(DISTINCT impressions.id) AS total_impressions,
    COUNT(DISTINCT clicks.click_id) AS total_clicks,
    ROUND(
        (COUNT(DISTINCT clicks.click_id) / NULLIF(COUNT(DISTINCT impressions.id), 0)) * 100,
        2
    ) AS ctr_percentage
FROM impressions
LEFT JOIN clicks ON impressions.id = clicks.impression_id
GROUP BY impressions.device
ORDER BY ctr_percentage DESC
