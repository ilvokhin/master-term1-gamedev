#! /usr/bin/env python
# -*- coding: utf-8 -*

from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight
from panda3d.core import AmbientLight
from panda3d.core import LightAttrib
from panda3d.core import LVector3
from panda3d.core import NodePath
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode

import sys

class Balls(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    # exit on esc
    self.accept('escape', sys.exit)
    # disable standart mouse based camera control
    self.disableMouse()
    # set camera position
    camera.setPosHpr(0, -12, 12, 0, -35, 0)
    #
    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -9.81))
    self.taskMgr.add(self.updateWorld, 'updateWorld')
    self.setupLight()
    self.makePlane()
    cnt = 3
    for num in xrange(cnt):
      self.makeBall(num, (num, num, 2*(num + 1)))

  def setupLight(self):
    ambientLight = AmbientLight("ambientLight")
    ambientLight.setColor((.8, .8, .8, 1))
    directionalLight = DirectionalLight("directionalLight")
    directionalLight.setDirection(LVector3(0, 45, -45))
    directionalLight.setColor((0.2, 0.2, 0.2, 1))
    render.setLight(render.attachNewNode(directionalLight))
    render.setLight(render.attachNewNode(ambientLight))

  def updateWorld(self, task):
    dt = globalClock.getDt()
    # bug #1455084, simple doPhysics(dt) does nothing
    # looks like fixed already
    self.world.doPhysics(dt, 5, 1. / 180.)
    return task.cont

  def makePlane(self):
    shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
    node = BulletRigidBodyNode('plane')
    node.addShape(shape)
    physics = render.attachNewNode(node)
    physics.setPos(0, 0, 0)
    self.world.attachRigidBody(node)
    model = loader.loadModel('models/square')
    model.setScale(10, 10, 10)
    model.reparentTo(physics)

  def makeBall(self, num, pos = (0, 0, 0)):
    shape = BulletSphereShape(0.5)
    node = BulletRigidBodyNode('ball_' + str(num))
    node.setMass(1.0)
    node.setRestitution(.9)
    node.addShape(shape)
    physics = render.attachNewNode(node)
    physics.setPos(*pos)
    self.world.attachRigidBody(node)
    model = loader.loadModel('models/ball')
    model.reparentTo(physics)

def main():
  balls = Balls()
  balls.run()

if __name__ == "__main__":
  main()
