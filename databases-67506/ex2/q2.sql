SELECT DISTINCT P.pname
FROM Visit V, Doctor D, Patient P
WHERE V.fee = 0 and D.dname = 'Avi Cohen' and D.did = V.did and P.pid = V.pid
ORDER BY P.pname ASC;