import pickle


class UserTaskSaver:
    filename = "./user_tasks.save"
    _user_task = {}

    def __init__(self):
        self.upload()

    def save(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self._user_task, file)

    def upload(self):
        try:
            with open(self.filename, "rb") as file:
                self._user_task = pickle.load(self.filename)
        except FileNotFoundError:
            self._user_task = {}

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

    def __del__(self):
        self.save()
