-- The number of airlines, active or inactive, by country

SELECT c.country_name, COUNT(a.airline_id) AS num_airlines
	FROM countries c LEFT JOIN airlines a
		ON c.country_id = a.country_id
GROUP BY c.country_name;

	
