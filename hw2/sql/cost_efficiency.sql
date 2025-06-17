SELECT
    impressions.campaign_id,
    campaigns.campaign_name,
    COUNT(impressions.id) AS total_impressions,
    COALESCE(click_summary.total_clicks, 0) AS total_clicks,
    ROUND(SUM(impressions.ad_cost), 2) AS total_cost,
    ROUND(SUM(impressions.ad_cost) / NULLIF(click_summary.total_clicks, 0), 2) AS cpc,
    ROUND((SUM(impressions.ad_cost) / NULLIF(COUNT(impressions.id), 0)) * 1000, 2) AS cpm
FROM impressions
LEFT JOIN (
    SELECT campaign_id, COUNT(click_id) AS total_clicks
    FROM clicks
    GROUP BY campaign_id
) AS click_summary
	ON impressions.campaign_id = click_summary.campaign_id
INNER JOIN campaigns 
	ON impressions.campaign_id = campaigns.campaign_id
WHERE impressions.timestamp BETWEEN '2024-11-01' AND '2024-11-30'
GROUP BY 1,2
ORDER BY cpc;
