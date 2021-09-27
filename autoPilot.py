from PID_Controller import PID
from typing import List
from Objects.Rocket import Rocket
import numpy as np

class Target:
    def __init__(self, pos:np.ndarray, vel:np.ndarray) -> None:
        self.pos = pos
        self.vel = vel

class AutoPilot:
    def __init__(self, rocket:Rocket, goals:List[Target]) -> None:
        self.rocket = rocket
    
        self.goal = 0
        self.goals = goals

        self.pid_y = PID(1, 1, 1)

    def update(self, delta_time):
        pid_y_val = self.pid_y.compute(self.rocket.pos[1][0], self.goals[self.goal].pos[1][0])
        if pid_y_val < 0:
            self.rocket.thrust = 1
        else:
            self.rocket.thrust = 0