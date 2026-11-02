"""Reusable helpers for rendering lesson illustrations with Blender in background mode.

Usage from a stage script:
    import sys; sys.path.insert(0, "<workspace>/assets/tools")
    from blender_render import *
Run: blender -b --factory-startup --python <stage_script>.py
Renders look like Blender's own Solid viewport (Workbench), so they match what the learner sees.
"""
import bpy, bmesh, math
from mathutils import Vector

def reset_scene():
    bpy.ops.wm.read_homefile(use_empty=True)
    s = bpy.context.scene
    s.render.engine = 'BLENDER_WORKBENCH'
    s.display.shading.light = 'STUDIO'
    s.display.shading.color_type = 'MATERIAL'
    s.display.shading.show_cavity = True
    s.display.shading.show_object_outline = True
    s.render.resolution_x, s.render.resolution_y = 900, 600
    s.render.film_transparent = False
    s.world = bpy.data.worlds.new("W") if not s.world else s.world
    s.world.color = (0.86, 0.86, 0.83)   # light backdrop, close to the lesson paper colour
    s.display_settings.display_device = 'sRGB'
    return s

def material(name, color, metallic=0.0, roughness=0.5):
    """Principled BSDF material whose viewport colour matches (Workbench shows diffuse_color)."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = roughness
    m.diffuse_color = (*color, 1)
    m.metallic, m.roughness = 0.0, roughness   # viewport only: metallic renders near-black in Workbench
    return m

GREY = (0.8, 0.8, 0.8)
SELECT = (1.0, 0.45, 0.05)   # Blender's orange selection colour

def ground(size=12.0):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    g = bpy.context.active_object; g.name = "_ground"
    g.data.materials.append(material("_Ground", (0.35, 0.37, 0.4)))
    return g

def wire_overlay(obj, thickness=0.004):
    """Dark edge lines on top of obj, so loop cuts and insets are visible in the render."""
    w = obj.copy(); w.data = obj.data.copy(); w.name = "_wire_" + obj.name
    bpy.context.collection.objects.link(w)
    w.data.materials.clear(); w.data.materials.append(material("_Wire", (0.05, 0.05, 0.06)))
    mod = w.modifiers.new("wire", 'WIREFRAME'); mod.thickness = thickness; mod.use_replace = True
    mod.use_even_offset = True
    return w

def camera(location, target=(0, 0, 0.3), ortho_scale=None, lens=65):
    cam_data = bpy.data.cameras.new("Cam"); cam = bpy.data.objects.new("Cam", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = Vector(location)
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    if ortho_scale: cam_data.type = 'ORTHO'; cam_data.ortho_scale = ortho_scale
    else: cam_data.lens = lens
    bpy.context.scene.camera = cam
    return cam

def render(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)

def clear_temp():
    for o in list(bpy.data.objects):
        if o.name.startswith("_wire_") or o.name == "Cam":
            bpy.data.objects.remove(o, do_unlink=True)
