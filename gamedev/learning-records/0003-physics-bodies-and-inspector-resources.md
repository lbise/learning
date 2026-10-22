# Built a character controller; tripped on resource properties in the Inspector

He finished Lesson 2: a CharacterBody3D with WASD, jump and instanced crates. The one blocker was "set the Size": he didn't know Size lives on the BoxShape3D/BoxMesh *resource*, which you click to expand, rather than on the node. Lesson 3 teaches node vs resource explicitly. The quiz score and the jump calculation still weren't reported.

**Implications**: Name the exact place to click for every editor step. The node/resource split is now a taught concept that later lessons can rely on (materials, meshes, animations). Ask for quiz scores again, since only self-reports exist so far.
