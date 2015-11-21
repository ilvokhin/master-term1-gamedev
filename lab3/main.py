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
from panda3d.core import TransparencyAttrib
from panda3d.core import PandaNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from math import atan2
from math import cos
from math import sin
from functools import partial
from random import uniform
import sys

HIGHLIGHT = (0, 1, 1, 1)
STANDART = (1, 1, 1, 1)
SPEED = 5
ROTATE_SPEED = 10
SHAKE_SPEED = 15

class Balls(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    # exit on esc
    self.accept('escape', sys.exit)
    # disable standart mouse based camera control
    self.disableMouse()
    #base.useDrive()
    #base.useTrackball()
    # set camera position
    self.camera.setPos(0, -30, 25)
    self.camera.lookAt(0, 0, 0)
    #
    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -9.81))
    # debug
    debugNode = BulletDebugNode('Debug')
    debugNode.showWireframe(True)
    debugNode.showConstraints(True)
    debugNode.showBoundingBoxes(False)
    debugNode.showNormals(False)
    debugNP = render.attachNewNode(debugNode)
    #debugNP.show()
    #self.world.setDebugNode(debugNP.node())

    self.taskMgr.add(self.updateWorld, 'updateWorld')
    self.setupLight()
    # down
    self.makePlane(0, Vec3(0, 0, 1), (0, 0, 0), (0, 0, 0))
    # up
    self.makePlane(1, Vec3(0, 0, -1), (0, 0, 10), (0, 0, 0))
    # left
    self.makePlane(2, Vec3(1, 0, 0), (-5, 0, 5), (0, 0, 90))
    # right
    self.makePlane(3, Vec3(-1, 0, 0), (5, 0, 5), (0, 0, -90))
    # top
    self.makePlane(4, Vec3(0, 1, 0), (0, -5, 5), (0, 90, 0))
    # buttom
    self.makePlane(5, Vec3(0, -1, 0), (0, 5, 5), (0, -90, 0))

    self.accept('mouse1', self.pickBall)
    self.accept('mouse3', self.releaseBall)
    self.accept('arrow_up', partial(self.rotateCube, hpr = (0, ROTATE_SPEED, 0)))
    self.accept('arrow_down', partial(self.rotateCube, hpr = (0, -ROTATE_SPEED, 0)))
    self.accept('arrow_left', partial(self.rotateCube, hpr = (0, 0, -ROTATE_SPEED)))
    self.accept('arrow_right', partial(self.rotateCube, hpr = (0, 0, ROTATE_SPEED)))
    self.accept('space', self.shakeBalls)

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
      hits = self.world.rayTestAll(pointFrom, pointTo).getHits()
      return sorted(hits, key = lambda x: (x.getHitPos() - pointFrom).length())
    return []

  def pickBall(self):
      hits = self.rayCollision()
      for hit in hits:
        hit_node = hit.getNode()
        if 'ball' in hit_node.getName():
          self.picked.add(hit_node.getName())
          NodePath(hit_node.getChild(0).getChild(0)).setColor(HIGHLIGHT)

  def releaseBall(self):
    hits = self.rayCollision()
    if hits:
      for picked in hits:
        hit_node = picked.getNode()
        if 'ball' in hit_node.getName():
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

  def rotateCube(self, hpr = (0, 0, 0)):
    # h, p, r = z, x, y
    # FIXME: something completely wrong goes here
    # need some time to figure it out
    planes = render.findAllMatches('**/plane*')
    for plane in planes:
      oldParent = plane.getParent()
      pivot = render.attachNewNode('pivot')
      pivot.setPos(render, 0, 0, 5)
      plane.wrtReparentTo(pivot)
      pivot.setHpr(render, Vec3(hpr))
      if oldParent.getName() != 'render':
        oldParent.removeNode()

  def shakeBalls(self):
    balls = filter(lambda x: 'ball' in x.getName(), self.world.getRigidBodies())
    for ball in balls:
      dx = uniform(-SHAKE_SPEED, SHAKE_SPEED)
      dy = uniform(-SHAKE_SPEED, SHAKE_SPEED)
      dz = uniform(-SHAKE_SPEED, SHAKE_SPEED)
      ball.applyCentralImpulse(LVector3(dx, dy, dz))

  def makePlane(self, num, norm, pos, hpr):
    shape = BulletPlaneShape(norm, 0)
    node = BulletRigidBodyNode('plane_' + str(num))
    node.addShape(shape)
    physics = render.attachNewNode(node)
    physics.setPos(*pos)
    self.world.attachRigidBody(node)
    model = loader.loadModel('models/square')
    model.setScale(10, 10, 10)
    model.setHpr(*hpr)
    model.setTransparency(TransparencyAttrib.MAlpha)
    model.setColor(1, 1, 1, 0.25)
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
