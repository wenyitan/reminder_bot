from bot.database import Database
from bot.config import TABLE_NAME
db = Database()


# drop_table_query = f"DROP TABLE IF EXISTS {TABLE_NAME}"

# db.execute(drop_table_query)

create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    user_id TEXT PRIMARY KEY,
    chat_id TEXT NOT NULL,
    hour INTEGER NOT NULL
    );
"""

db.execute(create_table_query)
db.close()