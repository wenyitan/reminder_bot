import sqlite3
from config import TABLE_NAME

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

class Database:
    def __init__(self, db_path="/app/bot/reminders.db"):
        self.db_path=db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = dict_factory
        return conn

    def execute(self, query, values=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values or ())
            conn.commit()

    def fetch_all(self, query, values=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values or ())
            return cursor.fetchall()
    
    def fetch_one(self, query, values=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values or ())
            return cursor.fetchone()

    def init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                user_id TEXT PRIMARY KEY,
                chat_id TEXT NOT NULL,
                hour INTEGER NOT NULL
                );
            """
            cursor.execute(create_table_query)
            conn.commit()