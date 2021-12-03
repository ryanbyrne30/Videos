

class Canvas(object):
    def __init__(self, width, height, x_range, y_range):
        # constants
        self.width = width 
        self.height = height 
        self.x_range = x_range 
        self.y_range = y_range 

        # variables
        self.ppu_x = self.width // self.x_range
        self.ppu_y = self.height // self.y_range


    def plot(self, x, y):
        pass
