/*Table stores  impressions events with metadata and financial metrics. 
Removed redundant rows from original ad_events datasource.
Provided foreign keys for joining with campains, users
*/
CREATE TABLE impressions (
    id INT PRIMARY KEY,
    campaign_id INT NOT NULL,
    user_id INT NOT NULL,
    device VARCHAR(50),
    user_location VARCHAR(100),
    timestamp DATETIME,
    bid_amount DECIMAL(10, 2),
    ad_cost DECIMAL(10, 2),
    ad_revenue DECIMAL(10, 2),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
