import numpy as np

class Rocket:

    def __init__(self, pos : np.ndarray, mass : float, vel : np.ndarray, acc : np.ndarray, angle : float  ) -> None:
        self.pos = pos
        self.acc = acc
        self.vel = vel
        self.angle = angle
        self.mass = mass
        self.thrust = 0 # 0 - 1

    def apply_force (self, force):
        self.acc = np.divide(force,self.mass)

    def update (self, d_time):
        self.vel += self.acc * d_time
        self.pos += self.vel * d_time
        self.acc = np.zeros((2, 1))

