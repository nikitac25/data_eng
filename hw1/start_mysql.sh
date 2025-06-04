mkdir -p hw_1_db
cd hw_1_db || exit

docker run -d \
  --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=assessment_db \
  -p 3306:3306 \
  mysql:8.0

sleep 20


docker exec -i mysql-db mysql -uroot -prootpassword <<EOF
USE assessment_db;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    age INT,
    gender VARCHAR(10),
    location VARCHAR(100),
    interests TEXT,
    signup_date DATE
);

CREATE TABLE advertisers (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

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

CREATE TABLE clicks (
    click_id INT PRIMARY KEY,
    impression_id INT NOT NULL,
    click_timestamp DATETIME,
    FOREIGN KEY (impression_id) REFERENCES impressions(id)
);
EOF
