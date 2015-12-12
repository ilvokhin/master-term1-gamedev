#! /usr/bin/env python
# -*- coding: utf-8 -*

# Based on Panda3D infinite-tunnel sample.

from direct.showbase.ShowBase import ShowBase
from direct.interval.MetaInterval import Sequence
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func
from panda3d.core import LPoint3f
from panda3d.core import LVector3f
from panda3d.core import Fog
from random import randint
from random import uniform
from random import choice
import sys

TUNNEL_CNT = 4
TUNNEL_SEGMENT_LENGTH = 50
TUNNEL_TIME = 2
TUNNEL_CENTER = (0, 0, 2)
TUNNEL_RADIUS = 1.3

SPHERE_SPEED = 5

CRYSTALS_CNT = 15
DELTA = 1

class Tunnel(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    base.disableMouse()
    self.camera.setPosHpr(0, 0, 10, 0, -90, 0)
    self.setBackgroundColor(0, 0, 0)
    
    self.fog = Fog('distanceFog')
    self.fog.setColor(0, 0, 0)
    self.fog.setExpDensity(.08)
    render.setFog(self.fog)

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
    self.makeTunnel()
    self.makeSphere()
    self.continueTunnel()
    #
    self.crystals = []
    for _ in xrange(CRYSTALS_CNT):
      self.makeRandomCrystal(randint(0, TUNNEL_CNT - 1))
    #
    taskMgr.add(self.moveSphere, 'moveSphere')

  def makeTunnel(self):
    self.tunnel = [None] * TUNNEL_CNT
    for x in range(TUNNEL_CNT):
      self.tunnel[x] = loader.loadModel('models/tunnel')
      if x == 0:
        self.tunnel[x].reparentTo(render)
      else:
        self.tunnel[x].reparentTo(self.tunnel[x - 1])
      self.tunnel[x].setPos(0, 0, -TUNNEL_SEGMENT_LENGTH)

  def makeSphere(self):
    self.sphere = loader.loadModel('models/alice-shapes--sphere-highpoly/sphere-highpoly.egg')
    self.sphere.reparentTo(render)
    self.sphere.setScale(0.07)
    self.sphere.setZ(2)

  def makeRandomCrystal(self, tun):
    crystal = loader.loadModel('models/bvw-f2004--purplecrystal/purplecrystal.egg')
    crystal.reparentTo(self.tunnel[tun])
    crystal.setScale(0.1)
    pos = ['rx', '-rx', 'ry', 'down', 'up']
    rnd = choice(pos)
    Z = randint(0, 10)
    if rnd == 'rx':
      R = randint(45, 90)
      X = uniform(-2, 6)
      crystal.setR(R)
      crystal.setX(X)
    elif rnd == '-rx':
      R = randint(45, 90)
      X = uniform(-2, 8)
      crystal.setR(-R)
      crystal.setX(-X)
    elif rnd == 'ry':
      R = randint(45, 120)
      Y = uniform(2, 6)
      crystal.setR(R)
      crystal.setY(Y)
    elif rnd == '-py':
      R = randint(45, 120)
      Y = uniform(3, 8)
      crystal.setR(-R)
      crystal.setY(-Y)
    elif rnd == 'down':
      Y = uniform(1, 6)
      P = randint(70, 120)
      crystal.setY(-Y)
      crystal.setP(P)
    elif rnd == 'up':
      Y = uniform(-1, 6)
      P = randint(-130, -60)
      crystal.setY(Y)
      crystal.setP(P)
      
    crystal.setZ(Z)
    self.crystals.append(crystal)
    
  def continueTunnel(self):
    self.tunnel = self.tunnel[1:] + self.tunnel[0:1]
    self.tunnel[0].setZ(0)
    self.tunnel[0].reparentTo(render)
    self.tunnel[0].setScale(.155, .155, .305)
    self.tunnel[3].reparentTo(self.tunnel[2])
    self.tunnel[3].setZ(-TUNNEL_SEGMENT_LENGTH)
    self.tunnel[3].setScale(1)

    for child in self.tunnel[3].getChildren():
      if child.getName() == 'purplecrystal.egg':
        self.crystals.remove(child)
        child.removeNode()
        self.makeRandomCrystal(3)

    self.tunnelMove = Sequence \
    (
      LerpFunc \
      (
        self.tunnel[0].setZ,
        duration=TUNNEL_TIME,
        fromData=0,
        toData=TUNNEL_SEGMENT_LENGTH * .305
      ),
      Func(self.continueTunnel)
    )
    self.tunnelMove.start()

  def setKey(self, key, value):
    self.keyMap[key] = value

  def moveSphere(self, task):
    dt = globalClock.getDt()
    addVec = LVector3f(0, 0, 0)
    if self.keyMap['left']:
      addVec[0] -= SPHERE_SPEED * dt
    elif self.keyMap['right']:
      addVec[0] += SPHERE_SPEED * dt
    elif self.keyMap['up']:
      addVec[1] += SPHERE_SPEED * dt
    elif self.keyMap['down']:
      addVec[1] -= SPHERE_SPEED * dt
   
    if ((self.sphere.getPos() + addVec) - LPoint3f(TUNNEL_CENTER)).length() < TUNNEL_RADIUS:
      self.sphere.setPos(self.sphere.getPos() + addVec)

    return task.cont

def main():
  tunnel = Tunnel()
  tunnel.run()

if __name__ == "__main__":
  main()
