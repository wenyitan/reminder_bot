from bot.database import Database

class ReminderManager():
    def __init__(self):
        self.db = Database()

    def get_all_reminders(self):
        results = self.db.collection.find({})
        return list(results)
    
    def get_all_reminders_by_hour(self, hour):
        results = self.db.collection.find({"hour": hour})
        return list(results)
    
    def add_reminder(self, chat_id, user_id, hour):
        self.db.collection.insert_one({
            "chat_id": str(chat_id),
            "user_id": str(user_id),
            "hour": hour,
            "pester": False,
            "acknowledge": True
        })
        
    def get_reminder_by_id(self, user_id):
        result = self.db.collection.find_one({"user_id": str(user_id)})
        return result
    
    def change_reminder_hour_for_user(self, user_id, hour):
        result = self.db.collection.update_one({"user_id": str(user_id)}, {"$set": {"hour": hour}})
        return result.modified_count

    def get_pester_by_id(self, user_id):
        return self.db.collection.find_one({"user_id": str(user_id)}, projection={"pester": 1})
        # query = f"select pester from {TABLE_NAME} where user_id=?"
        # return self.db.fetch_one(query, (str(user_id),))

    def set_pester_by_id(self, user_id, pester):
        result = self.db.collection.update_one({"user_id": str(user_id)}, {"$set": {"pester": pester}})
        return result.modified_count

    def set_acknowledge_by_id(self, user_id, acknowledge):
        result = self.db.collection.update_one({"user_id": str(user_id)}, {"$set": {"acknowledge": acknowledge}})
        return result.modified_count

    def get_acknowledge_by_id(self, user_id):
        return self.db.collection.find_one({"user_id": str(user_id)}, projection={"acknowledge": 1})
        # query = f"select acknowledge from {TABLE_NAME} where user_id=?"
        # return self.db.fetch_one(query, (str(user_id),))

    def get_all_reminder_by_acknowledge(self):
        results = self.db.collection.find({"acknowledge": False, "pester": True})
        return list(results)