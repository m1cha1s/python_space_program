import numpy as np

class Settings:

    # forces to apply 
    # lenght - m
    # time - s 
    # mass - kg 
    # force - N
    
    def __init__(self) -> None:
        # forces 
        self.gravity = np.array([[0], [-9.8]], float)

        # simulation setup 
        self.height = 1000
        self.width = 2000

        # ship 
        self.ship_mass = 3 * (10 ** 6)
        self.fuel_percentage = 0.85 # od 0 do 1 
        self.fuel_burned_per_s = 4989.5 # s

        # engines 
        self.engine1 =  35 * (10**6)*2
        self.engine2 =  7 * (10**6)*2

        #wind 
        self.wind_num_of_levels = 1
        self.wind_max_speed = 10
        self.wind_min_speed = 0
        self.wind_shear_component = 0.1 # obtained from tables online

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