SELECT
    adv.id AS advertiser_id,
    adv.name AS advertiser_name,
    ROUND(SUM(imp.ad_cost), 2) AS total_spent
FROM advertisers adv
INNER JOIN campaigns camp 
	ON adv.id = camp.advertiser_id
INNER JOIN 
	impressions imp ON camp.campaign_id = imp.campaign_id
WHERE imp.timestamp BETWEEN '2024-11-01' AND '2024-11-30'
GROUP BY adv.id, adv.name
ORDER BY total_spent DESC;
