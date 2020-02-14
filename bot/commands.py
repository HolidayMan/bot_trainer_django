from .savers import UserTaskSaver
from .bot import bot
from .dialog_registration import TASKS_MANAGER
from .models import TgUser


def user_exists(message):
    return TgUser.objects.filter(tg_id=message.chat.id).exists()

def create_user_if_not_exist(message):
    if not user_exists(message):
        new_user = TgUser(tg_id=message.chat.id)
        if message.chat.username:
            new_user.username = message.chat.username
        if message.chat.first_name:
            new_user.first_name = message.chat.first_name
        new_user.save()
        return new_user


@bot.message_handler(commands=['start'])
def cmd_start(message):
    create_user_if_not_exist(message)
    title = "Task1"
    user_tasks = UserTaskSaver()
    user_tasks[message.chat.id] = title
    task = TASKS_MANAGER.get_task(title)
    task.add_user(user_id=message.chat.id)

@bot.message_handler(commands=["start_real"])
def cmd_start_real(message):
    create_user_if_not_exist(message)
    title = "Task2"
    user_tasks = UserTaskSaver()
    user_tasks[message.chat.id] = title
    task = TASKS_MANAGER.get_task(title)
    task.add_user(user_id=message.chat.id)