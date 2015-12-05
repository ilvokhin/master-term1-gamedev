#! /usr/bin/env python
# -*- coding: utf-8 -*

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3

import sys

SPACE_SPEED = 75
MIN_X = -65
MAX_X = 65
MIN_Z = -65
MAX_Z = 65

START_X = 0
START_Y = 0
START_Z = -10

class SpaceFlight(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    self.setBackgroundColor(0, 0, 0)
    self.disableMouse()
    #
    self.loadSky()
    self.loadShip()
    #
    self.keyMap = {'left' : 0, 'right' : 0, 'up' : 0, 'down' : 0}
    #
    self.accept('escape', sys.exit)
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

  def loadSky(self):
    self.sky = loader.loadModel('models/solar_sky_sphere.egg.pz')
    self.sky_tex = loader.loadTexture('models/stars_1k_tex.jpg')
    self.sky.setTexture(self.sky_tex, 1)
    self.sky.reparentTo(render)
    self.sky.setScale(150)

  def loadShip(self):
    self.ship = loader.loadModel('models/alice-scifi--fighter/fighter.egg')
    self.ship.reparentTo(render)
    self.ship.setPos(START_X, START_Y, START_Z)
    self.ship.setScale(0.25)

  def setKey(self, key, value):
    self.keyMap[key] = value

  def updateCamera(self):
    x, y, z = self.ship.getPos()
    self.camera.setPos(x, y - 40, z + 25)
    self.camera.lookAt(x, y, z + 10)

  def rollbackOnBoard(self, minPos, maxPos, getFunc, setFunc):
    if getFunc() < minPos:
      setFunc(minPos)
    if getFunc() > maxPos:
      setFunc(maxPos)

  def applyBound(self):
    self.rollbackOnBoard(MIN_X, MAX_X, self.ship.getX, self.ship.setX)
    self.rollbackOnBoard(MIN_Z, MAX_Z, self.ship.getZ, self.ship.setZ)

  def moveSky(self, task):
    dt = globalClock.getDt()
    self.sky.setY(self.sky.getY() - SKY_SPEED)

    return task.cont

  def moveShip(self, task):
    dt = globalClock.getDt()
    if self.keyMap['left']:
      self.ship.setX(self.ship.getX() - SPACE_SPEED * dt)
    elif self.keyMap['right']:
      self.ship.setX(self.ship.getX() + SPACE_SPEED * dt)
    elif self.keyMap['up']:
      self.ship.setZ(self.ship.getZ() + SPACE_SPEED * dt)
    elif self.keyMap['down']:
      self.ship.setZ(self.ship.getZ() - SPACE_SPEED * dt)

    self.applyBound()
    self.updateCamera()

    return task.cont

def main():
  spaceFlight = SpaceFlight()
  spaceFlight.run()

if __name__ == '__main__':
  main()
