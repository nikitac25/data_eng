CREATE TABLE users (
    user_id INT PRIMARY KEY,
    age INT,
    gender VARCHAR(10),
    location_id INT,
    interests TEXT,
    signup_date DATE,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);