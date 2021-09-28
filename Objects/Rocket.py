import numpy as np

class Rocket:

    def __init__(self, settings, pos : np.ndarray, mass : float, vel : np.ndarray, acc : np.ndarray, angle : float  ) -> None:
        self.pos = pos
        self.acc = acc
        self.vel = vel
        self.angle = angle
        self.mass = mass
        self.thrust:float = 0.0 # 0 - 1
        self.kinetic_energy = 0
        self.settings = settings
        self.fuel_mass = self.mass * self.settings.fuel_percentage
        self.is_fuel = True
        self.engines = np.array([[0],[self.settings.engine1]], float)

    def apply_thrust(self):
        self.acc += (self.engines / self.mass)*self.thrust

    def update_thrust (self, n):
        self.thrust += n 
        self.thrust = round(self.thrust, 1)

    def apply_force (self, force):
        self.acc += force / self.mass

    def apply_gravity(self, g):
        self.acc += g

    def calc_kenergy (self):
        sum_v = (self.vel[0][0]**2 + self.vel[1][0]**2)**(1/2)
        self.kinetic_energy = self.mass * (sum_v**2) / 2

    def update_fuel (self, d_time):
        burned_fuel = self.settings.fuel_burned_per_s * d_time * self.thrust
        if self.fuel_mass - burned_fuel > 0:
            self.fuel_mass -= burned_fuel
            self.mass -= burned_fuel
        
        else:
            self.is_fuel = False
        
        print(self.fuel_mass)

    def update (self, d_time):
        # print(self.acc)
        self.update_fuel(d_time)
        self.vel += self.acc * d_time
        self.pos += self.vel * d_time
        self.acc = np.zeros((2, 1))

