import json
# from abc import ABC, abstractmethod
from .bot import bot


class JsonDeserializable:

    # @abstractmethod
    # @classmethod
    def de_json(self):
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
    def __init__(self, action=None, **kwargs):
        self.action = action
        for kwarg in kwargs:
            self.__dict__[kwarg] = kwargs[kwarg]


    @classmethod
    def de_json(cls, json_type):
        if not isinstance(json_type, dict):
            raise TypeError("json_type must be an instance of dict")

        return cls(**json_type)


class SendMessageStep(Step):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_handler()

    def register_handler(self):
        pass
