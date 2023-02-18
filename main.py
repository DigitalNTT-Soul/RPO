from config import *
import kivy
from kivy.config import Config
kivy.require('2.1.0')
from kivy.app import App
from services.keyboard_service import KeyboardService
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

class PillarButton(Button):
    # Currently has no features. Likely to move to another file when adding further features
    pass

class CoreGrid(Widget):
    # Custom Widget class/orientation that occupies the entire window
    #   further defined in the rpo.kv kivy layout file
    def __init__(self, **kwargs):
        # initialize the instance of the parent class
        super(CoreGrid, self).__init__(**kwargs)

        # create an instance of our KeyboardService so that we can create keybinds
        keyboard_service = KeyboardService()

        # Fetch objects (and relevant properties) that were defined in rpo.kv
        play_modules = ObjectProperty(None)
        find_modules = ObjectProperty(None)
        app_settings = ObjectProperty(None)
        combat_pillar = ObjectProperty(None)
        social_pillar = ObjectProperty(None)
        explore_pillar = ObjectProperty(None)
        main_screen = ObjectProperty(None)
        test_image = ObjectProperty(None)

        # create keybinds for up,down,left,right and WADS, binding them to the methods below
        #   Passes the function objects to the keybind dictionary in the keyboard_service
        keyboard_service.add_keybinds(KEYBINDS_LEFT, self.move_test_image_left)
        keyboard_service.add_keybinds(KEYBINDS_RIGHT, self.move_test_image_right)    
        keyboard_service.add_keybinds(KEYBINDS_UP, self.move_test_image_up)
        keyboard_service.add_keybinds(KEYBINDS_DOWN, self.move_test_image_down)

    def move_test_image_left(self):
        # pos_hint, while very convenient during initial object placement
        #   makes widgets immobile. If it's not empty, empty it, otherwise
        #   coordinate editing is futile.
        if self.test_image.pos_hint != {}:
            self.test_image.pos_hint = {}
        self.test_image.x -= 1

    def move_test_image_right(self):
        # pos_hint, while very convenient during initial object placement
        #   makes widgets immobile. If it's not empty, empty it, otherwise
        #   coordinate editing is futile.
        if self.test_image.pos_hint != {}:
            self.test_image.pos_hint = {}
        self.test_image.x += 1

    def move_test_image_up(self):
        # pos_hint, while very convenient during initial object placement
        #   makes widgets immobile. If it's not empty, empty it, otherwise
        #   coordinate editing is futile.
        if self.test_image.pos_hint != {}:
            self.test_image.pos_hint = {}
        # in Kivy, coordinate 0,0 is bottom left, with Y increasing as you go
        #   up the screen and X increasing as you go right
        self.test_image.y += 1

    def move_test_image_down(self):
        # pos_hint, while very convenient during initial object placement
        #   makes widgets immobile. If it's not empty, empty it, otherwise
        #   coordinate editing is futile.
        if self.test_image.pos_hint != {}:
            self.test_image.pos_hint = {}
        # in Kivy, coordinate 0,0 is bottom left, with Y increasing as you go
        #   up the screen and X increasing as you go right
        self.test_image.y -= 1

class RPO(App):
    # Driver that runs the whole application
    def build(self):
        # counter the default behavior of closing app when pressing esc key
        Config.set('kivy', 'exit_on_escape', '0')
        # return an instance of the CoreGrid class of widget, to be displayed on screen
        return CoreGrid()

# actually run the app
RPO().run()

# Sprint 3 todo list
#   stretch:
#       -- figure out how to make the main_screen its own transparent
#       widget specifically for other objects to be displayed in relation to
#       the main_screen object's borders rather than the window's borders
#       -- Keep objects moved over edge of main_screen from being displayed
#           including parts of objects
#           This is part of widget layering mentioned below
#       On Pillar Button press, create and slide-down 9 more buttons of similar design with different text
#           new buttons can be inserted into these option lists by the module.
#       Maybe put a black box behind first pillar buttons, Perhaps as something to hide stray screen objects behind?
#           Or find alternative widget layering plan