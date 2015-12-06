#! /usr/bin/env python
# -*- coding: utf-8 -*

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionHandlerQueue
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionSphere
from panda3d.core import CollisionNode
from panda3d.core import TextNode
from panda3d.core import Point3
from panda3d.core import Fog

from random import choice
from random import randint
import sys

SHIP_SPEED = 25
SHIP_SPHERE_RADIUS = 10
MIN_X = -100
MAX_X = 100

MIN_Z = -100
MAX_Z = 100

START_X = 0
START_Y = 0
START_Z = -10

TURN_SPEED = 10

ASTEROID_MAX_CNT = 75
ASTEROID_SPEED = 15
ASTEROID_SPHERE_RADIUS = 3
ASTEROID_SPAWN_MIN_Y = 320
ASTEROID_SPAWN_MAX_Y = 520
ASTEROID_ROTATE_MIN = -10
ASTEROID_ROTATE_MAX = 10
ASTEROID_SHAPES = [
  'models/alice-shapes--dodecahedron/dodecahedron.egg',
  'models/alice-shapes--icosahedron/icosahedron.egg',
  'models/alice-shapes--octahedron/octahedron.egg'
]

DEBUG = False

class SpaceFlight(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    self.text = OnscreenText \
    (
      parent = base.a2dBottomCenter,
      align=TextNode.ARight,
      fg=(1, 1, 1, 1),
      pos=(0.2, 1.),
      scale=0.1,
      shadow=(0, 0, 0, 0.5)
    )
    self.setBackgroundColor(0, 0, 0)
    self.disableMouse()
    self.fog = Fog('distanceFog')
    self.fog.setColor(0, 0, 0)
    self.fog.setExpDensity(.002)
    #
    self.queue = CollisionHandlerQueue()
    self.trav = CollisionTraverser('traverser')
    base.cTrav = self.trav
    self.loadSky()
    self.reloadGame()

    self.keyMap = {'left' : 0, 'right' : 0, 'up' : 0, 'down' : 0}
    self.gamePause = False
    #
    self.accept('escape', sys.exit)
    self.accept('p', self.pause)
    self.accept('r', self.reloadGame)
    self.accept('arrow_left', self.setKey, ['left', True])
    self.accept('arrow_right', self.setKey, ['right', True])
    self.accept('arrow_up', self.setKey, ['up', True])
    self.accept('arrow_down', self.setKey, ['down', True])
    self.accept('arrow_left-up', self.setKey, ['left', False])
    self.accept('arrow_right-up', self.setKey, ['right', False])
    self.accept('arrow_up-up', self.setKey, ['up', False])
    self.accept('arrow_down-up', self.setKey, ['down', False])
    #
    taskMgr.add(self.moveShip, 'moveShip')
    taskMgr.add(self.moveAsteroids, 'moveAsteroids')
    taskMgr.add(self.handleCollisions, 'handleCollisions')
    #
    if DEBUG:
      self.trav.showCollisions(render)
      render.find('**/ship_collision').show()
      for asteroid in render.findAllMatches('**/asteroid_collision*'):
        asteroid.show()

  def loadSky(self):
    self.sky = loader.loadModel('models/solar_sky_sphere.egg.pz')
    self.sky_tex = loader.loadTexture('models/stars_1k_tex.jpg')
    self.sky.setTexture(self.sky_tex, 1)
    self.sky.reparentTo(render)
    self.sky.setScale(500)

  def loadShip(self):
    self.ship = loader.loadModel('models/alice-scifi--fighter/fighter.egg')
    self.ship.reparentTo(render)
    self.ship.setPos(START_X, START_Y, START_Z)
    self.ship.setScale(0.25)
    # add some physics
    ship_col = self.ship.attachNewNode(CollisionNode('ship_collision'))
    col_sphere = CollisionSphere(START_X, START_Y, 0, SHIP_SPHERE_RADIUS)
    ship_col.node().addSolid(col_sphere)
    self.trav.addCollider(ship_col, self.queue)

  def spawnAsteroid(self):
    asteroid = loader.loadModel(choice(ASTEROID_SHAPES))
    asteroid_tex = loader.loadTexture('models/rock03.jpg')
    asteroid.setTexture(asteroid_tex, 1)
    asteroid.reparentTo(render)
    asteroid.setFog(self.fog)
    self.asteroids.append(asteroid)
    self.asteroids_rotation.append(randint(ASTEROID_ROTATE_MIN, ASTEROID_ROTATE_MAX))
    #
    num = len(self.asteroids) - 1
    asteroid_col = asteroid.attachNewNode(CollisionNode('asteroid_collision_%d' % num))
    col_sphere = CollisionSphere(0, 0, 0, ASTEROID_SPHERE_RADIUS)
    asteroid_col.node().addSolid(col_sphere)
    #
    asteroid.setX(randint(MIN_X, MAX_X))
    asteroid.setY(randint(ASTEROID_SPAWN_MIN_Y, ASTEROID_SPAWN_MAX_Y))
    asteroid.setZ(randint(MIN_Z, MAX_Z))

  def setKey(self, key, value):
    self.keyMap[key] = value
    if key in ['left', 'right'] and value == False:
      self.ship.setH(0)
    if key in ['up', 'down'] and value == False:
      self.ship.setP(0)

  def updateCamera(self):
    x, y, z = self.ship.getPos()
    self.camera.setPos(x, y - 40, z + 25)
    self.camera.lookAt(x, y, z + 10)

  def moveAsteroids(self, task):
    dt = globalClock.getDt()
    if not self.gamePause:
      for num, asteroid in enumerate(self.asteroids):
        asteroid.setY(asteroid.getY() - ASTEROID_SPEED * dt)
        rotation = self.asteroids_rotation[num]
        asteroid.setH(asteroid.getH() - rotation * ASTEROID_SPEED * dt)
        if asteroid.getY() < self.camera.getY() + 10:
          asteroid.setX(randint(MIN_X, MAX_X))
          asteroid.setY(randint(ASTEROID_SPAWN_MIN_Y, ASTEROID_SPAWN_MAX_Y))
          asteroid.setZ(randint(MIN_Z, MAX_Z))
    return task.cont

  def rollbackOnBoard(self, minPos, maxPos, getFunc, setFunc):
    if getFunc() < minPos:
      setFunc(minPos)
    if getFunc() > maxPos:
      setFunc(maxPos)

  def applyBound(self):
    self.rollbackOnBoard(MIN_X, MAX_X, self.ship.getX, self.ship.setX)
    self.rollbackOnBoard(MIN_Z, MAX_Z, self.ship.getZ, self.ship.setZ)

  def moveShip(self, task):
    dt = globalClock.getDt()
    if not self.gamePause:
      if self.keyMap['left']:
        self.ship.setX(self.ship.getX() - SHIP_SPEED * dt)
        self.ship.setH(TURN_SPEED)
      elif self.keyMap['right']:
        self.ship.setX(self.ship.getX() + SHIP_SPEED * dt)
        self.ship.setH(-TURN_SPEED)
      elif self.keyMap['up']:
        self.ship.setZ(self.ship.getZ() + SHIP_SPEED * dt)
        self.ship.setP(TURN_SPEED)
      elif self.keyMap['down']:
        self.ship.setZ(self.ship.getZ() - 5 * SHIP_SPEED * dt)
        self.ship.setP(-TURN_SPEED)

      self.sky.setP(self.sky.getP() - dt * 10)
      self.applyBound()
      self.updateCamera()

    return task.cont

  def handleCollisions(self, task):
    if not self.gamePause:
      for entry in self.queue.getEntries():
        node = entry.getFromNodePath()
        if node.getName() == 'ship_collision':
          self.gamePause = True
          self.text.setText('You lose :(')
    return task.cont

  def pause(self):
    self.gamePause = not self.gamePause

  def reloadGame(self):
    self.gamePause = False
    self.text.clearText()

    if hasattr(self, 'asteroids'):
      for asteroid in self.asteroids:
        asteroid.removeNode()

    self.asteroids = []
    self.asteroids_rotation = []

    if hasattr(self, 'ship'):
      self.ship.removeNode()

    self.loadShip()

    for _ in xrange(ASTEROID_MAX_CNT):
      self.spawnAsteroid()

def main():
  spaceFlight = SpaceFlight()
  spaceFlight.run()

if __name__ == '__main__':
  main()
