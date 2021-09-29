from Objects.Logger import Logger
from PID_Controller import PID
from typing import List
from Objects.Rocket import Rocket
import numpy as np
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Target:
    pos : np.ndarray
    vel : np.ndarray

class AutoPilot:
    def __init__(self, rocket:Rocket, goals:List[Target], mode:str = "Auto") -> None:

        self.mode = mode

        self.rocket = rocket
    
        self.goal = 0
        self.goals = goals

        self.pid_y =  PID(3, 0.03, 10000, 1000, 0) # Calibrated NO TOUCHY
        self.pid_Vy = PID(4, 0.1, 10, 1000, 0)   # Calibrated NO TOUCHY

        self.pid_x = PID(1, 0.034, 1000, 1000, -1000)
        self.pid_Vx = PID(10, 0.5, 100, 1000, -1000)

        self.pid_y_val = 0
        self.pid_x_val = 0

        self.complete = False

        self.time = 0

        self.landingSpeed = None
        self.apogee = None

        self.logger = Logger("logs/FlightLog_{}.csv".format(datetime.now()))

    def update(self, delta_time):
        # self.logger.log([self.time, 
        #                  self.rocket.pos[0][0], self.rocket.pos[1][0], 
        #                  self.rocket.vel[0][0], self.rocket.vel[1][0],
        #                  self.rocket.acc[0][0], self.rocket.acc[1][0],
        #                  self.rocket.engines[0].throttle,
        #                  self.rocket.angle,
        #                  ])
        if round(self.rocket.vel[1][0]) == 0:
            self.apogee = self.rocket.pos[1][0]
        if self.mode == "Auto" :
            if self.goal < len(self.goals):
                self.pid_y_val = self.pid_y.compute(self.rocket.pos[1][0], self.goals[self.goal].pos[1][0], delta_time)
                self.pid_y_val += self.pid_Vy.compute(self.rocket.vel[1][0], self.goals[self.goal].vel[1][0], delta_time)

                thr_y = self.pid_y_val/1000 * (self.rocket.mass/self.rocket.starting_mass)

                if thr_y > 1:
                    thr_y = 1
                if thr_y < 0:
                    thr_y = 0

                self.pid_x_val = self.pid_x.compute(self.rocket.pos[0][0], self.goals[self.goal].pos[0][0], delta_time)
                self.pid_x_val += self.pid_Vx.compute(self.rocket.vel[0][0], self.goals[self.goal].vel[0][0], delta_time)

                thr_x = self.pid_x_val/1000 * (self.rocket.mass/self.rocket.starting_mass)

                thr_x_l = 0
                thr_x_r = 0

                if thr_x > 0 :
                    thr_x_r = thr_x
                    if thr_x_r > 1 :
                        thr_x_r = 1
                if thr_x < 0 :
                    thr_x_l = -thr_x
                    if thr_x_l > 1 :
                        thr_x_l = 1

                self.rocket.engines[0].throttle = thr_y
                self.rocket.engines[1].throttle = thr_x_r
                self.rocket.engines[2].throttle = thr_x_l
                
                if (self.rocket.pos[1][0] <= self.goals[self.goal].pos[1][0] + 5) and (self.rocket.pos[1][0] >= self.goals[self.goal].pos[1][0] - 5) and (self.rocket.pos[0][0] <= self.goals[self.goal].pos[0][0] + 5) and (self.rocket.pos[0][0] >= self.goals[self.goal].pos[0][0] - 5) :
                    self.goal += 1
            elif not self.complete:
                self.rocket.engines[0].throttle = 0
                print("Flight plan complete!!!")
                self.landingSpeed = self.rocket.vel[1][0]
                print("Landing V: {}".format(self.landingSpeed))
                self.complete = True
        elif self.mode == "Manual":
            pass
        self.time += delta_time