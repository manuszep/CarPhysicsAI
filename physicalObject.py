import pyglet
from pyglet.window import key
from pygame.math import Vector2
from math import cos, sin, radians, sqrt

class PhysicalObject(pyglet.sprite.Sprite):
  power = 8000.0
  drag = .25
  resistance = 300.0
  grip = 2.0
  velocity = Vector2(0.0, 0.0)
  mass = 750
  brakeForce = 3000
  rotationSpeed = 200

  powerFactor = 0
  keys = dict(left=False, right=False, up=False)

  def __init__(self, *args, **kwargs):
    super().__init__(img=kwargs.get("img"))
    self.gameWindow = kwargs.get("win")

    self.key_handler = key.KeyStateHandler()
    self.x = self.gameWindow.width / 2
    self.y = self.gameWindow.height / 2
    
  def getAngleVector(self):
    angle = radians((self.rotation + 180) % 360)

    return Vector2(
      round(cos(angle), 4),
      round(-sin(angle), 4)
    )
  
  def getSpeed(self):
    v = self.velocity

    return round(sqrt(v.x * v.x + v.y * v.y), 4)
  
  def getPower(self):
    if (self.key_handler[key.UP]):
      return self.power
    else:
      return 0

  def getTraction(self):
    return self.getAngleVector() * self.getPower()
  
  def getBrake(self):
    brake = self.brakeForce if self.key_handler[key.DOWN] else 0

    return self.getAngleVector() * -brake
        
  def getDrag(self):
    speed = self.getSpeed()
    v = self.velocity
    drag = self.drag

    return Vector2(
      round(-(drag * v.x * speed), 4),
      round(-(drag * v.y * speed), 4)
    )
  
  def getResistance(self):
    resistance = -self.resistance
    v = self.velocity

    if (self.key_handler[key.SPACE]):
      return (resistance - self.brakeForce) * v
    else:
      return resistance * v

  def getLongitudinalForce(self):
    return 100 * self.getTraction() + self.getDrag() + self.getResistance() + self.getBrake()
  
  def getAcceleration(self):
    return self.getLongitudinalForce() / self.mass
  
  def getSlipRatio(self):
    angularVelocity = self.getAngleVector()
    wheelRadius = .65
    speed = self.getSpeed()

    print (angularVelocity * wheelRadius - speed) / speed
    return (angularVelocity * wheelRadius - speed) / speed
  
  def updateVelocity(self, dt):
    self.velocity = self.velocity + dt * self.getAcceleration()
  
  def updatePosition(self, dt):
    posV = Vector2(self.x, self.y)
    newposV = posV + dt * self.velocity

    self.x = newposV.x
    self.y = newposV.y

    outMargin = 20

    if (self.x <= 0 - outMargin and self.velocity.x < 0):
      self.x = self.gameWindow.width + outMargin
    elif (self.x >= self.gameWindow.width + outMargin and self.velocity.x > 0):
      self.x = 0 - outMargin

    if (self.y <= 0 - outMargin and self.velocity.y < 0):
      self.y = self.gameWindow.height + outMargin
    elif (self.y >= self.gameWindow.height + outMargin and self.velocity.y > 0):
      self.y = 0 - outMargin
  
  def updateAngle(self, dt):
    if (self.key_handler[key.LEFT]):
      self.rotation -= self.rotationSpeed * dt

    if (self.key_handler[key.RIGHT]):
      self.rotation += self.rotationSpeed * dt
  
  def update(self, dt):
    if (self.getSpeed() < 1):
      self.velocity.x = 0
      self.velocity.y = 0

    self.updateAngle(dt)
    self.updateVelocity(dt)
    self.updatePosition(dt)

    if (self.key_handler[key.X]):
      self.x = self.gameWindow.width / 2
      self.y = self.gameWindow.height / 2
      self.velocity.x = 0
      self.velocity.y = 0
      self.rotation = 0