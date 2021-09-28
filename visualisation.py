from autoPilot import AutoPilot, Target
import pyglet
import numpy as np
from simulation import Simulation
from Objects.particles import ParticleMenager
from Settings import Settings
import time

mode = "Auto"
# mode = "Manual"

window = pyglet.window.Window(1000, 500)

speedometer = pyglet.text.Label("Vy: {}".format(0.0),y=480)
altimeter = pyglet.text.Label("Alt: {}".format(0.0),y=460)

mode_indicator = pyglet.text.Label("Mode: {}".format(mode), x=880, y=480)
phase_indicator = pyglet.text.Label("Phase {}".format(None), x=880, y=460)

apogee_label = pyglet.text.Label("Apogee: {}".format(None), y=440)
landing_speed_label = pyglet.text.Label("Landing speed: {}".format(None), y=420)

hundr_prc = pyglet.text.Label("100%", y=85)
zero_prc = pyglet.text.Label("0%", x=20)
thrustometer = pyglet.shapes.Rectangle(45, 0, 10, 0)

ship = pyglet.shapes.Rectangle(500, 0, 2, 40)

ships_data = [{
    "pos" : np.array([[1000],[0]], float),
    "mass" : 3 * (10**6),
    "vel" : np.array([[0], [0]], float),
    "acc" : np.array([[0], [0]], float),
    "angle" : 90,
}]

sim = Simulation(ships_params = ships_data)

ao = AutoPilot(sim.ships[0], [Target(np.array([[0],[800]], float)), Target(np.array([[0],[0]], float))], mode)

@window.event
def on_key_press(symbol, mod):
    mode = "Manual"
    if mode == "Manual":
        if symbol == 119 and sim.ships[0].engine.throttle <= 0.9:
            sim.ships[0].engine.change_throttle(1)
        if symbol == 115 and sim.ships[0].engine.throttle >= 0.1:
            sim.ships[0].engine.change_throttle(-1)

# @window.event
# def on_key_release(symbol, mod):
#     if symbol == 119:
#         # sim.ships[0].apply_force(np.array([[0],[35*(10**6)]], float))
#     if symbol == 115:
#         pass # down

@window.event
def on_draw():
    window.clear()
    ship.draw()

    apogee_label.draw()
    landing_speed_label.draw()
    
    speedometer.draw()
    altimeter.draw()

    mode_indicator.draw()
    phase_indicator.draw()

    thrustometer.draw()
    hundr_prc.draw()
    zero_prc.draw()
    pman.draw_particles()


def update(dt):
    ao.update(dt)
    sim.run(dt)
    #pman.update_particles(dt)
    speedometer.text = "Vy: {} m/s".format(round(sim.ships[0].vel[1][0],4))
    altimeter.text = "H: {} m".format(round(sim.ships[0].pos[1][0],4))
    thrustometer.height = 100 * sim.ships[0].engine.throttle

    apogee_label.text = "Apogee: {}".format(ao.apogee)
    landing_speed_label.text = "Landing speed: {}".format(ao.landingSpeed)

    phase_indicator.text = "Phase {}".format(ao.goal+1)

    ship.x = sim.ships[0].pos[0][0]/2
    ship.y = sim.ships[0].pos[1][0]/2

s = Settings()
pman = ParticleMenager(s, np.array([[500], [100]]), 100, (30, 60))
pman.spawn_particles()

pyglet.clock.schedule_interval(update, 0.00001)
pyglet.app.run()