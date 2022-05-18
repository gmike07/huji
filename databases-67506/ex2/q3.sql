SELECT DISTINCT P.pid, P.pname
FROM Visit V, Doctor D, Patient P
WHERE D.did = V.did and P.pid = V.pid and D.specialty = 'orthopedist'
INTERSECT
SELECT DISTINCT P.pid, P.pname
FROM Visit V, Doctor D, Patient P
WHERE D.did = V.did and P.pid = V.pid and D.specialty = 'pediatrician'
ORDER BY pid ASC;