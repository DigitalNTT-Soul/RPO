from screen_elements.pillar_button import PillarButton

# Quick class to define the Pillar Sub Buttons and their behaviors
class PillarSubButton(PillarButton):
    # Quick Pass-through to initialize the underlying PillarButton object
    def __init__(self, **kwargs):
        super(PillarSubButton, self).__init__(**kwargs)