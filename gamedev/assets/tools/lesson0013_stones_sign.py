"""Lesson 13 exercises: stone ring for the campfire (well Part 1 skills), village sign (well Part 2 skills).
Run: blender -b --factory-startup --python assets/tools/lesson0013_stones_sign.py
"""
import sys; sys.path.insert(0, "/home/leo/learning/gamedev/assets/tools")
from blender_render import *
import math, random, mathutils
OUT = "/home/leo/learning/gamedev/assets/img/0013/"
random.seed(7)

def shot(name, cam, objs, ortho=None, markers=()):
    clear_temp()
    for o in list(bpy.data.objects):
        if o.name.startswith("_m_"): bpy.data.objects.remove(o, do_unlink=True)
    for o in objs: wire_overlay(o)
    sel = material("_Sel", SELECT)
    for loc in markers:   # orange 3-axis cross = an Empty (empties don't render)
        for rot in ((0, 0, 0), (math.pi / 2, 0, 0), (0, math.pi / 2, 0)):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.5, location=loc, rotation=rot)
            c = bpy.context.active_object; c.name = "_m_empty"; c.data.materials.append(sel)
    camera(*cam, ortho_scale=ortho); render(OUT + name)

def stone(size, loc, rot_x=0.0, seed=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.active_object
    o.data.materials.append(material("Stone", (0.55, 0.55, 0.57), 0, 0.9))
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.scale(bm, vec=size, verts=bm.verts)                       # S then Ctrl+A Scale: size baked into the mesh
    bmesh.ops.bevel(bm, geom=bm.edges[:], offset=min(size) * 0.18, segments=1, affect='EDGES')   # Ctrl+B
    for no in ((1, 0, 0), (0, 0, 1), (0, 1, 0)):                          # three loop cuts
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0), plane_no=no)
    rnd = random.Random(seed)
    for v in bm.verts: v.co += mathutils.Vector([rnd.uniform(-1, 1) * 0.015 for _ in range(3)])   # Randomize
    bm.to_mesh(o.data); bm.free(); o.rotation_euler.x = rot_x
    return o

# ================= Exercise A: stone ring =================
reset_scene(); ground(16)
s1 = stone((0.28, 0.2, 0.16), (0, 0, 0.08), seed=1)
shot("a1-one-stone.png", ((0.7, -0.9, 0.55), (0, 0, 0.08)), [s1])
L = 3.46   # circumference for a 0.55 m ring = 2*pi*0.55
stones = [s1]; x = 0.0
s1.location.x = 0.14
shapes = [(0.28, 0.2, 0.16), (0.18, 0.2, 0.15), (0.24, 0.18, 0.18)]
while x < L - 0.4:
    x += 0.26 + random.uniform(-0.03, 0.02)
    sz = shapes[len(stones) % 3]
    stones.append(stone(sz, (x + 0.14, 0, sz[2] / 2), rot_x=random.choice((0, math.pi / 2)) * 0, seed=len(stones) + 1))
LINE = ((1.73, -6.5, 2.4), (1.73, 0, 0.1))
shot("a2-line.png", LINE, stones)
# join (Ctrl+J) into the first stone, whose origin is at the start of the line
for o in bpy.context.scene.objects: o.select_set(o in stones)
bpy.context.view_layer.objects.active = s1
s1.location.x = 0.14; bpy.ops.object.join(); ring = bpy.context.active_object; ring.name = "StoneRing"
bpy.context.scene.cursor.location = (0, 0, 0); bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
m = ring.modifiers.new("SimpleDeform", 'SIMPLE_DEFORM'); m.deform_method = 'BEND'; m.deform_axis = 'Z'; m.angle = math.radians(360)
shot("a3-bent-ring.png", ((1.6, -1.6, 2.0), (0, 0.55, 0)), [ring])
d = ring.modifiers.new("Decimate", 'DECIMATE'); d.ratio = 0.5
ring.location.y = -0.55          # move the ring so it surrounds the fire at the origin
# the Lesson 11 campfire, for context
bark, flame = material("Bark", (0.35, 0.2, 0.1), 0, 0.9), material("Flame", (1.0, 0.45, 0.05))
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.06, depth=0.6, location=(0.3, 0, 0.06), rotation=(0, math.pi / 2, 0))
log = bpy.context.active_object; log.data.materials.append(bark); logs = [log]
for i in range(1, 5):
    c = log.copy(); bpy.context.collection.objects.link(c); c.matrix_world = mathutils.Matrix.Rotation(math.radians(72 * i), 4, 'Z') @ log.matrix_world; logs.append(c)
bpy.context.view_layer.update()
for l in logs:
    mw = l.matrix_world.copy(); loc = mw.to_translation(); ax = (mw.to_3x3() @ mathutils.Vector((0, 1, 0))).normalized()
    l.matrix_world = mathutils.Matrix.Translation(loc) @ mathutils.Matrix.Rotation(math.radians(35), 4, ax) @ mathutils.Matrix.Translation(-loc) @ mw
    l.location.z += 0.17
bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.16, depth=0.45, location=(0, 0, 0.225)); f = bpy.context.active_object; f.data.materials.append(flame)
shot("a4-campfire-ring.png", ((1.7, -2.1, 1.3), (0, 0, 0.15)), [ring] + logs + [f])

# ================= Exercise B: village sign =================
reset_scene(); ground(16)
wood, plank = material("Wood", (0.42, 0.25, 0.12), 0, 0.8), material("Plank", (0.62, 0.45, 0.28), 0, 0.8)
def beam(dims, loc, notches=(), mat=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.active_object; o.data.materials.append(mat or wood)
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.scale(bm, vec=dims, verts=bm.verts)
    for z0, (sx, sy) in notches:   # a notch: two loop cuts close together, the corner between them pushed in
        for z in (z0 - 0.05, z0 + 0.05):
            bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, z), plane_no=(0, 0, 1))
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, z0), plane_no=(0, 0, 1))
        for v in bm.verts:
            if abs(v.co.z - z0) < 1e-4 and v.co.x * sx > 0 and v.co.y * sy > 0:
                v.co.x -= sx * 0.035; v.co.y -= sy * 0.035
    bm.to_mesh(o.data); bm.free()
    return o
post = beam((0.14, 0.14, 1.6), (0.6, 0, 0.8), notches=((0.35, (1, -1)), (-0.25, (-1, -1))))
shot("b1-post-notches.png", ((3.4, -4.4, 1.6), (0.6, 0, 0.8)), [post])
bpy.context.scene.cursor.location = (0, 0, 0)
empty = bpy.data.objects.new("MirrorEmpty", None); empty.empty_display_type = 'PLAIN_AXES'; bpy.context.collection.objects.link(empty)
mm = post.modifiers.new("Mirror", 'MIRROR'); mm.mirror_object = empty
shot("b2-mirrored-post.png", ((1.8, -5.2, 1.8), (0, 0, 0.8)), [post], markers=[(0, 0, 0.3)])
top = beam((1.6, 0.16, 0.14), (0, 0, 1.55), notches=())
top.rotation_euler.y = math.radians(2)
board = beam((1.0, 0.05, 0.4), (0, -0.09, 1.15), mat=plank)
SIGN = ((2.2, -5.0, 1.9), (0, 0, 0.85))
shot("b3-sign-done.png", SIGN, [post, top, board])
