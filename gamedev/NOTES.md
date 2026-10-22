# Teacher notes

- Programmer (C, Python, embedded). Teach engine concepts, not programming. Compare to Python/C where it helps (e.g. GDScript ≈ Python syntax; `_process` loop ≈ superloop tick).
- Prefers 3D, but 2D is fine. Inspirations: Valheim, isometric cyberpunk action games.
- Wants to make games for his kids: good motivator for project choices.
- 3 h/week → each lesson should take ~20-40 min, leaving the rest for practice or a primary source.
- Plan: Godot first, Blender later (when a game needs custom assets). Use Kenney/Quaternius placeholder assets until then.
- Workspace: ~/learning/gamedev. Godot 4.7.2 at /usr/bin/godot. Blender not installed yet.

## Rough roadmap (revise as learning records accumulate)
1. ✅ L1 Nodes, scenes, game loop: cube you can drive (found it basic → pace up)
2. ✅ L2 Physics bodies: CharacterBody3D walks/jumps among crates, Input Map, scene instancing
3. ✅ L3 Area3D + signals + score UI + node vs resource: collect coins → first game the kids can play (includes a kids playtest: bring back one confusion and one delight)
4. L4 Third-person camera (SpringArm3D, mouse look, camera-relative movement, Model facing). FIRST SPEC-DRIVEN LESSON
4a. L5 Mouse→camera worked example + zoom (completion) + sprint (independent). Consolidates L4, which was copied, not learned
4b. L6 Imported animated character (Quaternius CC0) + AnimationPlayer/AnimationTree: idle/walk/jump; +Z MODEL_FRONT gotcha
5. Squash the Creeps (official) as a self-guided consolidation project, or skip if L2-L4 cover it
6. Blender intro → model a simple prop → glTF into Godot
7. Third-person (Valheim-ish) or isometric (cyberpunk) prototype
8. Godot Wild Jam entry

## Lesson conventions
- The user asked whether he must read every link. Inline links are citations only (optional). Each lesson has exactly ONE recommended reading, in the "Primary source" box. Keep stating this in the lesson's meta box ("Links" row).
- Editor UI steps need to say exactly where to click. He got stuck on "set Size" in L2: he didn't know you click the resource (BoxShape3D/BoxMesh) in the Inspector to expand its properties. The resource-vs-node distinction is worth a proper explanation soon (a candidate for L3 or L4).
- L4's pure spec format was too big a jump ("way harder"). From L5, use FADED GUIDANCE:
  1. Worked example: the new concept fully shown and explained (read + run)
  2. Completion task: the same pattern with gaps / TODOs to fill
  3. Small independent spec using only concepts he already knows (retrieval + desirable difficulty)
  Hints stay available. Full guidance for new editor UI, less for code he has seen before.
  Learning-science sources: Clark, Kirschner & Sweller 2012 (https://www.aft.org/sites/default/files/Clark.pdf); Bjork lab, desirable difficulties (https://bjorklab.psych.ucla.edu/research/)
- He found L1-L3 easy. Don't over-explain programming. Maths/engineering framings (integration, LPF, rotation matrices) land well.
- Stop asking for quiz scores every time. Ask once casually at most. The kids-playtest feedback is still worth asking about.
