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
4a. ✅ L5 Mouse→camera worked example + zoom (completion) + sprint (independent). Consolidates L4. He did ② and ③ unaided and liked the format
4b. ✅ L6 Imported animated character (Quaternius UAL, CC0) + AnimationPlayer: idle/walk/sprint/jump, victory dance; +Z MODEL_FRONT; _Loop suffix stripped
4c. ✅ L7 State machine: enum + match + change_state enter actions; LAND via animation_finished (completion); ROLL (independent)
4d. L8 candidates: kids-playtest-driven level design OR enemies (second CharacterBody3D with its own simple FSM: patrol/chase via Area3D detection) OR Blender start. Ask him which he prefers. Reached a natural milestone: a Valheim-ish controller
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

## Blender track (agreed: same workspace, lessons continue numbering, kicker "Blender track")
- He wants to start Blender now and chose Grant Abbitt's "Blender 5 Complete Beginners Guide" (8 × ~12 min). Blender 5.2.2 LTS is installed (~/.local/bin/blender).
- Blender is visual: VIDEO is the primary instruction. My role: companion pages per chunk (what to watch, active follow-along, retrieval quiz, shortcut sheet), a "transfer" task that makes an asset for HIS game, then Blender → Godot pipeline lessons (glTF export, scale/apply transforms, origin at the base, Z-up vs Y-up, collision).
- Recommended keeping it in this workspace as a separate track (same mission: success criteria include a self-made Blender asset in Godot).
- Blender track format: companion page per video block. ① setup → ② watch (chapter table + "watch for") → ③ recall quiz → ④ transfer task making assets for HIS game. Pipeline lessons (export/import) in between.
- ✅ L10 done (tripped on Alt+click face loops and material SLOTS; fixed, and step 7 rewritten as sub-steps).
- He REJECTED the chest-animation L11 (too early). It's parked at lessons/later/chest-that-opens.html (images in assets/img/later-chest, script assets/tools/later_chest_lid.py). New L11 = Parts 5-6 + Exercise A bench (mirror XY + clipping + X-ray) + Exercise B campfire (3D cursor pivot, Shift+D, individual origins, local axes, collections).
- PLAN from here: follow the course in order. L12 = Part 7 (street) + exercise. L13 = Part 8 (lights/compositing, lighter) + exercise or recap. Then the low-poly playlist or back to Godot, decided WITH him. Ask before any direction change.
- ✅ L9 done. He declined the optional tree-variant extra (fine: extras stay optional).
- L10 = Parts 3-4 (Mirror, Edit Mode) + treasure chest (edit-mode scaling, band via loop cuts, inset lid, per-face materials, mirrored handles, Apply Modifiers off by default!). L11 candidate: animate the chest lid opening on all_coins_collected (Godot AnimationPlayer keyframes OR Blender action), or continue with Parts 5-6 (Monster).
- ✅ L8 done (props.blend saved). L9 = pipeline lesson (coin end-to-end, tree join/origin, solid tree scene + forest).
- Plan: L8 Parts 1-2 + coin & tree. L9 origin, join, apply transforms, glTF export → replace Godot coin, plant trees (Godot-side lesson in the faded format). L10 Parts 3-4 (Old Man), and so on. Part 8 (lights & compositing) is optional for game purposes.
- Grant's video descriptions include chapter timestamps (fetch via the watch-page shortDescription) to build the "watch for" tables.

## Environment
- Hyprland (Wayland, Lua config in ~/gitrepo/dotfiles/dot/.config/hypr/hyprland.lua). Blender's file dialog opened as a 320x240 float. Fixed with the window rule "blender-file-view" (added on request; not committed). Alternative: Blender Prefs → Temporary Editors → Maximize Area.
- Pipeline verified headless: blender -b --python script → glb → godot --headless import. Reuse this to test Blender-track lessons.

## Visuals for build tasks (his request after L10)
- He finds it hard to picture custom builds from text alone. EVERY custom build task (Blender track especially) gets rendered images: a hero image of the finished target, a step grid matching the checklist step numbers, and front/back views of the final result.
- Pipeline: assets/tools/blender_render.py (helpers: reset_scene, material, ground, wire_overlay, camera, render; Workbench render looks like Blender's Solid view). One stage script per lesson: assets/tools/lessonNNNN_<name>.py → assets/img/NNNN/*.png. Run: blender -b --factory-startup --python <script>.
- HTML: <div class="figs"> grid of <figure><a><img></a><figcaption><b>Step N</b> …</figcaption></figure>; <figure class="hero"> for the target. Captions reference checklist step numbers.
- Gotcha: Workbench renders metallic materials near-black, so the helper keeps metallic in the nodes but sets viewport metallic to 0.
- He watched Part 5 during the L10 period (ahead of plan). For L11 he does the bench (Exercise A) as spaced retrieval, then Part 6 + campfire. L12 = Part 7. Tell him upfront in future lessons that watching ahead is fine, and which exercise matches which part.
- ✅ L11 done ("went well, liked it"). L12 = Parts 7-8 (end of the course): Exercise A fence (Alt+D vs Shift+D, Shift+R, Ctrl+L link materials, emission lanterns), Exercise B campfire at night (EEVEE, world colour, emission, point light; trap: a light inside a solid mesh is blocked). Verified: Alt+D copies → one shared mesh in Godot; emission strength survives to StandardMaterial3D.
- AFTER L12: course finished. Next session = a retrospective + decide direction WITH him (options: Grant low-poly playlist, back to Godot with his props, the parked chest animation). Don't pre-decide.
- Keyboard: NO NUMPAD, Swiss French layout (ch fr). In every Blender step, give the menu path next to numpad shortcuts (View → Frame Selected for Numpad ., View → Viewpoint → Front/Top for Numpad1/7, View → Perspective/Orthographic for Numpad5). Emulate Numpad (suggested in L8) remaps 1/2/3, which conflicts with the Edit Mode select-mode keys, so also mention the header's select-mode buttons. Asked him which he prefers (pending).
- ✅ L12 done. The beginner course is finished ("it was great"). Agreed ALTERNATING plan: L13 well P1-2 (+ stone ring for the campfire, village sign), L14 well P3-5, L15 Godot village. He already imported campfire/chest/etc. into his Godot game on his own, so L15 must NOT re-teach importing. Focus on level layout/design for the kids, or a gameplay addition. Ask him.
- Transcripts for well parts 1-4 were fetched to /tmp/well (temporary). Part 5 hit a 429: retry when writing L14.
- L13 debugging: "grey rings around stones" = Force Field accidentally added in the Physics tab (right next to Modifiers), then copied by Shift+D. Diagnosed by opening his saved .blend headless with blender -b --python-expr. Useful trick: ask him to save, then inspect the file instead of guessing. He shares screenshots via /tmp/pi-clipboard-*.png paths.
- Pipeline lesson learned (L13): "modifiers first, transforms second". Applying transforms on an object with Simple Deform collapsed his ring (verified: 1.78 m ring → 0.2 m blob). Added to reference/blender-to-godot.html. His campfire then exported cleanly as one joined object (5 materials).
- He asked about baking being destructive. Recommended direct .blend import in Godot (tested: live modifiers OK; defaults import hidden objects and lights, so set Visible = Visible Only and untick Cameras/Punctual Lights). Blender path must be set in Editor Settings (his Blender is at ~/.local/opt/blender-5.2.2-linux-x64/blender). This supersedes "join + apply transforms" as the default pipeline; keep L9 habits for .glb only.

## Rabbit game plan (agreed, see MISSION.md and learning-records/0013)
- L14 Blender: well Parts 3-5 (roof tiles, winch + rope, finish) + a small exercise. He's a modelling beginner: keep exercises small and pictured. The finished well becomes a forest landmark.
- L15 Godot: NEW project "rabbit game". Copy player/camera/state machine (give the exact files and steps), replace the mouse-look rig with a fixed auto-follow camera, input actions for keyboard AND gamepad, coin→carrot, celebration, first SOUNDS (crunch, boing). Placeholder rabbit.
- Then alternate: Blender (carrot, low-poly trees → Grant videos; forest props) / Godot level design (greybox blockout with simple blocks/CSG, paths, landmarks, carrot breadcrumbs; RESEARCH a trusted level-design source first) / power-up (golden carrot: super jump + Timer) / rabbit (Grant Low Poly Animal F_JK9eaYYTQ, squash-and-stretch hop in AnimationPlayer, then optional simple rig: body, head, ears, legs; hop + idle).
- Kid design rules: no losing, big collectibles, silly feedback, sound, simple controls.
- Code is the least interesting part for him: supply code, explain briefly, focus on design and feel.
- L14 written: well P3 (tiles, Randomize Transform, lattice + proportional editing) + Exercise A carrot (cone r1=0 r2=0.07 d=0.35, 3 loop cuts, 3 leaves via cursor pivot + individual origins, lattice bend); P4 (winch, rope, icosphere rocks, auto merge, face snapping; Snap With is called Snap Base in 5.2) + Exercise B forest-floor kit (3 rocks, mushroom); P5 captions blocked (HTTP 429), so the section is honest and generic about colour, with a table of what reaches Godot. Files go in blender/rabbit/ for direct .blend import in L15.

## Carrot game project (~/gitrepo/carrot-game), built by me at his request
- He asked me to set up the project and basic code himself ("I understand how it works"). From now on I WRITE THE CODE, and lessons focus on modelling, level design, sound and props, plus the rabbit's modelling and animation.
- Built and play-tested headless (4.7.2): input map (WASD/arrows + stick/D-pad, Space/A jump, R/Start restart), rabbit placeholder (spheres) with state machine and squash/stretch/hop bob, fixed follow camera, carrot (his carrot.blend, auto-counted via group), HUD ("x / y", "Bravo !"), confetti, 4 Kenney CC0 audio packs in sounds/kenney, test level. README.md documents knobs.
- Gotcha: changing .blend .import settings headless needs the .godot/imported cache deleted; in the editor the Reimport button works.
- Design notes for next lessons: his mushrooms are 3-5 cm vs a 1.1 m carrot (scale mismatch: decide a world scale). forest_props.blend is one scene with a 4 m ground Plane: split props into separate objects/scenes for level design. Nothing is committed in git yet (repo has no commits): ask before committing.
- NEXT lesson candidate: level design, greyboxing the forest level (research a trusted level-design source first).
- L15 = blockout lesson (Level Design Book: blockout/metrics/flow/critical path/playtesting; Godot CSG). I made levels/forest.tscn (Rabbit at z=25, camera offset is now an export (0,6,8), so the rabbit can start anywhere, Blockout CSGCombiner3D with use_collision, Ground 60x60). Measured metrics: 4.5 m/s, running jump 1.89 m high / 5.7 m long / 1.27 s, 45° max slope, no step-up, 1.15 m tall, 0.6 m wide. Tested: the rabbit can't walk out of a 0.5 m CSG dent (needs an inside ramp AFTER the subtraction node); a 20° ramp gets onto a 1 m hill.
- Possible code improvement later (mine to do): step-up for small ledges, and camera occlusion (fade/hide obstacles between camera and rabbit), if his playtests show problems.
- He asked for a Godot reference sheet: made reference/godot-level-blockout.html (navigation without numpad, CSG, path/hill/ramp/stream recipes, metrics, checklist). Every Godot design lesson needs a matching cheat sheet, like the Blender ones. Added a Paths CSGCombiner3D (no collision, sand material, PathSegment 3x0.02x10 + Clearing r4) to forest.tscn. Tested: bumps <=5 cm crossable, 10 cm blocks; +X rotation makes a ramp rise toward -Z (north).

## PIVOT (after L15): Blender environment art is the main track (MISSION.md rewritten, LR-0015)
- Project: a stylised forest-clearing scene from his own asset kit, rendered nicely, importable into Godot later as the rabbit game's forest.
- Keep Grant Abbitt as the main teacher. He asked about Grant's paid courses: research pending (background task).
- Rabbit game: on hold. I keep it working. L15 blockout parked (still valid when he wants it).
- Recommended buying Grant's Low Poly Landscapes ($10, sale until 2 Dec 2026). The $30 bundle is optional. Free videos cover techniques, but there's no recent full scene project. Awaiting his decision. L16 plan: plan the clearing (reference/mood, kit list, scale) + free "Essential Tips for Low Poly Scenes" (mvE_TykzJQU) + palette texturing (Komry1kruHs). Then companion lessons per section of the Landscapes course (fetch its curriculum from the gamedev.tv productSaleData JSON).
