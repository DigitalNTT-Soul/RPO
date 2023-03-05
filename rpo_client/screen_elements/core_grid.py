from config import *
from kivy.uix.gridlayout import GridLayout
from services.keyboard_service import KeyboardService
from kivy.properties import ObjectProperty

class CoreGrid(GridLayout):
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
        keyboard_service.add_keybinds(KEYBINDS_LEFT, self.kb_move_test_image_left)
        keyboard_service.add_keybinds(KEYBINDS_RIGHT, self.kb_move_test_image_right)    
        keyboard_service.add_keybinds(KEYBINDS_UP, self.kb_move_test_image_up)
        keyboard_service.add_keybinds(KEYBINDS_DOWN, self.kb_move_test_image_down)

    def kb_move_test_image_left(self):
        # pos_hint, while very convenient during initial object placement
        #   makes widgets immobile. If it's not empty, empty it, otherwise
        #   coordinate editing is futile.
        if self.test_image.pos_hint != {}:
            self.test_image.pos_hint = {}
        self.test_image.x -= 1

    def kb_move_test_image_right(self):
        # pos_hint, while very convenient during initial object placement
        #   makes widgets immobile. If it's not empty, empty it, otherwise
        #   coordinate editing is futile.
        if self.test_image.pos_hint != {}:
            self.test_image.pos_hint = {}
        self.test_image.x += 1

    def kb_move_test_image_up(self):
        # pos_hint, while very convenient during initial object placement
        #   makes widgets immobile. If it's not empty, empty it, otherwise
        #   coordinate editing is futile.
        if self.test_image.pos_hint != {}:
            self.test_image.pos_hint = {}
        # in Kivy, coordinate 0,0 is bottom left, with Y increasing as you go
        #   up the screen and X increasing as you go right
        self.test_image.y += 1

    def kb_move_test_image_down(self):
        # pos_hint, while very convenient during initial object placement
        #   makes widgets immobile. If it's not empty, empty it, otherwise
        #   coordinate editing is futile.
        if self.test_image.pos_hint != {}:
            self.test_image.pos_hint = {}
        # in Kivy, coordinate 0,0 is bottom left, with Y increasing as you go
        #   up the screen and X increasing as you go right
        self.test_image.y -= 1