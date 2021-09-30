from autoPilot import AutoPilot, Target
import pyglet
from pyglet.window import key
import numpy as np
from simulation import Simulation
from Objects.particles import ParticleMenager
from Settings import Settings
import time

# mode = "Auto"
mode = "Manual"

window = pyglet.window.Window(1000, 500)

speedometer = pyglet.text.Label("Vx: {} Vy : {}".format(0.0, 0.0),y=480)
altimeter = pyglet.text.Label("X: {} Alt: {}".format(0.0, 0.0),y=460)
rocket_angle = pyglet.text.Label("Rocket angle: {} Engine angle: {} deg".format(0.0, 0.0),y=440)
fuel_indicator = pyglet.text.Label("Ramaining fuel (engine #1): {}%".format(100),y=420)

mode_indicator = pyglet.text.Label("Mode: {}".format(mode), x=880, y=480)
phase_indicator = pyglet.text.Label("Phase {}".format(None), x=880, y=460)

apogee_label = pyglet.text.Label("Apogee: {}".format(None), y=400)
landing_speed_label = pyglet.text.Label("Landing speed: {}".format(None), y=380)

hundr_prc = pyglet.text.Label("100%", y=85)
zero_prc = pyglet.text.Label("0%", x=20)
thrustometer = pyglet.shapes.Rectangle(45, 0, 10, 0)

ship = pyglet.shapes.Rectangle(500, 0, 2, 40)

ships_data = [{
    "pos" : np.array([[1000],[0]], float),
    "mass" : 3 * (10**6),
    "vel" : np.array([[0], [0]], float),
    "acc" : np.array([[0], [0]], float),
    "angle" : 0,
}]

sim = Simulation(ships_params = ships_data)

ao = AutoPilot(sim.ships[0], [Target(np.array([[0],[800]], float), np.zeros((2,1), float)), 
                              Target(np.array([[0],[0]], float), np.zeros((2,1), float))],
                              mode)

@window.event
def on_key_press(symbol, mod):
    mode = "Manual"
    if mode == "Manual":
        if symbol == key.W and sim.ships[0].engines[0].throttle <= 0.9:
            sim.ships[0].engines[0].change_throttle(1)
        if symbol == key.S and sim.ships[0].engines[0].throttle >= 0.1:
            sim.ships[0].engines[0].change_throttle(-1)
        if symbol == key.A:
            sim.ships[0].engines[2].throttle = 1
        if symbol == key.D:
            sim.ships[0].engines[1].throttle = 1

@window.event
def on_key_release(symbol, mod):
    if symbol == key.A:
        sim.ships[0].engines[2].throttle = 0
    if symbol == key.D:
        sim.ships[0].engines[1].throttle = 0

@window.event
def on_draw():
    window.clear()
    if not sim.ships[0].is_hidden:
        ship.draw()

    apogee_label.draw()
    landing_speed_label.draw()
    
    speedometer.draw()
    altimeter.draw()
    rocket_angle.draw()
    fuel_indicator.draw()

    mode_indicator.draw()
    phase_indicator.draw()

    thrustometer.draw()
    hundr_prc.draw()
    zero_prc.draw()
    pman.draw_particles()


def update(dt):
    ao.update(dt)
    sim.run(dt)
    pman.update_particles(dt)
    speedometer.text = "Vx: {} Vy: {} m/s".format(round(sim.ships[0].vel[0][0],4), round(sim.ships[0].vel[1][0],4))
    altimeter.text = "X: {} H: {} m".format(round(sim.ships[0].pos[0][0],4), round(sim.ships[0].pos[1][0],4))
    rocket_angle.text = "Rocket angle: {} Engine angle: {} deg".format(round(sim.ships[0].rotation_angle,4), round(sim.ships[0].engines[0].angle,4))
    fuel_indicator.text = "Ramaining fuel (engine #1): {}%".format(round(sim.ships[0].fuel_percentage_left * 100, 2))
    thrustometer.height = 100 * sim.ships[0].engines[0].throttle


    apogee_label.text = "Apogee: {}".format(ao.apogee)
    landing_speed_label.text = "Landing speed: {}".format(ao.landingSpeed)

    phase_indicator.text = "Phase {}".format(ao.goal+1)

    ship.x = sim.ships[0].pos[0][0]/2
    ship.y = sim.ships[0].pos[1][0]/2
    ship.rotation = sim.ships[0].rotation_angle

s = Settings()
pman = ParticleMenager(s, np.array([[500], [100]]), 100, (30, 60))
pman.spawn_particles()

pyglet.clock.schedule_interval(update, 0.00001)
pyglet.app.run()