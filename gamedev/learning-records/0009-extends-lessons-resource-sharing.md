# Extends lessons on his own; met the shared-resource trap in practice

After Lesson 9 he went beyond the spec: he added a script with an exported height to `tree.tscn` to make size variants. He got stuck on how to resize without scaling collision. The solution combines: scale only the visual model; resize the CylinderShape3D via its properties; make the shape **Local to Scene**, because otherwise every tree instance shares one shape resource and the last tree's `_ready` wins (verified in 4.7.2); and `@tool` with export setters for editor preview.

**Evidence**: His own question and partial implementation.

**Implications**: The node/resource split (L3) now has a concrete failure mode he's run into: shared resources across instances. Expect him to keep extending lessons, so stretch goals pay off. `@tool` and export setters are introduced but not yet practised. Revisit them when building level-design helpers.
