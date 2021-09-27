import numpy as np
import random as rand

class Particle:

    def __init__(self, pos : np.ndarray, vel : np.ndarray, angle : int, size : float, color : tuple) -> None:
        self.pos = pos
        self.vel = vel 
        self.angle = angle
        self.size = size # 0 - 1
        self.color = color # (0-256, 0-256, 0-256)

    def update (self):

        self.pos += self.vel
        self.vel *= 0.9 


    