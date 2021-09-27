import numpy as np

class PID:
    def __init__(self, P:float, I:float, D:float) -> None:
        self.P = P
        self.I = I
        self.D = D

        self.e = 0
        self.e_prev = 0
        
        self.e_sum = 0

    def compute(self, current, target, delta_time):
        self.e = target - current

        self.e_sum += ((self.e + self.e_prev)*delta_time)/2

        P = self.P * self.e
        I = self.I * self.e_sum
        D = self.D * (self.e - self.e_prev)

        self.e_prev = self.e

        return P + I + D