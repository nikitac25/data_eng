

CREATE TABLE campaigns (
    campaign_id INT PRIMARY KEY,
    advertiser_id INT NOT NULL,
    campaign_name VARCHAR(100),
    campaign_start_date DATE,
    campaign_end_date DATE,
    target_age_range VARCHAR(20),
    target_interest VARCHAR(100),
    target_location VARCHAR(100),
    ad_slot_size VARCHAR(20),
    budget DECIMAL(12, 2),
    remaining_budget DECIMAL(12, 2),
    FOREIGN KEY (advertiser_id) REFERENCES advertisers(id)
);
