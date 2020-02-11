import telebot
from bot_trainer.settings import TOKEN


class TeleBot(telebot.TeleBot):
    def process_new_messages(self, new_messages):
        self._notify_next_handlers(new_messages)
        self._notify_reply_handlers(new_messages)
        self._notify_command_handlers(self.message_handlers, new_messages)
        self.__notify_update(new_messages)


bot = TeleBot(TOKEN, threaded=False)

