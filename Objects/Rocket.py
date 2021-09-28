import numpy as np
from .Engine import Engine

class Rocket:

    def __init__(self, settings, pos : np.ndarray, mass : float, vel : np.ndarray, acc : np.ndarray, angle : float  ) -> None:
        self.pos = pos
        self.acc = acc
        self.vel = vel
        self.angle = angle
        self.mass = mass
        self.kinetic_energy = 0
        self.settings = settings
        self.fuel_mass : float = self.mass * self.settings.fuel_percentage 
        self.engine = Engine(self, self.settings.engine1, 90, 5000, self.fuel_mass)
        self.static_forces = [self.settings.gravity]

    def apply_static_forces(self, d_time):
        for static_force in self.static_forces:
            if self.pos[1][0] > 0:
                self.acc += static_force

    def calc_kenergy (self):
        sum_v = (self.vel[0][0]**2 + self.vel[1][0]**2)**(1/2)
        self.kinetic_energy = self.mass * (sum_v**2) / 2

    def check_high (self):
        if self.pos[1][0] < 0:
            self.vel *= 0
            self.pos[1][0] = 0
    
    def update (self, d_time):
        self.acc_engines, self.fuel_mass = self.engine.update(d_time)
        self.acc += self.acc_engines

        self.vel += self.acc * d_time
        self.pos += self.vel * d_time

        self.acc = np.zeros((2, 1))

        self.check_high()

