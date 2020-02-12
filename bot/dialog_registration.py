import os

from bot_trainer.settings import TASKS_DIR
from .types import TaskManager


def get_task_files(folder):
    return (os.path.join(folder, dir) for dir in os.listdir(folder))


TASKS_MANAGER = TaskManager()
for filename in get_task_files(TASKS_DIR):
    TASKS_MANAGER.from_file(filename)
