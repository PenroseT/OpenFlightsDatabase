-- When WHERE is used instead of AND the condition eliminates all 
-- countries with no active airlines, effectively turning LEFT JOIN
-- into INNER JOIN

-- Query with WHERE condition
SELECT c.country_name,
COUNT(a.airline_id) AS active_airlines
	FROM countries c LEFT JOIN airlines a
		ON c.country_id = a.country_id
	WHERE a.active='Y'
GROUP BY c.country_name;

-- Query with INNER JOIN instead of a LEFT JOIN
SELECT c.country_name,
COUNT(a.airline_id) AS active_airlines
	FROM countries c INNER JOIN airlines a
		ON c.country_id = a.country_id AND a.active='Y'
GROUP BY c.country_name;


