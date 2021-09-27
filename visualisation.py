import pyglet
import numpy as np
from simulation import Simulation

window = pyglet.window.Window(1000, 500)

speedometer = pyglet.text.Label("Vy: {}".format(0.0),y=480)
altimeter = pyglet.text.Label("Alt: {}".format(0.0),y=460)

hundr_prc = pyglet.text.Label("100%", y=85)
zero_prc = pyglet.text.Label("0%", x=20)
thrustometer = pyglet.shapes.Rectangle(45, 0, 10, 0)

ship = pyglet.shapes.Rectangle(500, 0, 2, 40)

ships_data = {
    "pos" : np.array([[1000],[0]], float),
    "mass" : 3 * (10**6),
    "vel" : np.array([[0], [0]], float),
    "acc" : np.array([[0], [0]], float),
    "angle" : 1,
}

sim = Simulation(ships_params = ships_data)

@window.event
def on_key_press(symbol, mod):
    if symbol == 119 and sim.ships[0].thrust < 1:
        sim.ships[0].thrust += 0.1
        sim.ships[0].thrust = round(sim.ships[0].thrust, 1)
        thrustometer.height = 100 * sim.ships[0].thrust
    if symbol == 115 and sim.ships[0].thrust > 0:
        sim.ships[0].thrust -= 0.1
        sim.ships[0].thrust = round(sim.ships[0].thrust, 1)
        thrustometer.height = 100 * sim.ships[0].thrust
    print(sim.ships[0].thrust)

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

    speedometer.draw()
    altimeter.draw()

    thrustometer.draw()
    hundr_prc.draw()
    zero_prc.draw()

def update(dt):
    sim.run(dt)
    speedometer.text = "Vy: {} m/s".format(round(sim.ships[0].vel[1][0],4))
    altimeter.text = "H: {} m".format(round(sim.ships[0].pos[1][0],4))

    ship.x = sim.ships[0].pos[0][0]/2
    ship.y = sim.ships[0].pos[1][0]/2

pyglet.clock.schedule_interval(update, 0.00001)
pyglet.app.run()