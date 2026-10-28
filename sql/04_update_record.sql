-- (D) Update record id 1 (run AFTER your initial SELECT screenshots).
UPDATE calculations
SET result = 6
WHERE id = 1;

-- Run this SELECT separately afterward to show the new value.
SELECT * FROM calculations WHERE id = 1;
