from typing import List
import numpy as np
import json

# data = time, x, y, vx, vy, ax ,ay, throttle, a

class Logger:

    def __init__(self, filename) -> None:
        self.filename = filename

    def log (self, data:List):
        with open(self.filename, "w") as f:
            f.write("{},{},{},{},{},{},{},{},{}".format(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))