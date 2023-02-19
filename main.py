import os, sys, plyer
os.environ['KIVY_IMAGE'] = 'pil,sdl2'

from config import *
import kivy
from kivy.config import Config
kivy.require('2.1.0')
from kivy.app import App
from screen_elements.core_grid import CoreGrid
from screen_elements.pillar_button import PillarButton
from screen_elements.main_screen import MainScreen
from screen_elements.module_image import ModuleImage

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
#       -- Keep objects moved over edge of main_screen from being displayed
#           -- Including parts of objects
#           -- This is part of widget layering mentioned below
#       -- On Pillar Button press, create and slide-down 9 more "sub-buttons" of similar design with different text
#           -- new buttons can be inserted into these option lists by the module.
#       -- Maybe put a black box behind first pillar buttons, Perhaps as something to hide stray screen objects behind?
#           -- Or find alternative widget layering plan