from PID_Controller import PID
from typing import List
from Objects.Rocket import Rocket
import numpy as np

class Target:
    def __init__(self, pos:np.ndarray, vel:np.ndarray = np.zeros((2,1), float)) -> None:
        self.pos = pos
        self.vel = vel

class AutoPilot:
    def __init__(self, rocket:Rocket, goals:List[Target]) -> None:
        self.rocket = rocket
    
        self.goal = 0
        self.goals = goals

        self.pid_y =  PID(1, 1/30, 1, 1000, 0) # Calibrated NO TOUCHY
        self.pid_Vy = PID(40, 1, 1, 1000, 0)   # Calibrated NO TOUCHY

        self.trig = 800

        self.pid_y_val = 0

        self.complete = False

    def update(self, delta_time):
        if self.goal < len(self.goals):
            self.pid_y_val = self.pid_y.compute(self.rocket.pos[1][0], self.goals[self.goal].pos[1][0], delta_time)
            self.pid_y_val += self.pid_Vy.compute(self.rocket.vel[1][0], self.goals[self.goal].vel[1][0], delta_time)

            thrust = self.pid_y_val/1000

            if thrust > 1:
                thrust = 1
            if thrust < 0:
                thrust = 0

            self.rocket.thrust = thrust
            
            if self.rocket.pos[1][0] <= self.goals[self.goal].pos[1][0] + 5 and self.rocket.pos[1][0] >= self.goals[self.goal].pos[1][0] - 5:
                self.trig *= -1
                # self.pid_y.clear()
                self.goal += 1
        elif not self.complete:
            self.rocket.thrust = 0
            print("Flight plan complete!!!")
            print("Landing V: {}".format(self.rocket.vel[1][0]))
            self.complete = True