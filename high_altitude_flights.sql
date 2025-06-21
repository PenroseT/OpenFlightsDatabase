-- Lists the flights where both the source and the
-- destination airports are above 1000m

SELECT src.airport_name, dst.airport_name,
	   CONCAT(src.altitude*0.3048, ' m'), CONCAT(dst.altitude*0.3048, ' m')
FROM routes r 
	 INNER JOIN airports src ON src.airport_id = r.source_airport_id
	 INNER JOIN airports dst ON dst.airport_id = r.destination_airport_id
WHERE src.altitude >= 1000/0.3048
  AND dst.altitude >= 1000/0.3048
ORDER BY ABS(dst.altitude-src.altitude); -- Ascending order of altitude difference
