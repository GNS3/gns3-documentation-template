import json

class Config:
    def __init__(self, path):
        self._path = path
        with open(path) as f:
            self._config = json.load(f)

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

    def get(self, key):
        return self._config.get(key)

    def save(self):
        with open(self._path, 'w+') as f:
            json.dump(self._config, f, indent=4)
