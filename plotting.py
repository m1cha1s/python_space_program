import matplotlib.pyplot as plt
from simulation import Simulation
from autoPilot import *
import numpy as np

time = 0
dt = 0.01

ships_data = [{
    "pos" : np.array([[1000],[0]], float),
    "mass" : 3 * (10**6),
    "vel" : np.array([[0], [0]], float),
    "acc" : np.array([[0], [0]], float),
    "angle" : 1,
}]

sim = Simulation(ships_params = ships_data)

ao = AutoPilot(sim.ships[0], [Target(np.array([[0],[800]], float)), Target(np.array([[0],[0]], float))])

y = []
vy = []
t = []
zero = []
targets = []

while time < 80 :
    ao.update(dt)
    sim.run(dt)
    y.append(sim.ships[0].pos[1][0])
    vy.append(sim.ships[0].vel[1][0])
    zero.append(0)
    t.append(time)
    targets.append(ao.goal*100)
    time += dt

plt.plot(t, zero)
plt.plot(t, y)
plt.plot(t, vy)
plt.plot(t, targets)
plt.show()