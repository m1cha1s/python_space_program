from typing import Dict
import numpy as np

class AutoPilot:
    def __init__(self) -> None:
        self.landing_vel:np.ndarray = np.array([[0],[0]], float)

        self.pos:np.ndarray = np.zeros((2,1), float)
        self.vel:np.ndarray = np.zeros((2,1), float)
        self.acc:np.ndarray = np.zeros((2,1), float)
        self.thr:float = 0.0
    
    def updateTelemetry(self, tlm:Dict) -> None:
        self.pos = tlm["pos"]
        self.vel = tlm["vel"]
        self.acc = tlm["acc"]

    def getThrust(self):
        return self.thr

    def update(self):
        self.thr = 1