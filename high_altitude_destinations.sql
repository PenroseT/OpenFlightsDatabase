-- Select the routes with destinations above 1000m

SELECT src.airport_name, dst.airport_name, CONCAT(dst.altitude*0.3048, ' m') as altitude_m
	FROM routes r
		INNER JOIN airports src ON r.source_airport_id = src.airport_id
		INNER JOIN airports dst ON r.destination_airport_id = dst.airport_id
WHERE dst.altitude>=1000/0.3048
ORDER BY dst.altitude; -- Ascending order
