-- Table stores demographic and interest data. user_id is the primary key for connecting user activity across impressions and clicks.

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    age INT,
    gender VARCHAR(10),
    location VARCHAR(100),
    interests TEXT,
    signup_date DATE
);
