from Objects.Logger import Logger
from PID_Controller import PID
from typing import List
from Objects.Rocket import Rocket
import numpy as np
from datetime import datetime

class Target:
    def __init__(self, pos:np.ndarray, vel:np.ndarray = np.zeros((2,1), float)) -> None:
        self.pos = pos
        self.vel = vel

class AutoPilot:
    def __init__(self, rocket:Rocket, goals:List[Target], mode:str = "Auto") -> None:

        self.mode = mode

        self.rocket = rocket
    
        self.goal = 0
        self.goals = goals

        self.pid_y =  PID(1, 0.029, 100, 1000, 0) # Calibrated NO TOUCHY
        self.pid_Vy = PID(40, 0.8, 100, 1000, 0)   # Calibrated NO TOUCHY

        self.trig = 800

        self.pid_y_val = 0

        self.complete = False

        self.time = 0

        self.landingSpeed = None
        self.apogee = None

        self.logger = Logger("logs/FlightLog_{}.csv".format(datetime.now()))

    def update(self, delta_time):
        self.logger.log([self.time, 
                         self.rocket.pos[0][0], self.rocket.pos[1][0], 
                         self.rocket.vel[0][0], self.rocket.vel[1][0],
                         self.rocket.acc[0][0], self.rocket.acc[1][0],
                         self.rocket.thrust,
                         self.rocket.angle,
                         ])
        if round(self.rocket.vel[1][0]) == 0:
            self.apogee = self.rocket.pos[1][0]
        if self.mode == "Auto" :
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
                self.landingSpeed = self.rocket.vel[1][0]
                print("Landing V: {}".format(self.landingSpeed))
                self.complete = True
        elif self.mode == "Manual":
            pass
        self.time += delta_time