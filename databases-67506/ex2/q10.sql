DELETE FROM Patient WHERE pid IN (SELECT P.pid
                                  FROM Patient P
                                  EXCEPT
                                  SELECT V.pid
                                  FROM Visit V);