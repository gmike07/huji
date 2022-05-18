SELECT DISTINCT D.did
FROM Doctor D
WHERE 3 =   (SELECT COUNT(P.pid)
            FROM Patient P, Visit V
            WHERE V.did = D.did and V.pid = P.pid and P.bmi > 30)
ORDER BY did ASC;