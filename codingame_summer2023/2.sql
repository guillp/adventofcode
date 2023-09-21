SELECT a.name, count(*)
FROM mutant m
JOIN agent a
ON a.agentId = m.recruiterId
GROUP BY a.agentId, a.name
ORDER BY count(*) DESC
LIMIT 10;