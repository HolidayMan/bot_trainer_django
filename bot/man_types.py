import datetime

from .types import ReceiveMessageStep, Step
from .savers import SaverDict
from .models import Project, TgUser


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
        title, manager_name, goal, date_end = messages
        date = datetime.datetime.strptime(date_end, "%d.%m.%Y").date()
        new_project = Project()
        new_project.title = title
        new_project.manager_name = manager_name
        new_project.goal = goal
        new_project.date_end = date
        new_project.user = user
        new_project.save()
        super()._next_step(user_id)

