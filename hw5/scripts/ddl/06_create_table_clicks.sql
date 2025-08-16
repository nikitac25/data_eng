CREATE TABLE IF NOT EXISTS clicks (
    click_id INT PRIMARY KEY,
    campaign_id INT NOT NULL,
    user_id INT NOT NULL,
    impression_id VARCHAR(100) NOT NULL,
    click_timestamp DATETIME,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (impression_id) REFERENCES impressions(id)
);

CREATE INDEX idx_clicks_campaign_timestamp ON clicks(campaign_id, click_timestamp);