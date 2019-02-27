import pyglet
from physicalObject import PhysicalObject
from resource import player_image

game_window = pyglet.window.Window()

car = PhysicalObject(img=player_image, win=game_window)
car.scale = .10

game_window.push_handlers(car.key_handler)

@game_window.event
def on_draw():
  game_window.clear()
  car.draw()

def update(dt):
  car.update(dt)

pyglet.clock.schedule_interval(update, 1/120.0)

pyglet.app.run()
  