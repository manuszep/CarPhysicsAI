import pyglet

def center_image(image):
  image.anchor_x = image.width // 2
  image.anchor_y = image.height // 2

pyglet.resource.path = ['./assets']
pyglet.resource.reindex()

player_image = pyglet.resource.image("player.png")

center_image(player_image)