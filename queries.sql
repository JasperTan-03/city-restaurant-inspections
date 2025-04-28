-- Cuisine Distributions
SELECT
  c.CuisineDescription,
  COUNT(*) AS NumRestaurants
FROM Restaurant r
JOIN Cuisine c ON r.CuisineID = c.CuisineID
GROUP BY c.CuisineDescription
ORDER BY NumRestaurants DESC;


-- Top 5 Violations
SELECT
  v.ViolationCode,
  v.ViolationDescription,
  COUNT(*) AS Occurrences
FROM Violation v
GROUP BY v.ViolationCode, v.ViolationDescription
ORDER BY Occurrences DESC
LIMIT 5;


-- Shows th average score for each borough
SELECT
  a.Borough,
  ROUND(AVG(i.Score),1) AS AvgScore,
  COUNT(i.InspectionID) AS TotalInspections
FROM Inspection i
JOIN Restaurant r ON i.RestaurantID = r.RestaurantID
JOIN Address   a ON r.AddressID     = a.AddressID
WHERE a.Borough IS NOT NULL
GROUP BY a.Borough
ORDER BY AvgScore DESC;

