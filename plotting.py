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

ao = AutoPilot(sim.ships[0], [Target(np.array([[50],[800]], float), np.zeros((2,1), float)), 
                              Target(np.array([[100],[0]], float), np.zeros((2,1), float))])

y = []
vy = []
thr = []
t = []
zero = []
targets = []

x = []
vx = []

fig, axs = plt.subplots(1, 2)

while time < 500 :
    ao.update(dt)
    sim.run(dt)
    thr.append(ao.pid_y_val)
    y.append(sim.ships[0].pos[1][0])
    vy.append(sim.ships[0].vel[1][0])
    zero.append(0)
    t.append(time)
    targets.append(ao.goal*100)

    x.append(sim.ships[0].pos[0][0])
    vx.append(sim.ships[0].vel[0][0])

    time += dt

axs[0].plot(t, zero)
axs[0].plot(t, y)
axs[0].plot(t, vy)
axs[0].plot(t, targets)
axs[0].plot(t, thr)

axs[1].plot(t, x)
axs[1].plot(t, vx)

plt.show()