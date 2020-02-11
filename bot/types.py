import json
from typing import Union

from telebot import types

from .bot import bot
from bot import UserStepSaver, UserTaskSaver

BLOCKING_ACTIONS = ("receive_message")

class JsonDeserializable:
    @classmethod
    def de_json(cls, json_type):
        raise NotImplementedError


class StepsDict(dict):
    ...


class StepWorker:
    @staticmethod
    def do_steps(task, user_id, *args, **kwargs):
        """ steps execution always start with blocking action """
        task.do_step(user_id, *args, **kwargs)
        step = task.steps[task.saver[user_id]]
        while step.action not in BLOCKING_ACTIONS:
            task.do_step(user_id, *args, **kwargs)
            try:
                step = task.steps[task.saver[user_id]]
            except KeyError:
                task.end_task(user_id)
                break
        if task.saver[user_id] == "ended":
            user_task = UserTaskSaver()
            del user_task[user_id]


class Task(JsonDeserializable):
    def __init__(self, title: str, condition: str, number: int, steps: Union[StepsDict, dict, None]) -> None:
        self.title = title
        self.condition = condition
        self.number = number

        if isinstance(steps, StepsDict):
            self.steps = steps
        elif isinstance(steps, dict):
            self.steps = TaskManager.parse_steps(self.title, steps)

        self.saver = UserStepSaver(f"{self.title}.save")

    def add_user(self, user_id):
        # self.saver.setdefault(user_id, 1)
        self.saver[user_id] = 1

    @classmethod
    def de_json(cls, json_type):
        if not isinstance(json_type, dict):
            raise TypeError("json_type must be an instance of dict")

        return cls(json_type['title'],
                   json_type['condition'],
                   json_type['number'],
                   json_type['steps'],
                   )

    def do_step(self, user_id, *args, **kwargs):
        step_number = self.saver[user_id]
        step = self.steps[step_number]

        step.do_step(user_id, *args, **kwargs)

    def end_task(self, user_id):
        self.saver[user_id] = "ended"


class Step(JsonDeserializable):
    action = None

    def __init__(self, task, number):
        self.task = TaskManager.tasks[task]
        self.number = number

    @classmethod
    def de_json(cls, json_type):
        # if not isinstance(json_type, dict):
        #     raise TypeError("json_type must be an instance of dict")

        raise NotImplementedError

    def _next_step(self, user_id):
        self.task.saver[user_id] += 1

    def do_step(self, *args, **kwargs):
        pass


class SendMessageStep(Step):
    """ implements send_message action """

    action = "send_message"

    def __init__(self, message_text, buttons=None, *args):
        super().__init__(*args)
        self.message_text = message_text
        self.buttons = buttons

    @classmethod
    def de_json(cls, json_type, *args):
        if not isinstance(json_type, dict):
            raise TypeError("json_type must be an instance of dict")

        return cls(json_type["message_text"],
                   json_type.get("buttons"),
                   *args
                   )

    def send_message(self, user_id):
        if self.buttons:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            keyboard.add(*self.buttons)
        else:
            keyboard = types.ReplyKeyboardRemove()

        message = bot.send_message(user_id, self.message_text, parse_mode="HTML", reply_markup=keyboard)
        return message

    def do_step(self, user_id, *args, **kwargs):
        """ sends message and moves user to the next step """
        message = self.send_message(user_id)
        self._next_step(user_id)
        return message


class ReceiveMessageStep(Step):
    """ implements receive_message action """

    action = "receive_message"

    def __init__(self, text_to_equal, *args):
        super().__init__(*args)
        self.text_to_equal = text_to_equal

    @classmethod
    def de_json(cls, json_type, *args):
        if not isinstance(json_type, dict):
            raise TypeError("json_type must be an instance of dict")

        return cls(json_type["text_to_equal"],
                   *args
                   )

    def do_step(self, user_id, message: types.Message) -> None:
        """ sends message and moves user to the next step """
        if message == self.text_to_equal:
            self._next_step(user_id)


class TaskManager:
    tasks = {}

    object = None

    def __new__(cls, *args, **kwargs):
        if cls.object:
            return cls.object
        else:
            cls.object = super().__new__(cls, *args, *kwargs)
            return cls.object

    @staticmethod
    def parse_json_file(json_file: str) -> dict:
        with open(json_file) as file:
            return json.load(file)

    @staticmethod
    def parse_steps(task: str, steps: dict) -> StepsDict:
        steps_dict = StepsDict({})
        for number, step in steps.items():
            action = step["action"]
            number = int(number)
            if action == "send_message":
                steps_dict[number] = SendMessageStep.de_json(step, task, number)
            elif action == "receive_message":
                steps_dict[number] = ReceiveMessageStep.de_json(step, task, number)

        return steps_dict

    def add_task(self, task_json: dict) -> Task:
        condition = task_json["condition"]
        number = task_json["number"]
        title = task_json["title"]

        task = Task(title, condition, number, None)
        # task = Task.de_json(task_json)
        self.tasks[title] = task
        steps = TaskManager.parse_steps(title, task_json["steps"])
        task.steps = steps
        return task

    def from_file(self, filename: str) -> Task:
        read_file = TaskManager.parse_json_file(filename)
        return self.add_task(read_file["task"])

    def get_task(self, task_name):
        return self.tasks[task_name]