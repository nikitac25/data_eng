SELECT
    users.user_id,
    users.age,
    users.gender,
    locations.name AS location_name,
    COUNT(clicks.click_id) AS total_clicks
FROM clicks
INNER JOIN users ON clicks.user_id = users.user_id
INNER JOIN locations ON users.location_id = locations.id
GROUP BY users.user_id, users.age, users.gender, locations.name
ORDER BY total_clicks DESC
LIMIT 10;

