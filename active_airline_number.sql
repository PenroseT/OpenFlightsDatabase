-- The number of active airlines by country
-- Note that the active column is unreliable

SELECT c.country_name, COUNT(a.airline_id) AS active_airlines
	FROM countries c LEFT JOIN airlines a
		ON c.country_id = a.country_id AND a.active = 'Y'
GROUP BY c.country_name;
