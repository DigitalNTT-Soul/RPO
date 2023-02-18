from kivy.core.window import Window
from kivy.uix.widget import Widget
from config import *

class KeyboardService(Widget):
    def __init__(self):
        # Request a keyboard connection from the Window
        #   Since Kivy was designed for phones, Keyboard handling is a bit messier
        self._keyboard = Window.request_keyboard(self._disconnect_keyboard, self)

        # Bind the keyboard's loose key-down listener to our relevant action method
        self._keyboard.bind(on_key_down=self._on_key_down)
 
        # Bind the keyboard's loose key-up listener to our relevant action method
        # self._keyboard.bind(on_key_up=self._on_key_up)

        # create a dictionary to store our keycodes and their bound functions
        #   as key-value pairs
        self._keybinds = {}

    def _disconnect_keyboard(self):
        # unbind all the things we bound
        self._keyboard.unbind(on_key_down=self._on_key_down)
        # self._keyboard.unbind(on_key_up=self._on_key_up)
        # let go of the dead keyboard connection
        self._keyboard = None

        # clear the keybinds (in the long run this *may* be a bad thing,
        #   so this may be removed in the future)
        self._keybinds = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        # Ensure keycode is among stored keybinds
        #   if it is, then call the function stored as the value of that key-value pair
        if keycode[1] in self._keybinds.keys():
            self._keybinds[keycode[1]]()
            return True

    def _on_key_up(self, keyboard, keycode):
        # May one day do something. Until then, stubbed
        pass

    def add_keybinds(self, keys: list, value):
        # ensure value is a function so it can be called later
        if not callable(value):
            # early return if it's not
            return False
        
        # ensure keys are in list format
        if isinstance(keys, list):
            # loop through them
            for key in keys:
                # ensure the key name is a str
                if isinstance(key, str):
                    # call the method that adds them individually
                    self._add_keybind(key, value)
            # return True. Not necessary at moment, but may be useful later
            return True
        # return False. Not necessary at moment, but may be useful later
        return False

    def _add_keybind(self, key: str, value):
        # Double check function status of value in case this method was called
        #   erroneously from outside the class
        if not callable(value):
            # Early return if not a function
            return False
        
        # once again ensure key name is a str: same paranoia as above
        if isinstance(key, str):
            # register the key-value pair to the keybinds Dictonary
            self._keybinds[key] = value
            # Early return True. Not necessary at moment, but may be useful later
            return True
        # End return False. Not necessary at moment, but may be useful later
        return False

    def remove_keybinds(self, keys: list):
        # Ensure provided keys are in list format
        if isinstance(keys, list):
            # loop through them
            for key in keys:
                # ensure the individual key is in str format
                if isinstance(key, str):
                    # remove the individual key from the keybinds dictionary
                    self._remove_keybind(key)

    def _remove_keybind(self, key: str):
        # ensure we aren't trying to remove a keybind that doesn't exist
        if key not in self._keybinds.keys():
            # early return instead of attempting to delete nothingness
            return
        
        # remove the keybind from the dictionary
        del self._keybinds[key]