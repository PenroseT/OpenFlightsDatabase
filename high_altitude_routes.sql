-- Shows the routes where both the source and the destination
-- airport are at an altitude above 1000m

SELECT sc.source_airport_name, dc.destination_airport_name
	FROM routes sc INNER JOIN routes dc
WHERE 
