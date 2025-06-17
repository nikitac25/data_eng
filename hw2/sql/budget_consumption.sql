SELECT
    campaigns.campaign_id,
    campaigns.campaign_name,
    campaigns.budget,
    campaigns.remaining_budget,
    ROUND((campaigns.budget - campaigns.remaining_budget), 2) AS spent_amount,
    ROUND(((campaigns.budget - campaigns.remaining_budget) / campaigns.budget) * 100, 2) AS percent_spent
FROM campaigns
WHERE (campaigns.budget - campaigns.remaining_budget) / campaigns.budget > 0.8
ORDER BY percent_spent DESC
