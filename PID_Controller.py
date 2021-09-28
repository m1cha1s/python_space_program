import numpy as np

class PID:
    def __init__(self, P:float, I:float, D:float, max:float, min:float) -> None:
        self.P = P
        self.I = I
        self.D = D

        self.max = max
        self.min = min

        self.e = 0
        self.e_prev = 0
        
        self.e_sum = 0

        self.val1 = 0
        self.val2 = 0

        self.Pv = 0
        self.Iv = 0
        self.Dv = 0     

    def clear(self):
        self.e = 0
        self.e_prev = 0
        self.e_sum = 0

        self.val1 = 0
        self.val2 = 0

    def compute(self, current, target, delta_time):
        self.e = target - current

        if not (self.val1 != self.val2 and ((self.val1 < 0 and self.Iv < 0) or (self.val1 > 0 and self.Iv > 0))) :           
            self.e_sum += ((self.e + self.e_prev)*delta_time)/2

        self.Pv = self.P * self.e
        self.Iv = self.I * self.e_sum
        self.Dv = self.D * (self.e - self.e_prev)
        # print(self.Dv)

        self.e_prev = self.e

        self.val1 = self.Pv + self.Iv + self.Dv
        self.val2 = self.val1

        if self.val1 > self.max :
            self.val2 = self.max
        if self.val1 < self.min :
            self.val2 = self.min


        return self.val2