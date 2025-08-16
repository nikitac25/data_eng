CREATE TABLE impressions (
    id INT PRIMARY KEY,
    campaign_id INT NOT NULL,
    user_id INT NOT NULL,
    device VARCHAR(50),
    location_id INT,
    timestamp DATETIME,
    bid_amount DECIMAL(10, 2),
    ad_cost DECIMAL(10, 2),
    ad_revenue DECIMAL(10, 2),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE INDEX idx_impressions_campaign_timestamp ON impressions(campaign_id, timestamp);