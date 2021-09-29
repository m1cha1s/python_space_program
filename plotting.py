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

ao = AutoPilot(sim.ships[0], [Target(np.array([[1050],[800]], float), np.zeros((2,1), float)), 
                              Target(np.array([[1100],[0]], float), np.zeros((2,1), float))])

y = []
vy = []
thr = []
t = []
zero = []
targets = []

x = []
vx = []
x_thr = []

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
    x_thr.append(ao.pid_x_val)

    time += dt

plt_zero, = axs[0].plot(t, zero, label="ground")
plt_y, = axs[0].plot(t, y, label="y")
plt_vy, = axs[0].plot(t, vy, label="Vy")
plt_targets_y, = axs[0].plot(t, targets, label="target")
plt_thr, = axs[0].plot(t, thr, label="y thrust")

plt_x, = axs[1].plot(t, x, label="x")
plt_vx, = axs[1].plot(t, vx, label="Vx")
plt_x_thr, = axs[1].plot(t, x_thr, label="x thrust")
plt_targets_x, = axs[1].plot(t, targets, label="target")

plt.legend(handles=[plt_zero, plt_y, plt_vy, plt_targets_y, plt_thr, plt_x, plt_vx, plt_x_thr, plt_targets_x])
plt.show()