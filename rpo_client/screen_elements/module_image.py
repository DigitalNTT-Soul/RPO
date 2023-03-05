from kivy.uix.image import Image

# Define some behaviors of the temporary image we're using in the middle of the screen for testing
class ModuleImage(Image):
    # Pass-through init to parent class
    def __init__(self, **kwargs):
        super(ModuleImage, self).__init__(**kwargs)
        # store state of whether the image was the target of the click
        self.touched = False

    # override default on_touch_down behavior inherited from underlying Image object
    def on_touch_down(self, touch):
        # Immobility unlocker: pos_hint makes objects immobile, so if it's not empty, fix that
        if self.pos_hint != {}:
            self.pos_hint = {}

        # Determine whether the image was the target of the click
        if self.collide_point(*touch.pos):
            # print info about the click/touch
            print(f"Down {touch.pos}")
            # store state of whether the image was the target of the click
            self.touched = True
            # store original position of the click, to help with future math regarding to click/drag
            #   functionality
            self.original_x = self.x
            self.original_y = self.y

    # override default on_touch_move behavior inherited from underlying Image object
    def on_touch_move(self, touch):
        # only act if self was the target of the original touch
        if self.touched:
            # print info about the click/touch
            print(f"Move {touch.pos}")
            # calculate the difference between the current and original touch coordinates
            delta_x = touch.x - touch.ox
            delta_y = touch.y - touch.oy
            # add that difference to the stored original coordiantes of self to get current coordinates of self
            self.x = self.original_x + delta_x
            self.y = self.original_y + delta_y 

    # override default on_touch_up behavior inherited from underlying image object
    def on_touch_up(self, touch):
        # only act if self was target of initial touch
        if self.touched:
            # print info about touch
            print(f"Up {touch.pos}")
            # Clear touched state
            self.touched = False
            # reset original coordinates
            self.original_x = None
            self.original_y = None