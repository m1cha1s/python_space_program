import numpy as np
from random import randint, random

class WindMenager:

    def __init__(self, settings) -> None:
        self.settings = settings
        self.max_speed = self.settings.wind_max_speed
        self.min_spped = self.settings.wind_min_speed
        self.num_of_levels = self.settings.wind_num_of_levels
        self.level_high = int (self.settings.height / self.num_of_levels)
        self.wind_shear_component = self.settings.wind_shear_component
        self.base_speed = randint(self.min_spped, self.max_speed)
        self.speeds = [self.base_speed]
        self.direction = 1

    def calc_speed (self):
        for level in range (1, self.num_of_levels):

            h1 = self.level_high * (level - 1) + self.level_high / 2
            h2 = self.level_high * level + self.level_high / 2

            self.speeds.append(self.speeds[level - 1] * (h2 / h1)**self.wind_shear_component)

        print(self.speeds)

    def change_direction (self, dt):

        self.direction = 1 if random() > 0.5 else -1

    def get_wind_speed (self, h):

        print(self.direction)
        
        return self.base_speed * ((h / (self.level_high // 2))**self.wind_shear_component) * self.direction

        # return self.speeds[int(h / self.settings.height * self.num_of_levels) - 1] * direction