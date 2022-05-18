SELECT DISTINCT dname
FROM Doctor D
WHERE D.specialty = 'pediatrician' and
      NOT EXISTS(SELECT P.pid
                FROM Patient P
                WHERE P.bmi > 30 and P.gender = 'M' and 
                  NOT EXISTS(
                    SELECT *
                    FROM Visit V
                    WHERE V.pid = P.pid and V.did = D.did)
                 )
ORDER BY dname ASC;