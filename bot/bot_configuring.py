from .bot import bot
from bot import UserTaskSaver
from bot.dialog_registration import TASKS_MANAGER
from bot.types import StepWorker

def user_tasks_matches(messages):
    user_tasks = UserTaskSaver()
    for message in messages:
        user_id = message.chat.id
        if user_id in user_tasks:
            task_name = user_tasks[user_id]
            task = TASKS_MANAGER.get_task(task_name)
            StepWorker.do_steps(task, user_id, message.text)

bot.set_update_listener(user_tasks_matches)
