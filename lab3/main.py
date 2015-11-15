#! /usr/bin/env python
# -*- coding: utf-8 -*

from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight
from panda3d.core import AmbientLight
from panda3d.core import LightAttrib
from panda3d.core import LVector3
from panda3d.core import NodePath
from panda3d.core import Vec3
from panda3d.core import Point3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from math import atan2
from math import cos
from math import sin
import sys

HIGHLIGHT = (0, 1, 1, 1)
STANDART = (1, 1, 1, 1)
SPEED = 5

class Balls(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    # exit on esc
    self.accept('escape', sys.exit)
    # disable standart mouse based camera control
    self.disableMouse()
    #self.useDrive()
    #self.oobe()
    # set camera position
    #
    #self.camera.setPos(15, 0, 10)
    #self.camera.lookAt(0, 0, 0)
    self.camera.setPosHpr(0, -12, 12, 0, -35, 0)
    #
    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -9.81))
    self.taskMgr.add(self.updateWorld, 'updateWorld')
    self.setupLight()
    self.makePlane()
    self.accept('mouse1', self.pickBall)
    self.accept('mouse3', self.releaseBall)

    cnt = 3
    for num in xrange(cnt):
      self.makeBall(num, (num, num, 2*(num + 1)))
    self.picked = set([])

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
    self.world.doPhysics(dt, 1, 1. / 60.)
    return task.cont

  def rayCollision(self):
    if self.mouseWatcherNode.hasMouse():
      mouse = self.mouseWatcherNode.getMouse()
      pointFrom, pointTo = Point3(), Point3()
      self.camLens.extrude(mouse, pointFrom, pointTo)
      pointFrom = render.getRelativePoint(self.cam, pointFrom)
      pointTo = render.getRelativePoint(self.cam, pointTo)
      return self.world.rayTestClosest(pointFrom, pointTo)
    return None

  def pickBall(self):
      picked = self.rayCollision()
      if picked and 'ball' in picked.getNode().getName():
        self.picked.add(picked.getNode().getName())
        NodePath(picked.getNode().getChild(0).getChild(0)).setColor(HIGHLIGHT)

  def releaseBall(self):
    picked = self.rayCollision()
    if picked:
      x, y, z = picked.getHitPos()
      bodies = self.world.getRigidBodies()
      for elem in bodies:
        name = elem.getName()
        if name in self.picked:
          # apply some physics
          node = NodePath(elem.getChild(0).getChild(0))
          node_x, node_y, node_z = node.getPos(render)
          ix = (x - node_x)
          iy = (y - node_y)
          dir = atan2(iy, ix)
          dx, dy = SPEED * cos(dir), SPEED * sin(dir)
          elem.applyCentralImpulse(LVector3(dx, dy, z))
          node.setColor(STANDART)
      self.picked = set([])

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
    node.setDeactivationEnabled(False)
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
