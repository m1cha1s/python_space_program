from PID_Controller import PID
from typing import List
from Objects.Rocket import Rocket
import numpy as np

class Target:
    def __init__(self, pos:np.ndarray) -> None:
        self.pos = pos
        # self.vel = vel

class AutoPilot:
    def __init__(self, rocket:Rocket, goals:List[Target]) -> None:
        self.rocket = rocket
    
        self.goal = 0
        self.goals = goals

        self.pid_y = PID(5.9, 0.002, 0.45)
        self.pid_vy = PID(1, 0, 0)

        self.trig = 800

    def update(self, delta_time):
        if self.goal < len(self.goals):
            pid_y_val = self.pid_y.compute(self.rocket.pos[1][0], self.goals[self.goal].pos[1][0], delta_time)
            # print(pid_y_val)
            if pid_y_val > self.trig:
                self.rocket.thrust = 1
            else:
                self.rocket.thrust = 0
            if self.rocket.pos[1][0] <= self.goals[self.goal].pos[1][0] + 5 and self.rocket.pos[1][0] >= self.goals[self.goal].pos[1][0] - 5:
                self.trig *= -1
                # self.pid_y.clear()
                self.goal += 1
        else:
            self.rocket.thrust = 0
            print("Flight plan complete!!!")