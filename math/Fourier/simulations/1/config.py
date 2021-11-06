class Config(object):
    def __init__(self, 
            domain=(-10, 10),
            range=(-10, 10),
            speed=100):
        self.screen = ConfigScreen()
        self.surfaces = ConfigSurfaces(domain, range)
        self.speed = speed
        self.dot = ConfigDot()

class ConfigDot(object):
    def __init__(self):
        self.radius = 5
        self.color = [255,0,0]

class ConfigScreen(object):
    def __init__(self):
        self.size = self.width, self.height = 1000, 1000
        self.color = (0,0,0)

class ConfigSurfaces(object):
    def __init__(self, domain, range):
        self.main = ConfigSurface(domain, range)
        self.all = [ 
            self.main
        ]

class ConfigSurface(object):
    def __init__(self, domain, range):
        self.size = self.width, self.height = 1000, 1000
        self.x = 0
        self.y = 0
        self.gridColor = (25, 25, 25)
        self.color = (15,15,15)
        self.xtick = self.width / (domain[1]-domain[0])
        self.ytick = self.height / (range[1]-range[0])