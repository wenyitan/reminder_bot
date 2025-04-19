from config import TABLE_NAME

class ReminderManager():
    def __init__(self, database):
        self.db = database

    def get_all_reminders(self):
        query = f"select * from {TABLE_NAME}"
        return self.db.fetch_all(query)
    
    def get_all_reminders_by_hour(self, hour):
        query = f"select * from {TABLE_NAME} where hour=?"
        return self.db.fetch_all(query, (hour,))
    
    def add_reminder(self, chat_id, user_id, hour):
        query = f"insert into {TABLE_NAME} (chat_id, user_id, hour) values (?, ?, ?)"
        self.db.execute(query, (chat_id, user_id, hour))
        
    def get_reminder_by_id(self, user_id):
        query = f"select * from {TABLE_NAME} where user_id=?"
        return self.db.fetch_one(query, (str(user_id),))
    
    def change_reminder_hour_for_user(self, user_id, hour):
        query = f"update {TABLE_NAME} set hour=? where user_id=?"
        self.db.execute(query, (hour, user_id))