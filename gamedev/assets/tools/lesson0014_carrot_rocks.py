"""Lesson 14 exercises: a carrot with a lattice bend (well Part 3 skills), forest-floor rocks + mushroom (Part 4 skills).
Run: blender -b --factory-startup --python assets/tools/lesson0014_carrot_rocks.py
"""
import sys; sys.path.insert(0, "/home/leo/learning/gamedev/assets/tools")
from blender_render import *
import math, random, mathutils
OUT = "/home/leo/learning/gamedev/assets/img/0014/"
random.seed(3)

def shot(name, cam, objs, ortho=None, lattice=None):
    clear_temp()
    for o in list(bpy.data.objects):
        if o.name.startswith("_m_"): bpy.data.objects.remove(o, do_unlink=True)
    for o in objs: wire_overlay(o)
    if lattice:   # draw the lattice cage as thin orange rods between its points (lattices don't render)
        sel = material("_Sel", SELECT)
        lat = lattice.data; u, v, w = lat.points_u, lat.points_v, lat.points_w
        P = lambda i, j, k: lattice.matrix_world @ lat.points[i + j * u + k * u * v].co_deform
        segs = []
        for k in range(w):
            for j in range(v):
                for i in range(u):
                    if i + 1 < u: segs.append((P(i, j, k), P(i + 1, j, k)))
                    if j + 1 < v: segs.append((P(i, j, k), P(i, j + 1, k)))
                    if k + 1 < w: segs.append((P(i, j, k), P(i, j, k + 1)))
        for a, b in segs:
            d = b - a; mid = (a + b) / 2
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.002, depth=d.length, location=mid)
            c = bpy.context.active_object; c.name = "_m_lat"; c.data.materials.append(sel)
            c.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    camera(*cam, ortho_scale=ortho); render(OUT + name)

# ================= Exercise A: carrot =================
reset_scene(); ground(8)
orange, green = material("Carrot", (0.95, 0.45, 0.08), 0, 0.7), material("Leaves", (0.2, 0.6, 0.15), 0, 0.8)
CAM = ((0.75, -1.25, 0.6), (0.03, 0, 0.25))
# 1: cone, tip down: Radius 1 = 0 (bottom), Radius 2 = 0.07 (top), depth 0.35, sitting on the ground
bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.0, radius2=0.07, depth=0.35, location=(0, 0, 0.175))
car = bpy.context.active_object; car.name = "Carrot"; car.data.materials.append(orange)
shot("a1-cone.png", CAM, [car])
# 2: three loop cuts + lumpy rings + tiny randomize
bm = bmesh.new(); bm.from_mesh(car.data)
for z in (-0.09, 0.0, 0.08):
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, z), plane_no=(0, 0, 1))
for v in bm.verts:
    if abs(v.co.z - 0.0) < 1e-4: v.co.x *= 1.12; v.co.y *= 1.12
    v.co += mathutils.Vector([random.uniform(-1, 1) * 0.004 for _ in range(3)])
bm.to_mesh(car.data); bm.free()
shot("a2-loop-cuts.png", CAM, [car])
# 3: three leaves around the top centre, tilted outwards (3D cursor pivot, then individual origins)
leaves = []
for i in range(3):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.42)); lf = bpy.context.active_object; lf.name = f"Leaf.{i}"
    lf.data.materials.append(green)
    bm = bmesh.new(); bm.from_mesh(lf.data); bmesh.ops.scale(bm, vec=(0.035, 0.012, 0.16), verts=bm.verts)
    top = [v for v in bm.verts if v.co.z > 0]; bmesh.ops.scale(bm, vec=(0.3, 1, 1), verts=top)   # taper the tip
    bm.to_mesh(lf.data); bm.free()
    lf.rotation_euler = (0, math.radians(20), math.radians(120 * i))
    lf.location = (0.025 * math.cos(math.radians(120 * i)), 0.025 * math.sin(math.radians(120 * i)), 0.41)
    leaves.append(lf)
shot("a3-leaves.png", CAM, [car] + leaves)
# 4: lattice around everything, 1 x 1 x 4 points... use u=2, v=2, w=4 along Z; bend the middle rows sideways
lat_data = bpy.data.lattices.new("Lattice"); lat = bpy.data.objects.new("Lattice", lat_data); bpy.context.collection.objects.link(lat)
lat_data.points_u, lat_data.points_v, lat_data.points_w = 2, 2, 4
lat.location = (0, 0, 0.255); lat.scale = (0.2, 0.2, 0.54)
for o in [car] + leaves:
    m = o.modifiers.new("Lattice", 'LATTICE'); m.object = lat
bpy.context.view_layer.update()
shot("a4-lattice.png", CAM, [car] + leaves, lattice=lat)
# bend: shift the upper rows in X progressively (like G X with proportional editing)
for idx, p in enumerate(lat_data.points):
    k = idx // 4   # w index 0..3 (bottom..top)
    p.co_deform.x = p.co.x + [0.0, 0.25, 0.7, 1.3][k]   # local units: lattice scale X is 0.2, so 1.3 = 26 cm
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get(); e = car.evaluated_get(dg); me = e.to_mesh()
print('CARROT top x range', round(min(v.co.x for v in me.vertices if v.co.z > 0.15), 3), round(max(v.co.x for v in me.vertices if v.co.z > 0.15), 3)); e.to_mesh_clear()
shot("a5-bent.png", CAM, [car] + leaves, lattice=lat)
shot("a6-carrot-done.png", ((0.7, -1.15, 0.5), (0.06, 0, 0.25)), [car] + leaves)

# ================= Exercise B: forest-floor rocks + mushroom =================
reset_scene(); g = ground(8)
stone, stem_m, cap_m, dots_m = material("Stone", (0.5, 0.5, 0.52), 0, 0.9), material("Stem", (0.92, 0.88, 0.78), 0, 0.8), material("Cap", (0.8, 0.12, 0.1), 0, 0.6), material("Dots", (0.97, 0.97, 0.95), 0, 0.6)
FLOOR = ((1.5, -2.0, 1.1), (0.15, 0, 0.15))
def rock(loc, r, seed, flat=0.7):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=r, location=loc); o = bpy.context.active_object
    o.data.materials.append(stone)
    bm = bmesh.new(); bm.from_mesh(o.data); rnd = random.Random(seed)
    for v in bm.verts: v.co += mathutils.Vector([rnd.uniform(-1, 1) * r * 0.18 for _ in range(3)]); v.co.z *= flat
    bm.to_mesh(o.data); bm.free(); return o
r1 = rock((0, 0, 0.12), 0.22, 1)
shot("b1-rock.png", ((0.8, -1.0, 0.6), (0, 0, 0.1)), [r1])
r2 = rock((0.5, 0.25, 0.07), 0.13, 2); r2.rotation_euler.z = 1.2
r3 = rock((-0.35, 0.3, 0.06), 0.1, 3); r3.rotation_euler = (0.4, 0, 2.2)
# mushroom: 6-sided stem + half UV sphere cap
bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.035, depth=0.16, location=(0.3, -0.25, 0.08)); stem = bpy.context.active_object; stem.data.materials.append(stem_m)
bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=6, radius=0.11, location=(0.3, -0.25, 0.15)); cap = bpy.context.active_object; cap.data.materials.append(cap_m)
bm = bmesh.new(); bm.from_mesh(cap.data)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -1e-4], context='VERTS')
for v in bm.verts: v.co.z *= 0.75
bm.to_mesh(cap.data); bm.free()
for o in (r1, r2, r3): o.hide_render = True
shot("b2-mushroom.png", ((0.75, -0.95, 0.3), (0.3, -0.25, 0.11)), [stem, cap])
for o in (r1, r2, r3): o.hide_render = False
shot("b3-floor-kit.png", ((1.1, -1.5, 0.8), (0.12, 0, 0.1)), [r1, r2, r3, stem, cap])
