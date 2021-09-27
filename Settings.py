import numpy

class Settings:

    # forces to apply 
    # lenght - m
    # time - s 
    # mass - kg 
    # force - N
    
    def __init__(self) -> None:
        # forces 
        self.gravity = -9.8 

        # simulation setup 
        self.height = 1000
        self.width = 2000

        # ship 
        self.ship_mass = 3 * (10 ** 6)

        # engines 
        self.engine1 = 35 * (10**6)

        # start 
        self.start_h = 800

        # end 
        self.auto_max_landing_v = 3 
        self.manual_max_landing_v = 10

        self.colors = {
            "red" : (255, 0, 0),
            "orange" : (255, 112, 0),
            "yellow" : (255, 255, 0),
            "white" : (255, 255, 255),
        }
    
    def get_lower_color (self, color):
        switcher = {
            (255, 0, 0) : -1,
            (255, 112, 0) : self.colors["red"],
            (255, 255, 0) : self.colors["orange"],
            (255, 255, 255) : self.colors["yellow"],
        }
        return switcher[color]