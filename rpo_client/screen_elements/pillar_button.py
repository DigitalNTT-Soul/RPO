from kivy.uix.button import Button

# Define custom behavior of Pillar Buttons
class PillarButton(Button):
    # attribute definitions and initialize the underlying Button object
    def __init__(self, **kwargs):
        super(PillarButton, self).__init__(**kwargs)
        # Boolean to store touch state
        self.touched = False

    # override default on_touch_down behavior inherited from underlying Button object
    def on_touch_down(self, touch):
        # Determine whether or not this particular button was pressed
        if self.collide_point(*touch.pos):
            # store that state
            self.touched = True
        # Fire default behavior in addition to any/all overriden behavior
        return super(PillarButton, self).on_touch_down(touch)

    # override default on_touch_move behavior inherited from underlying Button object
    def on_touch_move(self, touch):
        # Fire default behavior in addition to any/all overriden behavior
        return super(PillarButton, self).on_touch_move(touch)

    # override default on_touch_up behavior inherited from underlying Button object
    def on_touch_up(self, touch):
        # Early return if touch didn't apply to this button
        if not self.touched:
            return False

        # Mark the button as no longer being touched because it's been released
        self.touched = False
        # activate on release, but only if mouse/touch hasn't moved much 
        if (abs(touch.ox - touch.x) <= 25 and
            abs(touch.oy - touch.y) <= 25):
            self.activate()

        # Fire default behavior in addition to any/all overriden behavior
        return super(PillarButton, self).on_touch_up(touch)
        
    def activate(self):
        # Currently just a placeholder that prints out some "code scaffolding"
        #   to identify which button was being pressed/activated
        print("Button Activated: ", self.background_color)