import numpy as np
import math

class Engine:

    def __init__(self, rocket, max_power, angle, fuel_burned_per_s, fuel_mass, throttle_step = 0.1,) -> None:
        self.rocket = rocket
        self.max_power = max_power
        self.force = 0
        self.angle = angle
        self.fuel_burned_per_s = fuel_burned_per_s
        self.fuel_mass = fuel_mass
        self.throttle_step = throttle_step
        self.throttle = 0
        self.is_active = True

    def change_throttle (self, sign):
        self.throttle += sign * self.throttle_step

    def change_angle (self, angle):
        self.angle = angle

    def update_fuel (self):
        self.fuel_mass -= self.fuel_burned_per_s * self.throttle * self.d_time

        self.rocket.mass -= self.fuel_burned_per_s * self.throttle * self.d_time

        if self.fuel_mass < 0:
            self.fuel_mass = 0
            self.is_active = False

    def apply_force (self):
        if not self.is_active:
            return 
        self.force = self.max_power * self.throttle / self.rocket.mass
        ax = round(math.cos(math.radians(self.angle)) * self.force, 2)
        ay = round(math.sin(math.radians(self.angle)) * self.force, 2)
        
        self.acc = np.array([[ax],[ay]], float)
        

    def update (self, d_time):
        self.d_time = d_time
        self.apply_force()
        self.update_fuel()
        return self.acc, self.fuel_mass
        