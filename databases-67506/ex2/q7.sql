SELECT DISTINCT D.did, MAX(V.fee), MIN(V.fee), AVG(V.fee)
FROM Doctor D, Visit V
WHERE D.did = V.did
GROUP BY D.did
ORDER BY did ASC;