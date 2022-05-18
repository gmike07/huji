SELECT DISTINCT did
FROM (SELECT DISTINCT P.pid, P.bmi, V.did
                FROM Visit V, patient P
                WHERE V.pid = P.pid) D1
GROUP BY did
HAVING AVG(bmi) >= ALL(SELECT AVG(bmi)
                      FROM (SELECT DISTINCT P.pid, P.bmi, V.did
                            FROM Visit V, patient P
                            WHERE V.pid = P.pid) D2
                      GROUP BY D2.did)
ORDER BY did ASC;