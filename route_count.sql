-- Count the number of routes starting from a specific airport

SELECT a.city, COUNT(r.route_id) AS num_routes
	FROM airports a INNER JOIN routes r
	ON r.source_airport_id = a.airport_id
GROUP BY a.city
ORDER BY num_routes;
