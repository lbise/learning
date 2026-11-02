import sys; sys.path.insert(0, "/home/leo/learning/gamedev/assets/tools")
from blender_render import *
reset_scene(); ground()
bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0.5)); c = bpy.context.active_object
c.data.materials.append(material("Wood", (0.4,0.22,0.1))); wire_overlay(c)
camera((2.2,-2.8,1.8), (0,0,0.4)); render("/tmp/test_render.png")
