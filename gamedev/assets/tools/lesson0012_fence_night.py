"""Lesson 12: fence with linked duplicates + glowing lanterns (Part 7), campfire at night (Part 8).
Run: blender -b --factory-startup --python assets/tools/lesson0012_fence_night.py
"""
import sys; sys.path.insert(0, "/home/leo/learning/gamedev/assets/tools")
from blender_render import *
import math, mathutils
OUT = "/home/leo/learning/gamedev/assets/img/0012/"

def glow_mat(name, color, strength):
    m = material(name, color)
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = (*color, 1); b.inputs["Emission Strength"].default_value = strength
    return m

def wb_shot(name, cam, objs):
    clear_temp()
    for o in objs: wire_overlay(o)
    camera(*cam); render(OUT + name)

def eevee_shot(name, cam, world_color, world_strength):
    clear_temp()
    s = bpy.context.scene; s.render.engine = 'BLENDER_EEVEE'
    w = s.world; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (*world_color, 1); bg.inputs[1].default_value = world_strength
    camera(*cam); render(OUT + name)
    s.render.engine = 'BLENDER_WORKBENCH'

# ======================= Exercise A: fence =======================
reset_scene(); ground(16)
wood = material("Wood", (0.42, 0.25, 0.12), 0, 0.8)
bpy.ops.mesh.primitive_cube_add(size=2); post = bpy.context.active_object; post.name = "Post"; post.data.materials.append(wood)
bm = bmesh.new(); bm.from_mesh(post.data)
bmesh.ops.scale(bm, vec=(0.05, 0.05, 0.5), verts=bm.verts); bmesh.ops.translate(bm, vec=(0, 0, 0.5), verts=bm.verts)
top = [f for f in bm.faces if f.normal.z > 0.9][0]
r = bmesh.ops.extrude_face_region(bm, geom=[top]); tv = [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]
bmesh.ops.translate(bm, vec=(0, 0, 0.1), verts=tv); bmesh.ops.scale(bm, vec=(0, 0, 1), space=mathutils.Matrix.Translation((0, 0, -1.1)), verts=tv)
bmesh.ops.remove_doubles(bm, verts=tv, dist=1e-4)
bm.to_mesh(post.data); bm.free()
ONE = ((2.2, -3.0, 1.6), (0, 0, 0.55))
wb_shot("a1-one-post.png", ONE, [post])
posts = [post]
for i in range(1, 5):
    d = post.copy(); d.location.x = i; d.name = f"Post.{i:03d}"; bpy.context.collection.objects.link(d); posts.append(d)   # Alt+D: d.data is post.data
rails = []
for z in (0.75, 0.35):
    bpy.ops.mesh.primitive_cube_add(size=2); rl = bpy.context.active_object; rl.name = "Rail"; rl.data.materials.append(wood)
    bm = bmesh.new(); bm.from_mesh(rl.data); bmesh.ops.scale(bm, vec=(2, 0.02, 0.04), verts=bm.verts); bmesh.ops.translate(bm, vec=(2, -0.07, z), verts=bm.verts); bm.to_mesh(rl.data); bm.free()
    rails.append(rl)
ROW = ((6.8, -5.4, 2.6), (2, 0, 0.5))
wb_shot("a2-row.png", ROW, posts + rails)
# experiment: move the tip of ONE post up -> all change
sel = material("_Sel", SELECT)
bm = bmesh.new(); bm.from_mesh(post.data)
tip = max(bm.verts, key=lambda v: v.co.z); tip.co.z += 0.2
bm.to_mesh(post.data); bm.free()
wb_shot("a3-edit-one-all-change.png", ROW, posts + rails)
bm = bmesh.new(); bm.from_mesh(post.data); tip = max(bm.verts, key=lambda v: v.co.z); tip.co.z -= 0.2; bm.to_mesh(post.data); bm.free()
# lanterns on posts 0, 2, 4 (one lantern + Alt+D), emission material
glow = glow_mat("LanternGlow", (1.0, 0.65, 0.2), 3.0)
bpy.ops.mesh.primitive_cube_add(size=0.14, location=(0, 0, 1.17)); lan = bpy.context.active_object; lan.name = "Lantern"; lan.data.materials.append(glow)
lans = [lan]
for x in (2, 4):
    d = lan.copy(); d.location.x = x; bpy.context.collection.objects.link(d); lans.append(d)
wb_shot("a4-lanterns.png", ROW, posts + rails + lans)
eevee_shot("a5-lanterns-glow.png", ROW, (0.12, 0.15, 0.28), 0.5)

# ======================= Exercise B: campfire at night =======================
reset_scene(); ground(16)
bark, stone = material("Bark", (0.35, 0.2, 0.1), 0, 0.9), material("Stone", (0.5, 0.5, 0.52), 0, 0.9)
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.06, depth=0.6, location=(0.3, 0, 0.06), rotation=(0, math.pi / 2, 0))
log = bpy.context.active_object; log.data.materials.append(bark); logs = [log]
for i in range(1, 5):
    d = log.copy(); bpy.context.collection.objects.link(d); d.matrix_world = mathutils.Matrix.Rotation(math.radians(72 * i), 4, 'Z') @ log.matrix_world; logs.append(d)
bpy.context.view_layer.update()
for l in logs:
    mw = l.matrix_world.copy(); loc = mw.to_translation(); ax = (mw.to_3x3() @ mathutils.Vector((0, 1, 0))).normalized()
    l.matrix_world = mathutils.Matrix.Translation(loc) @ mathutils.Matrix.Rotation(math.radians(35), 4, ax) @ mathutils.Matrix.Translation(-loc) @ mw
    l.location.z += 0.17
flame = material("Flame", (1.0, 0.45, 0.05))
bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.16, depth=0.45, location=(0, 0, 0.225)); f1 = bpy.context.active_object; f1.data.materials.append(flame)
for i in range(8):
    a = math.radians(45 * i)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.08, location=(0.55 * math.cos(a), 0.55 * math.sin(a), 0.04))
    s = bpy.context.active_object; s.scale = (1.2, 1, 0.7); s.data.materials.append(stone)
FIRE = ((1.7, -2.1, 1.1), (0, 0, 0.2))
eevee_shot("b1-day.png", FIRE, (0.55, 0.6, 0.7), 1.0)
# night: dark world
eevee_shot("b2-dark-world.png", FIRE, (0.02, 0.03, 0.08), 0.3)
# emission on the flame
fb = flame.node_tree.nodes["Principled BSDF"]; fb.inputs["Emission Color"].default_value = (1.0, 0.45, 0.05, 1); fb.inputs["Emission Strength"].default_value = 1.0
eevee_shot("b3-emissive-flame.png", FIRE, (0.02, 0.03, 0.08), 0.3)
# point light inside the fire
ld = bpy.data.lights.new("FireLight", 'POINT'); ld.color = (1.0, 0.55, 0.2); ld.energy = 60
lo = bpy.data.objects.new("FireLight", ld); lo.location = (0, 0, 0.3); bpy.context.collection.objects.link(lo)
eevee_shot("b4-light-inside-flame.png", FIRE, (0.02, 0.03, 0.08), 0.3)   # trap: the cone blocks it
lo.location = (0, 0, 0.6); ld.energy = 20
eevee_shot("b5-fire-light.png", FIRE, (0.02, 0.03, 0.08), 0.3)
