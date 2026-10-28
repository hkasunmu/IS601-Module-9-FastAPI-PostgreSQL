-- (E) Delete record id 2 (run AFTER the update screenshot).
DELETE FROM calculations
WHERE id = 2;

-- Run this SELECT separately afterward to verify id 2 is gone.
SELECT * FROM calculations ORDER BY id;
