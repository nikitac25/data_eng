if ! command -v dos2unix >/dev/null 2>&1; then
  sudo apt-get update && sudo apt-get install -y dos2unix
fi

dos2unix .env 2>/dev/null

set -a
source .env
set +a

mkdir -p hw_1_db
cd hw_1_db || exit

docker run -d \
  --name mysql-db \
  -e MYSQL_ROOT_PASSWORD="$MYSQL_PASSWORD" \
  -e MYSQL_DATABASE="$MYSQL_DATABASE" \
  -p 3306:3306 \
  mysql:8.0

sleep 30

docker exec -i mysql-db mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" <<EOF
USE $MYSQL_DATABASE;

CREATE TABLE locations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE
);

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    age INT,
    gender VARCHAR(10),
    location_id INT,
    interests TEXT,
    signup_date DATE,
    FOREIGN KEY (location_id) REFERENCES locations(id)
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
    target_location_id INT,
    ad_slot_size VARCHAR(20),
    budget DECIMAL(12, 2),
    remaining_budget DECIMAL(12, 2),
    FOREIGN KEY (advertiser_id) REFERENCES advertisers(id),
    FOREIGN KEY (target_location_id) REFERENCES locations(id)
);

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

CREATE TABLE clicks (
    click_id INT PRIMARY KEY,
    campaign_id INT NOT NULL,
    user_id INT NOT NULL,
    impression_id INT NOT NULL,
    click_timestamp DATETIME,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (impression_id) REFERENCES impressions(id)
);

CREATE INDEX idx_impressions_campaign_timestamp ON impressions(campaign_id, timestamp);
CREATE INDEX idx_clicks_campaign_timestamp ON clicks(campaign_id, click_timestamp);
CREATE INDEX idx_campaigns_advertiser_id ON campaigns(advertiser_id);
EOF
