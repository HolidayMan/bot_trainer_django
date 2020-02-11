from bot import UserTaskSaver
from .bot import bot
from .dialog_registration import TASKS_MANAGER


@bot.message_handler(commands=['start'])
def cmd_start(message):
    title = "Task1"
    user_tasks = UserTaskSaver()
    user_tasks[message.chat.id] = title
    task = TASKS_MANAGER.get_task(title)
    task.add_user(user_id=message.chat.id)
