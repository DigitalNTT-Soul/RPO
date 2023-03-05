from kivy.uix.floatlayout import FloatLayout

# Quick class used to define the Main Screen element of the UI
#   This should make it easier later on to deal with the
#   boundary/layer handling imposed on the child widgets of the MainScreen
class MainScreen(FloatLayout):
    # placeholder/pass-through of the __init__ function
    #   just to call the FloatLayout's __init__ function when
    #   the MainScreen is generated
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)