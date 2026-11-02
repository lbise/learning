"""Lesson 15: an example forest blockout (grey boxes), seen from above and through the game camera.
Blender +Y = "north" = Godot -Z (up the screen). Run: blender -b --factory-startup --python assets/tools/lesson0015_blockout.py
"""
import sys; sys.path.insert(0, "/home/leo/learning/gamedev/assets/tools")
from blender_render import *
import math
OUT = "/home/leo/learning/gamedev/assets/img/0015/"
reset_scene()
bpy.context.scene.view_settings.view_transform = "Standard"   # AgX desaturates flat blockout colours
s = bpy.context.scene; s.render.resolution_x, s.render.resolution_y = 1100, 900
M = {k: material(k, c) for k, c in {"Ground": (0.7, 0.72, 0.68), "Path": (0.88, 0.8, 0.62), "Trunk": (0.3, 0.3, 0.33),
     "Water": (0.25, 0.5, 0.9), "Hill": (0.55, 0.55, 0.57), "Landmark": (0.85, 0.62, 0.35), "Carrot": (1.0, 0.45, 0.05),
     "Rabbit": (0.97, 0.97, 0.97), "Bridge": (0.5, 0.42, 0.34)}.items()}
objs = []
def box(name, size, loc, mat, rot_z=0.0, rot_x=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(rot_x, 0, rot_z)); o = bpy.context.active_object
    o.name = name; o.scale = size; o.data.materials.append(M[mat]); objs.append(o); return o
def cyl(name, r, h, loc, mat, verts=8):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=(loc[0], loc[1], loc[2] + h / 2))
    o = bpy.context.active_object; o.name = name; o.data.materials.append(M[mat]); objs.append(o); return o
carrot_spots = []
def cone(loc):
    carrot_spots.append(loc)
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.0, radius2=0.25, depth=0.8, location=(loc[0], loc[1], loc[2] + 0.4))
    o = bpy.context.active_object; o.data.materials.append(M["Carrot"]); objs.append(o)

box("Ground", (90, 90, 1), (0, 0, -0.5), "Ground")
# path: a few flat strips (slightly above ground), winding north
path = [(0, -26), (-4, -16), (1, -7), (0, 0), (0, 7), (0, 10), (6, 16), (0, 24)]
for (x0, y0), (x1, y1) in zip(path, path[1:]):
    L = math.hypot(x1 - x0, y1 - y0); a = math.atan2(y1 - y0, x1 - x0)
    box("Path", (L + 3, 3.5, 0.04), ((x0 + x1) / 2, (y0 + y1) / 2, 0.02), "Path", rot_z=a)
# start meadow + central clearing + final clearing (wider path patches)
for c, r in (((0, -26), 5), ((0, 0), 7), ((0, 24), 6)):
    cyl("Clearing", r, 0.05, (c[0], c[1], 0), "Path", verts=16)
# stream across the map at y = 7..9.5, with a bridge on the path
box("Stream", (90, 2.5, 0.06), (0, 8.25, 0.03), "Water")
box("Bridge", (3.5, 3.2, 0.3), (0, 8.25, 0.15), "Bridge")
# hill east of the path with a ramp
box("Hill", (8, 8, 1.0), (12, 16, 0.5), "Hill")
box("Ramp", (4.5, 3, 0.2), (6.6, 16, 0.42), "Hill", rot_z=0, rot_x=0).rotation_euler = (0, math.radians(-12.5), 0)
# landmark: big "well" block in the central clearing, visible from the start
cyl("Well", 1.6, 1.4, (0, 2, 0), "Landmark", verts=12)
box("WellRoof", (4.2, 3.2, 0.5), (0, 2, 3.3), "Landmark")
for x in (-1.8, 1.8): box("WellPost", (0.3, 0.3, 3.1), (x, 2, 1.55), "Landmark")
# trees: trunks beside the path, never between the path and the (south) camera at the start
import random; random.seed(4)
trees = [(-9, -20), (-10, -12), (5, -18), (7, -11), (-8, -4), (6, -2), (-9, 3), (8, 4), (-7, 13), (-4, 18), (-10, 20),
         (4, 26), (-6, 27), (14, 24), (18, 10), (-16, -6), (-15, 12), (14, -14), (-14, -24), (10, -25), (17, 2), (-18, 22)]
for t in trees: cyl("Trunk", random.uniform(0.45, 0.7), random.uniform(4, 6), (t[0], t[1], 0), "Trunk")
# carrots: a breadcrumb trail every ~5 m, a reward on the hill, one behind the landmark, a bunch at the end
for c in [(-2, -21), (-3, -15), (-1, -10), (1, -5), (0, -2.5), (0, 5), (0, 11.5), (3, 13.5), (12, 15), (13, 18), (2, 20), (-1, 24), (1, 25), (0, 26)]:
    cone((c[0], c[1], 1.0 if 8 <= c[0] <= 16 and 12 <= c[1] <= 20 else 0))
cone((0, 4.5, 0))
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45, location=(0, -26, 0.5)); rb = bpy.context.active_object; rb.data.materials.append(M["Rabbit"]); rb.scale = (1, 1, 1.3); objs.append(rb)

clear_temp()
clear_temp(); s.render.resolution_x = s.render.resolution_y = 1000
markers = []
for c in carrot_spots:   # map view only: bigger orange dots so the trail is readable
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.7, depth=0.1, location=(c[0], c[1], c[2] + 2.5))
    m = bpy.context.active_object; m.data.materials.append(M["Carrot"]); markers.append(m)
s.display.shading.light = "FLAT"
camera((0, 0, 60), (0, 0.001, 0), ortho_scale=64); render(OUT + "01-top.png")
s.display.shading.light = "STUDIO"
for m in markers: bpy.data.objects.remove(m, do_unlink=True)
# the game camera: offset (0, back 8, up 6) from the rabbit, vertical FOV 75 like Godot's default
def game_view(name, rabbit_xy):
    clear_temp(); rx, ry = rabbit_xy
    cam = camera((rx, ry - 8, 6), (rx, ry, 0.5)); cam.data.sensor_fit = 'VERTICAL'; cam.data.angle_y = math.radians(75)
    s.render.resolution_x, s.render.resolution_y = 1280, 720; render(OUT + name); s.render.resolution_x, s.render.resolution_y = 1100, 900
game_view("02-view-start.png", (0, -26))
game_view("03-view-clearing.png", (0, -2))
# the trap: a tree between camera and path hides the rabbit
cyl("BadTree", 0.6, 5, (0, -30.5, 0), "Trunk")
game_view("04-tree-hides-rabbit.png", (0, -26))
