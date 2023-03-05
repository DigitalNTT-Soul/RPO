from config import *
# Class not yet in use. Comments will be added when it is
class FlagService:
    def __init__(self):
        self._flags = {}

    def get_flag(self, key):
        result = None
        if key in self._flags.keys():
            result = self._flags[key]
        return result

    def set_flag(self, key, value):
        self._flags[key] = value

    def clear_flag(self, key):
        if key not in self._flags.keys():
            return False
        del self._flags[key]

    def toggle_flag(self, key):
        if key not in self._flags.keys():
            return False
        
        if not isinstance(self._keybinds[key], bool):
            return False

        self._flags[key] = not self._flags[key]
        return True