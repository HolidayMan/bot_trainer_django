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
            pickle.dump(self._user_task, file)

    def upload(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        try:
            with open(self.filename, "rb") as file:
                self._data = pickle.load(self.filename)
        except FileNotFoundError:
            self._data = {}

    def __del__(self):
        self.save()


class UserTaskSaver(Saver):
    filename = "user_tasks.save"
    _user_task = {}
    data = _user_task

    def __init__(self):
        super().__init__()

    def __iter__(self):
        return iter(self._user_task.values())

    def __setitem__(self, key, value):
        self._user_task[key] = value

    def __getitem__(self, item):
        return self._user_task[item]

    def get(self, item, default=None):
        return self._user_task.get(item, default)

    def setdefault(self, item, default):
        return self._user_task.setdefault(item, default)
