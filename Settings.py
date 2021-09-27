import numpy

class Settings:

    # forces to apply 
    # lenght - m
    # time - s 
    # mass - kg 
    # force - N
    
    def __init__(self) -> None:
        # forces 
        self.gravity = 9.8 

        # simulation setup 
        self.height = 1000
        self.width = 2000

        # ship 
        self.ship_mass = 3 * (10 ** 6)

        # engines 
        self.engine1 = (0, 35 * (10**6))

        # start 
        self.start_h = 800

        # end 
        self.auto_max_landing_v = 3 
        self.manual_max_landing_v = 10