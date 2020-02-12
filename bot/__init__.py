import pickle
import os
import threading


class Saver:
    folder = "./saves/"
    filename = None
    _data = None
    delay = 1.0

    def __init__(self):
        self.filename = self.folder + self.filename
        self.upload()
        self.timer = self.get_save_timer()

    def get_save_timer(self):
        return threading.Timer(self.delay, self.save)

    def start_save_timer(self):
        if not self.timer.is_alive():
            if self.delay <= 0:
                self.save()
            else:
                self.timer = self.get_save_timer()
                self.timer.start()

    def save(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        with open(self.filename, "wb") as file:
            pickle.dump(self._data, file)

    def upload(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        try:
            with open(self.filename, "rb") as file:
                self._data = pickle.load(file)
        except FileNotFoundError:
            self._data = {}

    def __del__(self):
        self.save()


class SaverDict(Saver):

    _data = {}

    def __delitem__(self, key):
        self._data.pop(key)
        self.start_save_timer()

    def __init__(self):
        super().__init__()

    def __iter__(self):
        return iter(self._data.keys())

    def __setitem__(self, key, value):
        self._data[key] = value
        self.start_save_timer()

    def __getitem__(self, item):
        return self._data[item]

    def get(self, item, default=None):
        return self._data.get(item, default)

    def setdefault(self, item, default):
        self.start_save_timer()
        return self._data.setdefault(item, default)


class UserTaskSaver(SaverDict):
    """ implemented like a singleton """

    filename = "user_tasks.save"
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


class UserStepSaver(SaverDict):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        super().__init__()
