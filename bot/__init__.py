import pickle
import os


class Saver:
    folder = "./saves/"
    filename = None
    _data = None

    def __init__(self):
        self.filename = self.folder + self.filename
        self.upload()

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

    def __delitem__(self, key):
        self._data.pop(key)

    def __del__(self):
        self.save()


class SaverDict(Saver):

    _data = {}

    def __init__(self):
        super().__init__()

    def __iter__(self):
        return iter(self._data.keys())

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, item):
        return self._data[item]

    def get(self, item, default=None):
        return self._data.get(item, default)

    def setdefault(self, item, default):
        return self._data.setdefault(item, default)


class UserTaskSaver(SaverDict):
    """ implemented like a singleton """

    filename = "user_tasks.save"
    object = None

    def __new__(cls, *args, **kwargs):
        if cls.object:
            return cls.object
        else:
            object = super().__new__(cls, *args, *kwargs)
            # object.__init__()
            cls.object = object
            return cls.object

    def __init__(self):
        if self.object:
            self._data = self.object._data
        else:
            super().__init__()


class UserStepSaver(SaverDict):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        super().__init__()
