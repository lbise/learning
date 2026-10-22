# Godot Game Development Glossary

Canonical terms for this workspace. Only terms the learner has used correctly are added here.

## Engine model

**Node**:
The basic building block of a Godot game. Each node type does one job (draw a mesh, render a view, emit light).
_Avoid_: object, component, entity

**Scene**:
A saved, reusable tree of nodes (`.tscn`). It plays the role of both "prefab" and "level" in other engines.
_Avoid_: prefab, level (when you mean the file)

**Scene tree**:
The single runtime tree that all running scenes are joined into. A child's transform is relative to its parent.
_Avoid_: hierarchy, world

**Frame**:
One pass of the engine's loop, ending in one rendered image. The frame rate varies.
_Avoid_: tick (reserved for physics ticks)

**delta**:
Seconds elapsed since the previous call of a processing callback. Multiplying rates by it makes them frame-rate independent.
_Avoid_: dt, timestep

**Instance**:
A copy of a scene placed inside another scene. It stays linked to its source `.tscn`, so edits to the source show up in every instance.
_Avoid_: clone, prefab copy

## Physics

**Collision object**:
A node that takes part in collision: `StaticBody3D`, `CharacterBody3D`, `RigidBody3D` (the three *physics bodies*) or `Area3D` (detects overlaps, never blocks).
_Avoid_: collider, physics object

**Collision shape**:
The geometry physics uses for a collision object (a `CollisionShape3D` child). It's separate from the visible mesh.
_Avoid_: hitbox (in general use), collider

**Velocity**:
A `CharacterBody3D`'s motion in metres per second. `move_and_slide()` turns it into movement and applies delta internally.
_Avoid_: speed (which is velocity's magnitude only)

**Input action**:
A named intent (`jump`, `move_left`) defined in the Input Map and bound to one or more keys or buttons. Code checks actions, never raw keys.
_Avoid_: keybind, key
