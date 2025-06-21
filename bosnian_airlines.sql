-- List of all Bosnian airlines, active and defunct

SELECT a.country, a.airline_name FROM airlines a
	WHERE a.country = "Bosnia and Herzegovina";
