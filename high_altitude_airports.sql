-- Lists the airport located at 1000m and above
-- In the table altitudes are listed in feets.
-- We use the conversion 1m=0.3048ft.

SELECT a.country, a.airport_name, CONCAT(a.altitude*0.3048, ' m') AS altitude_m
	FROM airports a
WHERE a.altitude>=1000/0.3048
ORDER BY a.altitude DESC; -- Sorts in descending order
