/*
  Table stores click events associated with impressions.
  Clicks are isolated to simplify metrics calculations such as CTR.
  click_id is the PRIMARY KEY.
  impression_id is a FOREIGN KEY referencing impressions(id), ensuring only valid impressions are clicked.
 */
CREATE TABLE clicks (
    click_id INT PRIMARY KEY,
    impression_id INT NOT NULL,
    click_timestamp DATETIME,
    FOREIGN KEY (impression_id) REFERENCES impressions(id)
);
