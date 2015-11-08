import bge
from mathutils import Vector
from mathutils import geometry

import bpy

def mouse2world():
  cont = bge.logic.getCurrentController()
  mouse_over = cont.sensors['mouse_over']
  
  ray_p0 = mouse_over.raySource
  ray_p1 = mouse_over.rayTarget

  intersection = geometry.intersect_line_plane(ray_p0, ray_p1, Vector((0, 0, 0)), Vector((0, 0, 1)))
  # As alnernative we can use intersect_line_sphere.
  # ref: https://www.blender.org/api/blender_python_api_2_63_17/mathutils.geometry.html
  return intersection

def main():
  bge.render.showMouse(1)
  keyboard = bge.logic.keyboard
  mouse = bge.logic.mouse
  scene = bge.logic.getCurrentScene()
  JUST_ACTIVATED = bge.logic.KX_INPUT_JUST_ACTIVATED
  
  # spawn new ball
  if keyboard.events[bge.events.SPACEKEY] == JUST_ACTIVATED:
    ball = scene.addObject('Sphere')
    ball.applyForce((0, 300, 0), True)
    print(scene.objects)
  if mouse.events[bge.events.RIGHTMOUSE] == JUST_ACTIVATED:
    pos = mouse2world()
    if pos:
      dist = (scene.objects['Sphere'].worldPosition - pos).length
      radius = bpy.data.objects['Sphere'].game.radius
      if dist < radius:
        print('You select ball! Gratz!')
      else:
        print('You don\'t select ball :(')
        print(dist, radius)

main()
