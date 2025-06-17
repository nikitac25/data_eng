  WITH impressions_per_campaign AS (
    SELECT
        campaign_id,
        COUNT(*) AS total_impressions
    FROM impressions
    WHERE timestamp BETWEEN '2024-11-01' AND '2024-11-30'
    GROUP BY campaign_id
),
clicks_per_campaign AS (
    SELECT
        campaign_id,
        COUNT(*) AS total_clicks
    FROM clicks
    WHERE click_timestamp BETWEEN '2024-11-01' AND '2024-11-30'
    GROUP BY campaign_id
)
SELECT
    campaigns.campaign_id,
    campaigns.campaign_name,
    clicks_per_campaign.total_clicks AS total_clicks,
    impressions_per_campaign.total_impressions AS total_impressions,
    ROUND(
        clicks_per_campaign.total_clicks / 
        NULLIF(impressions_per_campaign.total_impressions, 0) * 100, 
    2) AS ctr_percentage
FROM campaigns
INNER JOIN impressions_per_campaign 
	ON campaigns.campaign_id = impressions_per_campaign.campaign_id
LEFT JOIN clicks_per_campaign 
	ON campaigns.campaign_id = clicks_per_campaign.campaign_id
ORDER BY ctr_percentage DESC
LIMIT 5;
