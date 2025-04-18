from config import TABLE_NAME
from database import Database

class ReminderManager():
    def __init__(self, database):
        self.db = database

    def get_all_users(self):
        query = f"select * from {TABLE_NAME}"
        return self.db.fetch_all(query)
    
    def add_user(self, chat_id, user_id, hour):
        query = f"insert into {TABLE_NAME} (chat_id, user_id, hour) values (?, ?, ?)"
        self.db.execute(query, (chat_id, user_id, hour))
        