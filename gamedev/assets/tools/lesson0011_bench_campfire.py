"""Lesson 11 exercises: mirrored bench (Part 5 skills) and campfire (Part 6 skills). Renders step images.
Run: blender -b --factory-startup --python assets/tools/lesson0011_bench_campfire.py
"""
import sys; sys.path.insert(0, "/home/leo/learning/gamedev/assets/tools")
from blender_render import *
import math
OUT = "/home/leo/learning/gamedev/assets/img/0011/"

def shot(name, cam, objs, marker=None, ortho=None):
    global sel
    sel = material("_Sel", SELECT)
    clear_temp()
    for o in list(bpy.data.objects):
        if o.name.startswith("_m_"): bpy.data.objects.remove(o, do_unlink=True)
    for o in objs: wire_overlay(o)
    if marker:  # 3D cursor marker: small orange ring + dot
        bpy.ops.mesh.primitive_torus_add(major_radius=0.06, minor_radius=0.008, location=marker); t = bpy.context.active_object; t.name = "_m_ring"; t.data.materials.append(sel)
    camera(*cam, ortho_scale=ortho); render(OUT + name)

def hide_all_but(keep):
    for o in bpy.data.objects:
        if o.type == 'MESH' and not o.name.startswith("_"):
            o.hide_render = o not in keep

# ================= Exercise A: bench (mirror X+Y, clipping, X-ray selection) =================
reset_scene(); ground()
wood, sel = material("Wood", (0.45, 0.27, 0.12), 0, 0.8), material("_Sel", SELECT)
bpy.ops.mesh.primitive_cube_add(size=2); bench = bpy.context.active_object; bench.name = "Bench"; bench.data.materials.append(wood); bench.data.materials.append(sel)
BENCH = ((2.0, -2.4, 1.6), (0, 0, 0.3))
def bm_edit(fn):
    bm = bmesh.new(); bm.from_mesh(bench.data); fn(bm); bm.to_mesh(bench.data); bm.free()
# A1: seat 1.2 x 0.4 x 0.1, top at 0.5
bm_edit(lambda bm: (bmesh.ops.scale(bm, vec=(0.6, 0.2, 0.05), verts=bm.verts), bmesh.ops.translate(bm, vec=(0, 0, 0.45), verts=bm.verts)))
# A2: centre loop cuts in both directions
def cuts(bm):
    for no in ((1, 0, 0), (0, 1, 0)):
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0), plane_no=no)
bm_edit(cuts)
def mark_neg(bm):
    for f in bm.faces:
        c = f.calc_center_median(); f.material_index = 1 if (c.x < 0 or c.y < 0) else 0
bm_edit(mark_neg); shot("a1-quarter-selected.png", BENCH, [bench])
# A3: delete the three selected quarters, add Mirror X+Y with clipping
def delete_neg(bm):
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.x < -1e-4 or v.co.y < -1e-4], context='VERTS')
    for f in bm.faces: f.material_index = 0
bm_edit(delete_neg); shot("a2-quarter-only.png", BENCH, [bench])
mod = bench.modifiers.new("Mirror", 'MIRROR'); mod.use_axis[0] = True; mod.use_axis[1] = True; mod.use_clip = True
shot("a3-mirrored.png", BENCH, [bench])
# A4: two loop cuts near the outer corner -> a 10 x 10 cm corner face underneath, selected
def corner_cuts(bm):
    for co, no in (((0.5, 0, 0), (1, 0, 0)), ((0, 0.1, 0), (0, 1, 0))):
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=co, plane_no=no)
    for f in bm.faces:
        c = f.calc_center_median()
        if f.normal.z < -0.9 and c.x > 0.5 and c.y > 0.1: f.material_index = 1
bm_edit(corner_cuts)
bpy.data.objects["_ground"].hide_render = True
bpy.context.scene.display.shading.light = "FLAT"   # underside is unlit in Studio lighting
shot("a4-corner-face-below.png", ((1.4, -1.7, -0.5), (0.15, 0, 0.42)), [bench])
bpy.data.objects["_ground"].hide_render = False
bpy.context.scene.display.shading.light = "STUDIO"
# A5: extrude corner face down to the ground
def extrude(bm):
    f = [f for f in bm.faces if f.material_index == 1][0]
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    vs = [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, -0.4), verts=vs)
    for f in bm.faces: f.material_index = 0
bm_edit(extrude); shot("a5-bench-done.png", BENCH, [bench])
print("BENCH dims", tuple(round(d, 3) for d in bench.dimensions))

# ================= Exercise B: campfire (3D cursor pivot, duplicate+rotate, local axes, individual origins) =================
reset_scene(); ground()
sel = material("_Sel", SELECT)
bark, flame, flame2, stone = material("Bark", (0.35, 0.2, 0.1), 0, 0.9), material("Flame", (1.0, 0.45, 0.05)), material("FlameCore", (1.0, 0.85, 0.2)), material("Stone", (0.5, 0.5, 0.52), 0, 0.9)
FIRE = ((1.5, -1.9, 1.3), (0, 0, 0.12))
# B1: one log lying along X, inner end at the centre
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.06, depth=0.6, location=(0.3, 0, 0.06), rotation=(0, math.pi / 2, 0))
log = bpy.context.active_object; log.name = "Log"; log.data.materials.append(bark)
shot("b1-one-log-cursor.png", FIRE, [log], marker=(0, 0, 0.002))
# B2: Shift+D, R Z 72 around the 3D cursor, x4
logs = [log]
for i in range(1, 5):
    d = log.copy(); d.data = log.data; d.name = f"Log.{i:03d}"; bpy.context.collection.objects.link(d)
    a = math.radians(72 * i)
    d.location = (0.3 * math.cos(a), 0.3 * math.sin(a), 0.06)
    d.rotation_euler = (0, math.pi / 2, 0); d.rotation_euler.rotate_axis('Z', 0)  # placeholder
    d.matrix_world = __import__("mathutils").Matrix.Rotation(a, 4, 'Z') @ log.matrix_world
    logs.append(d)
shot("b2-five-logs.png", FIRE, logs, marker=(0, 0, 0.002))
# B3: tilt every log around its OWN local Y axis (Individual Origins, R Y Y -35), then lift
import mathutils
for l in logs:
    mw = l.matrix_world.copy(); loc = mw.to_translation()
    axis = (mw.to_3x3() @ mathutils.Vector((0, 1, 0))).normalized()
    R = mathutils.Matrix.Rotation(math.radians(35), 4, axis)
    l.matrix_world = mathutils.Matrix.Translation(loc) @ R @ mathutils.Matrix.Translation(-loc) @ mw
    l.location.z += 0.17
bpy.context.view_layer.update()
inner_z = [round((l.matrix_world @ mathutils.Vector((0, 0, -0.3))).z, 3) for l in logs]
print("LOG inner/outer z", inner_z, [round((l.matrix_world @ mathutils.Vector((0, 0, 0.3))).z, 3) for l in logs])
shot("b3-tilted.png", FIRE, logs)
# B4: flames (two cones) + stone ring (8 ico spheres around the cursor)
bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.16, depth=0.45, location=(0, 0, 0.225)); f1 = bpy.context.active_object; f1.name = "Flame"; f1.data.materials.append(flame)
bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.09, depth=0.3, location=(0, 0, 0.15), rotation=(0, 0, 0.5)); f2 = bpy.context.active_object; f2.name = "FlameCore"; f2.data.materials.append(flame2)
stones = []
for i in range(8):
    a = math.radians(45 * i)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.08, location=(0.55 * math.cos(a), 0.55 * math.sin(a), 0.04))
    s = bpy.context.active_object; s.name = f"Stone.{i}"; s.scale = (1.2, 1, 0.7); s.data.materials.append(stone); stones.append(s)
shot("b4-campfire-done.png", FIRE, logs + [f1, f2] + stones)
shot("b5-campfire-top.png", ((0, 0, 3), (0, 0, 0)), logs + [f1, f2] + stones, ortho=1.6)
