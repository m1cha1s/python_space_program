import numpy as np

class Rocket:

    def __init__(self, pos : np.ndarray, mass : float, vel : np.ndarray, acc : np.ndarray, angle : float  ) -> None:
        self.pos = pos
        self.acc = acc
        self.vel = vel
        self.angle = angle
        self.mass = mass
        self.thrust:float = 0.0 # 0 - 1
        self.kinetic_energy = 0

    def apply_thrust(self, power : np.ndarray):
        self.acc += (power/self.mass)*self.thrust

    def apply_force (self, force):
        self.acc += force / self.mass

    def apply_gravity(self, g):
        self.acc += g

    def calc_kenergy (self):
        sum_v = (self.vel[0][0]**2 + self.vel[1][0]**2)**(1/2)
        self.kinetic_energy = self.mass * (sum_v**2) / 2

    def update (self, d_time):
        # print(self.acc)
        self.vel += self.acc * d_time
        self.pos += self.vel * d_time
        self.acc = np.zeros((2, 1))

