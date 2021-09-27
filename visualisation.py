import pyglet

window = pyglet.window.Window(1000, 500)

ship = pyglet.shapes.Circle(500, 0, 10)

@window.event
def on_key_press(symbol, mod):
    if symbol == 119:
        pass # up
    if symbol == 115:
        pass # down

@window.event
def on_draw():
    window.clear()
    ship.draw()

def update(dt):
    pass

pyglet.clock.schedule_interval(update, 0.1)
pyglet.app.run()