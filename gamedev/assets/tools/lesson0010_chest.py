"""Renders the step-by-step chest images for lessons/0010. Geometry matches the lesson's steps.
Run: blender -b --factory-startup --python assets/tools/lesson0010_chest.py
"""
import sys; sys.path.insert(0, "/home/leo/learning/gamedev/assets/tools")
from blender_render import *
OUT = "/home/leo/learning/gamedev/assets/img/0010/"
PERSP = ((1.9, -2.3, 1.55), (0, 0, 0.3))

reset_scene(); ground()
grey, wood, gold, sel = material("Default", GREY), material("Wood", (0.4, 0.22, 0.1), 0, 0.8), material("Gold", (1.0, 0.7, 0.1), 1, 0.3), material("_Sel", SELECT)

bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0)); chest = bpy.context.active_object; chest.name = "Chest"
for m in (grey, gold, sel): chest.data.materials.append(m)   # slots: 0 grey/wood, 1 gold, 2 highlight

def edit(fn):
    bm = bmesh.new(); bm.from_mesh(chest.data); r = fn(bm); bm.to_mesh(chest.data); bm.free(); return r

def shot(name, cam=PERSP, ortho=None):
    clear_temp(); wire_overlay(chest)
    if bpy.data.objects.get("Handles"): wire_overlay(bpy.data.objects["Handles"])
    camera(*cam, ortho_scale=ortho); render(OUT + name)

# Step 2-3: scale and lift in Edit Mode
def s1(bm):
    bmesh.ops.scale(bm, vec=(0.5, 0.3, 0.3), verts=bm.verts); bmesh.ops.translate(bm, vec=(0, 0, 0.3), verts=bm.verts)
edit(s1); shot("01-body.png")

# Step 5: two loop cuts -> band
def s2(bm):
    for z in (0.38, 0.42):
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, z), plane_no=(0, 0, 1))
edit(s2); shot("02-loop-cuts.png")

# Step 6: inset top + push down (view from higher up to see the recess)
def s3(bm):
    top = [f for f in bm.faces if f.normal.z > 0.9][0]
    bmesh.ops.inset_region(bm, faces=[top], thickness=0.05); bmesh.ops.translate(bm, vec=(0, 0, -0.04), verts=top.verts)
edit(s3); shot("03-lid-inset.png", ((1.9, -2.4, 3.0), (0, 0, 0.35)))

# Step 7a: band loop selected (orange, like Blender's selection)
def band(bm, idx):
    for f in bm.faces:
        if 0.38 < f.calc_center_median().z < 0.42 and abs(f.normal.z) < 0.5: f.material_index = idx
edit(lambda bm: band(bm, 2)); shot("04-band-selected.png")

# Step 7b: materials assigned
chest.data.materials[0] = wood
edit(lambda bm: band(bm, 1)); shot("05-materials.png")

# Own work: one handle on +X, origin at the world origin
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0)); h = bpy.context.active_object; h.name = "Handles"; h.data.materials.append(gold)
bm = bmesh.new(); bm.from_mesh(h.data)
bmesh.ops.scale(bm, vec=(0.06, 0.25, 0.06), verts=bm.verts); bmesh.ops.translate(bm, vec=(0.53, 0, 0.3), verts=bm.verts)
bm.to_mesh(h.data); bm.free()
shot("06-one-handle.png", ((3.0, -1.8, 1.6), (0.15, 0, 0.3)))

# Mirror + lock = final
h.modifiers.new("Mirror", 'MIRROR')
def lock(bm):
    lk = bmesh.ops.create_cube(bm, size=0.16); bmesh.ops.translate(bm, vec=(0, -0.31, 0.4), verts=lk['verts'])
    for f in {f for v in lk['verts'] for f in v.link_faces}: f.material_index = 1
edit(lock)
shot("07-final.png")
shot("08-final-front.png", ((0, -4, 0.35), (0, 0, 0.35)), ortho=1.6)
shot("09-final-back-left.png", ((-1.9, 2.0, 1.4), (0, 0, 0.3)))
