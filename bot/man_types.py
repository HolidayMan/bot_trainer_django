import datetime
from telebot import types
from bot.bot import bot

from .types import ReceiveMessageStep, Step, SendMessageStep
from .savers import SaverDict
from .models import Project, TgUser, Goal, Performer, Task


class MessageBuilder:
    def __init__(self, message_saver):
        self.saver = message_saver

    def build_message(self, user_id):
        user_messages = self.saver[user_id]
        return "\n".join(user_messages)

    def add_message(self, user_id, message):
        self.saver.setdefault(user_id, []).append(message)

    def get_unbuilt_message(self, user_id):
        return self.saver[user_id]

    def clear_message(self, user_id):
        self.saver[user_id] = []


class MessageSaver(SaverDict):

    def __init__(self, filename):
        self.filename = filename
        super().__init__()


class UserProjectSaver(SaverDict):
    filename = "user_projectid.save"

    object = None

    def __new__(cls, *args, **kwargs):
        if cls.object:
            return cls.object
        else:
            obj = super().__new__(cls, *args, *kwargs)
            obj.__init__()
            cls.object = obj
            return cls.object

    def __init__(self):
        if self.object:
            self._data = self.object._data
            self.timer = self.get_save_timer()
        else:
            super().__init__()


class UserNewTaskSaver(SaverDict):
    filename = "user_newtask.save"

    object = None

    def __new__(cls, *args, **kwargs):
        if cls.object:
            return cls.object
        else:
            obj = super().__new__(cls, *args, *kwargs)
            obj.__init__()
            cls.object = obj
            return cls.object

    def __init__(self):
        if self.object:
            self._data = self.object._data
            self.timer = self.get_save_timer()
        else:
            super().__init__()


class ReceiveSaveMessageStep(ReceiveMessageStep):
    action = "receive_and_save_message"
    is_blocking = True

    def __init__(self, *args):
        super().__init__(*args)
        filename = f"{self.task.title}_received_messages.save"
        self.message_builder = MessageBuilder(MessageSaver(filename))

    def do_step(self, user_id, message, *args, **kwargs):
        if super().do_step(user_id, message):
            messages = self.message_builder.get_unbuilt_message(user_id)
            self.message_builder.clear_message(user_id)
            return messages
        else:
            self.message_builder.add_message(user_id, message)


class SaveProjectStep(Step):
    action = "save_project"

    @classmethod
    def de_json(cls, json_type, *args, **kwargs):
        return cls(*args, **kwargs)

    def do_step(self, user_id, messages: list, *args, **kwargs):
        user = TgUser.objects.get(tg_id=user_id)
        title, manager_name, goal, date_end = messages  # TODO: checking for messages length
        date = datetime.datetime.strptime(date_end, "%d.%m.%Y").date()  # TODO: checking for valid date
        new_project = Project()
        new_project.title = title
        new_project.manager_name = manager_name
        new_project.goal = goal
        new_project.date_end = date
        new_project.user = user
        new_project.save()
        UserProjectSaver()[user_id] = new_project.id
        super()._next_step(user_id)


class SaveGoalsStep(Step):
    action = "save_goals"

    @classmethod
    def de_json(cls, json_type, *args, **kwargs):
        return cls(*args, **kwargs)

    def do_step(self, user_id, messages: list, *args, **kwargs):
        project = Project.objects.get(id=UserProjectSaver()[user_id])
        goals = [Goal.objects.create(title=title, project=project) for title in messages]
        project.goals.add(*goals)
        project.save()
        super()._next_step(user_id)


class SavePerformersStep(Step):
    action = "save_performers"

    @classmethod
    def de_json(cls, json_type, *args, **kwargs):
        return cls(*args, **kwargs)

    @staticmethod
    def parse_performer(text: str) -> tuple:
        name = text[:text.index(',')].strip()
        description = text[text.index(',')+1:].strip()
        return name, description

    def do_step(self, user_id, messages: list, *args, **kwargs):
        project = Project.objects.get(id=UserProjectSaver()[user_id])
        performers = [Performer.objects.create(name=name, description=description, user=project.user, project=project)
                      for name, description in map(SavePerformersStep.parse_performer, messages)]
        project.performers.add(*performers)
        project.save()
        super()._next_step(user_id)


class CreateTaskStep(Step):
    """ creates task and adds terms to it """
    action = "create_task_and_add_terms"
    is_blocking = True

    def __init__(self, title, *args):
        super().__init__(*args)
        self.title = title

    @classmethod
    def de_json(cls, json_type, *args):
        return cls(json_type["title"], *args)

    @staticmethod
    def parse_date(text: str):
        start, end = [datetime.datetime.strptime(date, "%d.%m.%Y").date() for date in text.split('-')]
        duration = end - start
        return start, duration.days

    def do_step(self, user_id, message, *args, **kwargs):
        project = Project.objects.get(id=UserProjectSaver()[user_id])
        date_start, duration = CreateTaskStep.parse_date(message)
        new_task = Task.objects.create(title=self.title,
                                       date_start=date_start,
                                       duration=duration,
                                       project=project)
        UserNewTaskSaver()[user_id] = new_task.id
        super()._next_step(user_id)


class SendMessageWithPerformers(SendMessageStep):
    action = "send_message_with_performers"

    @staticmethod
    def get_buttons(user_id):
        project = Project.objects.get(id=UserProjectSaver()[user_id])
        return [performer.name for performer in project.performers.all()]

    def send_message(self, user_id):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        keyboard.add(*SendMessageWithPerformers.get_buttons(user_id))

        message = bot.send_message(user_id, self.message_text, parse_mode="HTML", reply_markup=keyboard)
        return message


class AddPerformerToTaskStep(Step):
    action = "add_performer_to_task"
    is_blocking = True

    @staticmethod
    def get_performers(user_id, name):
        project = Project.objects.get(id=UserProjectSaver()[user_id])
        return project.performers.get(name=name)

    @classmethod
    def de_json(cls, json_type, *args, **kwargs):
        return cls(*args, **kwargs)

    def do_step(self, user_id, message, *args, **kwargs):
        task = Task.objects.get(id=UserNewTaskSaver()[user_id])
        task.performers.add(AddPerformerToTaskStep.get_performers(user_id, message))
        task.save()
        super()._next_step(user_id)
