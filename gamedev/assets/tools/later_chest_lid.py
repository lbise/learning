"""Lesson 11: separate the chest lid, hinge origin, fill holes. Renders images and exports a test glb.
Run: blender -b --factory-startup --python assets/tools/lesson0011_lid.py
"""
import sys; sys.path.insert(0, "/home/leo/learning/gamedev/assets/tools")
from blender_render import *
import math
OUT = "/home/leo/learning/gamedev/assets/img/later-chest/"
EXPORT = "/tmp/l11/proj/models/chest.glb"
PERSP = ((1.9, -2.3, 1.55), (0, 0, 0.3))

reset_scene(); ground()
wood, gold, sel = material("Wood", (0.4, 0.22, 0.1), 1 and 0, 0.8), material("Gold", (1.0, 0.7, 0.1), 1, 0.3), material("_Sel", SELECT)

# ---- the Lesson 10 chest (same geometry) ----
bpy.ops.mesh.primitive_cube_add(size=2); chest = bpy.context.active_object; chest.name = "Chest"
for m in (wood, gold, sel): chest.data.materials.append(m)
bm = bmesh.new(); bm.from_mesh(chest.data)
bmesh.ops.scale(bm, vec=(0.5, 0.3, 0.3), verts=bm.verts); bmesh.ops.translate(bm, vec=(0, 0, 0.3), verts=bm.verts)
for z in (0.38, 0.42):
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, z), plane_no=(0, 0, 1))
for f in bm.faces:
    if 0.38 < f.calc_center_median().z < 0.42 and abs(f.normal.z) < 0.5: f.material_index = 1
top = [f for f in bm.faces if f.normal.z > 0.9][0]
bmesh.ops.inset_region(bm, faces=[top], thickness=0.05); bmesh.ops.translate(bm, vec=(0, 0, -0.04), verts=top.verts)
lk = bmesh.ops.create_cube(bm, size=0.16); bmesh.ops.translate(bm, vec=(0, -0.31, 0.4), verts=lk['verts'])
for f in {f for v in lk['verts'] for f in v.link_faces}: f.material_index = 1
bm.to_mesh(chest.data); bm.free()
bpy.ops.mesh.primitive_cube_add(size=1); h = bpy.context.active_object; h.name = "Handles"; h.data.materials.append(gold)
bm = bmesh.new(); bm.from_mesh(h.data)
bmesh.ops.scale(bm, vec=(0.06, 0.25, 0.06), verts=bm.verts); bmesh.ops.translate(bm, vec=(0.53, 0, 0.3), verts=bm.verts)
bm.to_mesh(h.data); bm.free(); h.modifiers.new("Mirror", 'MIRROR')

def is_lid_vert(v):   # above the band, and not part of the lock (lock is the only geometry near x = 0 at the front)
    return v.co.z > 0.415 and not (abs(v.co.x) < 0.1 and v.co.y < -0.2)

def shot(name, cam=PERSP, ortho=None, marker=None):
    clear_temp()
    for o in list(bpy.data.objects):
        if o.name.startswith("_m_"): bpy.data.objects.remove(o, do_unlink=True)
    for o in list(bpy.data.objects):
        if o.type == 'MESH' and not o.name.startswith("_"): wire_overlay(o)
    if marker:   # orange dot = object origin, thin rod = hinge axis
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=marker); d = bpy.context.active_object; d.name = "_m_dot"; d.data.materials.append(sel)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.006, depth=1.3, location=marker, rotation=(0, math.pi / 2, 0)); r = bpy.context.active_object; r.name = "_m_rod"; r.data.materials.append(sel)
    camera(*cam, ortho_scale=ortho); render(OUT + name)

shot("00-closed.png")

# Step: select the lid (orange), lock excluded
bpy.context.view_layer.objects.active = chest
me = chest.data; bm = bmesh.new(); bm.from_mesh(me)
orig = {f.index: f.material_index for f in bm.faces}
for f in bm.faces:
    if all(is_lid_vert(v) for v in f.verts): f.material_index = 2
bm.to_mesh(me); bm.free()
shot("01-lid-selected.png", ((1.6, -2.6, 1.0), (0, 0, 0.35)))
bm = bmesh.new(); bm.from_mesh(me)
for f in bm.faces: f.material_index = orig[f.index]
bm.to_mesh(me); bm.free()

# Separate (P > Selection) in Edit Mode
bpy.ops.object.select_all(action='DESELECT'); chest.select_set(True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_mode(type='VERT'); bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')
for v in me.vertices: v.select = is_lid_vert(v)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.separate(type='SELECTED'); bpy.ops.object.mode_set(mode='OBJECT')
lid = [o for o in bpy.context.selected_objects if o != chest][0]; lid.name = "Lid"
# exploded view to show the holes
lid.location.z += 0.25; shot("02-separated-holes.png", ((1.6, -2.0, 2.1), (0, 0, 0.45)))

# Fill the holes (select boundary, F); chest's new top is Gold = treasure
for obj, mat_idx in ((chest, 1), (lid, 0)):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_mode(type='EDGE'); bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold(); bpy.ops.mesh.edge_face_add()
    obj.active_material_index = mat_idx; bpy.ops.object.material_slot_assign(); bpy.ops.object.mode_set(mode='OBJECT')
shot("03-filled.png", ((1.6, -2.0, 2.1), (0, 0, 0.45)))
lid.location.z -= 0.25

# Hinge origin: back-bottom edge of the lid = (0, 0.3, 0.42)
bpy.ops.object.select_all(action='DESELECT'); lid.select_set(True); bpy.context.view_layer.objects.active = lid
bpy.context.scene.cursor.location = (0, 0.3, 0.42); bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.context.scene.cursor.location = (0, 0, 0)
print("LID ORIGIN", tuple(round(c, 3) for c in lid.location))
shot("04-hinge-origin.png", ((2.4, 1.2, 1.3), (0, 0.15, 0.35)), marker=(0, 0.3, 0.42))

# Open pose (for the picture only)
lid.rotation_euler.x = math.radians(-110); shot("05-open.png", ((2.9, -3.7, 2.4), (0, 0.15, 0.6)))
shot("06-open-side.png", ((3, 0, 0.6), (0, 0, 0.5)), ortho=2.0)
lid.rotation_euler.x = 0

# Export (closed), with Apply Modifiers
bpy.ops.object.select_all(action='DESELECT')
for o in (chest, lid, h): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=EXPORT, export_format='GLB', use_selection=True, export_yup=True, export_apply=True)
