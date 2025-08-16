CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id INT PRIMARY KEY,
    advertiser_id INT NOT NULL,
    campaign_name VARCHAR(100),
    campaign_start_date DATE,
    campaign_end_date DATE,
    target_age_range VARCHAR(20),
    target_interest VARCHAR(100),
    target_location_id INT,
    ad_slot_size VARCHAR(20),
    budget DECIMAL(12, 2),
    remaining_budget DECIMAL(12, 2),
    FOREIGN KEY (advertiser_id) REFERENCES advertisers(id),
    FOREIGN KEY (target_location_id) REFERENCES locations(id)
);

CREATE INDEX idx_campaigns_advertiser_id ON campaigns(advertiser_id);