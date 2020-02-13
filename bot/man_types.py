from .types import ReceiveMessageStep
from .savers import SaverDict


class MessageBuilder:
    def __init__(self, message_saver):
        self.saver = message_saver

    def build_message(self, user_id):
        user_messages = self.saver[user_id]
        return "\n".join(user_messages)

    def add_message(self, user_id, message):
        self.saver.setdefault(user_id, []).append(message)

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
        next_step = self.task.steps[self.number+1]
        if super().do_step(user_id, message):
            built_message = self.message_builder.build_message(user_id)
            print(built_message)  # TODO: here must be saving to DB
            self.message_builder.clear_message(user_id)
            return built_message
        else:
            self.message_builder.add_message(user_id, message)
