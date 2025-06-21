-- Source of route count for airports

SELECT a.airport_name, a.longitude, a.latitude, COUNT(r.route_id) AS num_routes
	FROM routes r INNER JOIN airports a
	ON a.airport_id = r.source_airport_id
GROUP BY a.airport_name
ORDER BY num_routes;
