import telebot
from bot_trainer.settings import TOKEN
from bot import UserTaskSaver
import json

bot = telebot.TeleBot(TOKEN)

def user_tasks_matches(messages):
    user_tasks = UserTaskSaver()
    for message in messages:
        user_id = message.chat.id
        if user_id in user_tasks:
            task = user_tasks[user_id]

bot.set_update_listener(user_tasks_matches)