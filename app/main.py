import os
from typing import Literal

import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Module 9 FastAPI Calculator", version="1.0.0")

DATABASE_URL = os.getenv("DATABASE_URL")



class CalculationInput(BaseModel):
    user_id: int = Field(gt=0)
    operation: Literal["add", "subtract", "multiply", "divide", "power"]
    operand_a: float
    operand_b: float


@app.get("/")
def home():
    return {"message": "Module 9 FastAPI Calculator is running", "docs": "/docs"}


@app.get("/health")
def health():
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"app": "running", "database": "connected"}
    except psycopg.Error:
        raise HTTPException(status_code=503, detail="Database connection unavailable")


@app.get("/users")
def get_users():
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, username, email, created_at FROM users ORDER BY id")
                return cur.fetchall()
    except psycopg.errors.UndefinedTable:
        raise HTTPException(status_code=404, detail="Run sql/01_create_tables.sql first")


@app.get("/calculations")
def get_calculations():
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT c.id, u.username, c.operation, c.operand_a,
                           c.operand_b, c.result, c.timestamp
                    FROM calculations AS c
                    JOIN users AS u ON u.id = c.user_id
                    ORDER BY c.id
                """)
                return cur.fetchall()
    except psycopg.errors.UndefinedTable:
        raise HTTPException(status_code=404, detail="Run sql/01_create_tables.sql first")


@app.post("/calculate", status_code=201)
def calculate(data: CalculationInput):
    a, b = data.operand_a, data.operand_b
    if data.operation == "add":
        result = a + b
    elif data.operation == "subtract":
        result = a - b
    elif data.operation == "multiply":
        result = a * b
    elif data.operation == "divide":
        if b == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        result = a / b
    else:
        result = a ** b

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO calculations
                        (operation, operand_a, operand_b, result, user_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, operation, operand_a, operand_b, result, user_id
                    """,
                    (data.operation, a, b, result, data.user_id),
                )
                return cur.fetchone()
    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(status_code=404, detail="That user_id does not exist")
    except psycopg.errors.UndefinedTable:
        raise HTTPException(status_code=404, detail="Create tables in pgAdmin first")
