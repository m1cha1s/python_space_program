import numpy as np
import math

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

class Engine:

    def __init__(self, rocket, max_power, angle, fuel_burned_per_s, orientation, throttle_step = 0.1,) -> None:
        self.rocket = rocket
        self.max_power = max_power
        self.force = 0
        self.angle = angle
        self.fuel_burned_per_s = fuel_burned_per_s
        self.throttle_step = throttle_step
        self.throttle = 0
        self.is_active = 1
        self.distance_to_center_of_mass = 20
        self.orientation = orientation 

    def change_throttle (self, sign):
        self.throttle += sign * self.throttle_step

    def change_angle (self, angle):
        self.angle = angle
    
    def calc_fuel_burned (self):
        self.fuel_burned = self.d_time * self.throttle * self.fuel_burned_per_s

    def apply_force (self):
        self.force = self.max_power * self.throttle / self.rocket.mass * self.is_active
        ax = round(math.cos(math.radians(self.angle + self.orientation)) * self.force, 2)
        ay = round(math.sin(math.radians(self.angle + self.orientation)) * self.force, 2)

        self.rocket.rotation_angle = 0

        rho, phi = cart2pol(ax, ay)
        phi += math.radians(self.rocket.rotation_angle)
        x, y = pol2cart(rho, phi)

        # print(rho)

        # print(math.degrees(phi))
        self.acc = np.array([[-x], [y]], float)
        
    def update (self, d_time):
        self.d_time = d_time
        self.apply_force()
        self.rotational_force =  math.sin(math.radians(self.angle)) * self.force
        self.calc_fuel_burned()
        return self.acc, self.fuel_burned, self.rotational_force, self.distance_to_center_of_mass
        