import telebot
from config import BOT_TOKEN
from apscheduler.schedulers.background import BackgroundScheduler
from database import Database
from reminder_manager import ReminderManager
from telebot.util import quick_markup
from datetime import datetime 
import telebot.types as types

bot = telebot.TeleBot(BOT_TOKEN)
db = Database()
rm = ReminderManager(db)

@bot.message_handler(commands=['start'])
def start(message):
    from_user = message.from_user
    chat = message.chat
    all_reminders = rm.get_all_reminders()
    all_reminders_id = [int(reminder["user_id"]) for reminder in all_reminders]
    print(all_reminders)
    if from_user.id not in all_reminders_id:
        markup = quick_markup({
            f"{i}:00hrs" if len(str(i)) > 1 else f"0{i}:00hrs": {"callback_data": str(i)} for i in range(24)
        }, row_width=2)
        sent_message = bot.send_message(chat.id, text=f"Hello {from_user.first_name}! When would you like to be reminded?", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("At what time did I want to be reminded?")
        markup.add("I want to change the time I am reminded.")
        sent_message = bot.send_message(chat.id, text=f"Hello {from_user.first_name}! How can I help you? **This feature is still being built**", reply_markup=markup)
        bot.register_next_step_handler(sent_message, handle_idle_choice)
        ## if the user is not new and has already a record, then show list of options to show what they can do - for now only change hour to be reminded.

def handle_idle_choice(message):
    router = {
        "At what time did I want to be reminded?": check_reminder_time,
        "I want to change the time I am reminded.": change_reminder_time
    }
    router[message.text](message)

def check_reminder_time(message):
    print(message.from_user.id)
    reminder = rm.get_reminder_by_id(message.from_user.id)
    hour = reminder['hour']
    sent_message = bot.send_message(message.chat.id, text=f"You wanted to be reminded at {hour}00 hrs!")
    pass

def change_reminder_time():
    print("Placeholder for change reminder time")
    pass

@bot.callback_query_handler(func=lambda call: int(call.data) in range(24))
def log_reminder_input(callback):
    message = callback.message
    chat = message.chat
    from_user = callback.from_user
    to_edit_id = message.id
    to_edit_chat_id = message.chat.id
    user_id = from_user.id
    chat_id = chat.id
    rm.add_reminder(chat_id=chat_id, user_id=user_id, hour=int(callback.data))
    markup = quick_markup({})
    bot.edit_message_reply_markup(chat_id=to_edit_chat_id, message_id=to_edit_id, reply_markup=markup)
    text = f"OK you will be reminded daily at {callback.data if len(callback.data) > 1 else '0'+callback.data}00hrs!"
    sent_message = bot.send_message(chat.id, text=text)
    bot.register_next_step_handler(sent_message, start)

def remind():
    now = datetime.now().hour
    print(f"Sending reminders now at {now}00hrs...")
    all_users = rm.get_all_reminders()
    to_remind = [user for user in all_users if user['hour'] == now]
    for user in to_remind:
        bot.send_message(user["chat_id"], text="Reminder to do your quiet time!!")
        
if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(remind, "cron", hour="*")
    scheduler.start()
    bot.infinity_polling()