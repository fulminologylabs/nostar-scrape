from alembic import op
from sqlalchemy import text

def sql_fetch_all(sql: str) -> list:
    conn = op.get_bind()
    cursor = conn.execute(text(sql))
    # Fetchall
    return cursor.fetchall()

def sql_fetch_one(sql: str) -> tuple:
    conn = op.get_bind()
    cursor = conn.execute(text(sql))
    # Fetchone
    return cursor.fetchone()
