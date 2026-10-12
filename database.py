import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT,
                amount REAL,
                category TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def add_transaction(user_id: int, type_: str, amount: float, category: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO transactions (user_id, type, amount, category) VALUES (?, ?, ?, ?)",
            (user_id, type_, amount, category)
        )
        await db.commit()
      
