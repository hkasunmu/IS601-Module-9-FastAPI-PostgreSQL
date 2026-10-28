-- (C1) Select this statement alone in Query Tool, then press Execute.
SELECT * FROM users;

-- (C2) Select this statement alone, then press Execute.
SELECT * FROM calculations;

-- (C3) Select this statement alone, then press Execute.
SELECT u.username, c.operation, c.operand_a, c.operand_b, c.result
FROM calculations c
JOIN users u ON c.user_id = u.id;
