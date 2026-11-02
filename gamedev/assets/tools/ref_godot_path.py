"""Reference sheet diagram: blocking out a winding path from flat strips + discs. Top view, 3 stages.
Run: blender -b --factory-startup --python assets/tools/ref_godot_path.py
"""
import sys; sys.path.insert(0, "/home/leo/learning/gamedev/assets/tools")
from blender_render import *
import math
OUT = "/home/leo/learning/gamedev/assets/img/ref/"
import os; os.makedirs(OUT, exist_ok=True)
def scene():
    reset_scene(); s = bpy.context.scene
    s.view_settings.view_transform = "Standard"; s.display.shading.light = "FLAT"
    s.render.resolution_x, s.render.resolution_y = 600, 600
    bpy.ops.mesh.primitive_plane_add(size=40); g = bpy.context.active_object; g.data.materials.append(material("G", (0.7, 0.72, 0.68)))
def strip(x0, y0, x1, y1, col=(0.86, 0.76, 0.55)):
    L = math.hypot(x1 - x0, y1 - y0); a = math.atan2(y1 - y0, x1 - x0)
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, 0.02), rotation=(0, 0, a))
    o = bpy.context.active_object; o.scale = (L, 3, 0.02); o.data.materials.append(material("S%.2f" % col[1], col)); return o
def disc(x, y, r=1.6, col=(0.86, 0.76, 0.55)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=r, depth=0.02, location=(x, y, 0.03)); bpy.context.active_object.data.materials.append(material("D", col))
pts = [(0, -9), (0, -1), (5, 6)]
for name, stage in (("path-1-strip.png", 1), ("path-2-turn.png", 2), ("path-3-disc.png", 3)):
    scene()
    strip(*pts[0], *pts[1])
    if stage >= 2: strip(*pts[1], *pts[2], col=(0.92, 0.66, 0.4) if stage == 2 else (0.86, 0.76, 0.55))
    if stage >= 3: disc(*pts[1])
    camera((1.5, -1.5, 40), (1.5, -1.499, 0), ortho_scale=22); render(OUT + name)
