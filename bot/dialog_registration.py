# import json
# from abc import ABC, abstractmethod
from telebot import types
from .bot import bot


class JsonDeserializable:

    # @abstractmethod
    @classmethod
    def de_json(cls, json_type):
        raise NotImplementedError


class Task(JsonDeserializable):
    objects = {}

    def __init__(self, title, condition, number, steps):
        self.title = title
        self.condition = condition
        self.number = number
        self.steps = steps
        self.objects.setdefault(title, self)

    @classmethod
    def de_json(cls, json_type):
        if not isinstance(json_type, dict):
            raise TypeError("json_type must be an instance of dict")

        return cls(json_type['title'],
                   json_type['condition'],
                   json_type['number'],
                   json_type['steps'],
                   )


class Step(JsonDeserializable):
    action = None

    @classmethod
    def de_json(cls, json_type):
        if not isinstance(json_type, dict):
            raise TypeError("json_type must be an instance of dict")

        raise NotImplementedError

    def do_step(self):
        pass


class SendMessageStep(Step):
    """ implements send_message action """

    action = "send_message"

    def __init__(self, message_text, buttons=None):
        self.message_text = message_text
        self.buttons = buttons

    @classmethod
    def de_json(cls, json_type):
        if not isinstance(json_type, dict):
            raise TypeError("json_type must be an instance of dict")

        return cls(json_type["message_text"],
                   json_type.get("buttons")
                   )

    def send_message(self, user_id):
        if self.buttons:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            keyboard.add(*self.buttons)
        else:
            keyboard = types.ReplyKeyboardRemove()

        message = bot.send_message(user_id, self.message_text, parse_mode="HTML", reply_markup=keyboard)
        return message

    # def do_step(self):


class ReceiveMessageStep(Step):
    """ implements receive_message action """

    action = "receive_message"

    def __init__(self, text_to_equal):
        self.text_to_equal = text_to_equal

    @classmethod
    def de_json(cls, json_type):
        if not isinstance(json_type, dict):
            raise TypeError("json_type must be an instance of dict")

        return cls(json_type["text_to_equal"])
