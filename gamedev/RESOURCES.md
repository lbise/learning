# Game Development (Godot + Blender) Resources

Checked Oct 2026 against Godot 4.7 (docs "stable" = 4.7 branch) and Blender 5.2 LTS.

## Knowledge

### Godot: official docs (primary source for everything Godot)
- [Overview of Godot's key concepts](https://docs.godotengine.org/en/stable/getting_started/introduction/key_concepts_overview.html)
  Scenes, nodes, scene tree, signals on one page. Use for: the mental model.
- [Nodes and Scenes](https://docs.godotengine.org/en/stable/getting_started/step_by_step/nodes_and_scenes.html)
  "Nodes are the fundamental building blocks of your game." Use for: lesson 1 reading.
- [Creating your first script](https://docs.godotengine.org/en/stable/getting_started/step_by_step/scripting_first_script.html) / [Listening to player input](https://docs.godotengine.org/en/stable/getting_started/step_by_step/scripting_player_input.html)
  2D examples, but the ideas carry straight over to 3D. Use for: `_process(delta)`, the `Input` singleton, built-in `ui_*` actions.
- [Idle and Physics Processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)
  `_process` vs `_physics_process`, plus why to multiply by delta. Use for: the game loop.
- [Introduction to 3D](https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html)
  Y is up, 1 unit = 1 metre, the 3D editor. Use for: 3D space basics.
- [Node3D class reference](https://docs.godotengine.org/en/stable/classes/class_node3d.html) · [Input class reference](https://docs.godotengine.org/en/stable/classes/class_input.html) · [Vector3](https://docs.godotengine.org/en/stable/classes/class_vector3.html)
  Use for: exact API behaviour (`rotate_y`, `position`, `get_vector`, `Vector3.FORWARD`).
- [GDScript reference](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html) · [Static typing](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html)
  Python-like syntax, but "entirely independent from Python". Use for: language questions.
- [Best practices: Scene organization](https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html)
  "Design scenes to have no dependencies". It covers dependency injection and which node connects signals. Use for: architecture questions (who references whom).
- [Scripting languages (GDScript vs C#)](https://docs.godotengine.org/en/stable/getting_started/step_by_step/scripting_languages.html)
  The docs recommend GDScript for beginners. C# projects can't export to the web in Godot 4. Use for: justifying GDScript.
- [Your first 3D game (Squash the Creeps)](https://docs.godotengine.org/en/stable/getting_started/first_3d_game/index.html)
  A complete small 3D game: player, enemies, score. Use for: the first full project, after lesson 1-2.
- [Import configuration](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/import_configuration.html) · [Node type customization (name suffixes, `loop`)](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/node_type_customization.html) · [AnimationPlayer](https://docs.godotengine.org/en/stable/classes/class_animationplayer.html)
  Use for: importing characters, clip looping, playing animations.
- [Importing 3D scenes: available formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)
  glTF 2.0 is recommended. Includes a section on exporting from Blender. Use for: the Blender → Godot pipeline.

### Level design
- [The Level Design Book](https://book.leveldesignbook.com/) (free, online, founded by indie dev Robert Yang). Pages used: [Blockout](https://book.leveldesignbook.com/process/blockout), [Metrics](https://book.leveldesignbook.com/process/blockout/metrics), [Flow](https://book.leveldesignbook.com/process/layout/flow), [Critical path](https://book.leveldesignbook.com/process/layout/criticalpath), [Playtesting](https://book.leveldesignbook.com/process/blockout/playtesting). Use for: every level-design lesson.
- [Godot Docs: Prototyping levels with CSG](https://docs.godotengine.org/en/stable/tutorials/3d/csg_tools.html). "Level prototyping is one of the main uses of CSG in Godot." Use for: blockout tooling.

### Godot: other trusted teachers
- [GDQuest: Your first 3D game with Godot 4 (arena FPS)](https://www.gdquest.com/library/first_3d_game_godot4_arena_fps/)
  A free, well-produced 3D project. Use for: a second 3D project after Squash the Creeps.
- [GDQuest: Learn GDScript From Zero](https://gdquest.github.io/learn-gdscript/)
  Free, in-browser, aimed at non-programmers. Use for: optional syntax skim only. The learner already programs.

### Game programming (engine-agnostic)
- [Game Programming Patterns by Robert Nystrom (free online)](https://gameprogrammingpatterns.com/)
  The Godot docs point to it for the observer pattern behind signals. Use for: architecture questions (observer, state machines, game loop, update method).

### Blender
- [Blender 5.2 LTS Manual](https://docs.blender.org/manual/en/latest/) · [glTF 2.0 add-on](https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html)
  Use for: authoritative tool behaviour and export settings.
- [Blender Guru: Beginner Donut Tutorial (Blender 5.0, 2026)](https://www.blenderguru.com/posts/blender-donut-v5-tutorial)
  The standard beginner course (about 4 h of video). Use for: first contact with Blender.
- [Grant Abbitt: Blender 5 Complete Beginners Guide (free, 8 parts)](https://www.youtube.com/playlist?list=PLn3ukorJv4vv9_e-htADGsPX9TMaQpHV8)
  Published Nov 2025, about 100 min of video in total (parts are 11-14 min). 1 Interface, 2 Materials, 3-4 Old Man, 5-6 Monster, 7 Street, 8 Lights & Compositing (renders: least relevant to Godot). Chosen by the learner as his primary Blender course. Use for: the Blender fundamentals track.
- [Grant Abbitt: Modelling a Low-Poly Well (5 parts, Blender 4.2, Sep 2024)](https://www.youtube.com/playlist?list=PLn3ukorJv4vvMwZPLzlajVII2zJd-_BM-)
  About 75 min in total. Grant's own suggested follow-up to the beginner course. P1 stone base (bevel, randomize, Simple Deform bend, decimate), P2 wooden frame (vertex bevel notches, knife, mirror via Empty), P3 roof tiles, P4 winch and rope, P5 likely materials. The videos have no chapter lists: get captions with yt-dlp (works through a temp venv, may hit HTTP 429 rate limits) to build the "watch for" tables. Use for: L13-L14.
- [Grant Abbitt: Low-poly modelling](https://www.youtube.com/playlist?list=PLn3ukorJv4vsPy9J9x4--pat6jaPqNm11)
  32 videos. Use for: game-ready props after the beginner course.
- [Blender Studio: Blender 2.8 Fundamentals](https://studio.blender.org/training/blender-2-8-fundamentals/)
  Free and official, but the UI is dated. The rest of Blender Studio is paid. Use for: second opinions on fundamentals.

### Grant Abbitt: environment-art path (researched 2 Nov 2026)
**Paid (GameDev.tv, Black Friday prices until 2 Dec 2026; Udemy ratings via proxy):**
- [Blender Low Poly Landscapes](https://gamedev.tv/courses/blender-low-poly-landscapes): 6h12, Blender 4.x, **$10** (was $49), Udemy 4.9/5 from 1,720 ratings. Covers triangle and round trees, base, booleans, paving and rocks, grass and plants, colour, lighting, Eevee vs Cycles. Best fit for the mission now.
- [Blender Texture Painting: Stylised Models](https://gamedev.tv/courses/blender-texture-painting): 6h18, 4.3, $10, Udemy 4.8 (370). A hand-painted stylised turret. Phase B candidate.
- [Blender Isometric Scenes](https://gamedev.tv/courses/blender-isometric-scene-creation): 8h13, intermediate, $10. Isometric dioramas: fits the later cyberpunk interest.
- [Blender Environment Artist 5.1](https://gamedev.tv/courses/blender-environment-artist-5): 14h15, $10, Udemy 4.8 (4,541). Leans PBR, sculpting and realistic textures: later, not now.
- [Black Friday Beginner Blender Artist bundle](https://gamedev.tv/bundles/beginner-blender-black-friday-2026): **$30**. Complete Blender Creator, Isometric, Skill Builder, Texture Painting, Low Poly Landscapes, plus a Substance intro.
- Live programs (Ultimate 3D Artist $599; Game Asset Creator $499, about 6 h/week): no, too much for 3 h/week.
- [From Blender to Godot](https://gamedev.tv/courses/blender-to-godot) (Stephen Woods, not Grant), $10. Only if the export side ever needs more.

**Free YouTube, best ~10 for environment art (youtu.be/ID):** mvE_TykzJQU Essential Tips for Low Poly Scenes (12m, 2024); Komry1kruHs Low-Poly Game Optimised Textures (palette, 7m, 2024) + nEUUasLyHIA Master Low Poly Texturing; Y3vcFgutFMI 15 Minutes One Texture (Blender 5, 2026); jdTabPJuqdc Low Poly Trees; 1H2YaRPfpdM Low Poly Rocks; lthQq42f3K0 Low Poly Castle Landscape; RjxIaq8OiQg Simple Trick for Low Poly Landscapes; QE4aiWp5bZk Modular Building tips; Cdh2IZmW5ZQ Game Assets & Packs tips; j1EhPPFrZgk Asset Browser 5.1; EyK1F0BAl5Q Poly Count Explained; DmuZTw3UZ-c Blender 5 UV Unwrapping; 7kSRXnAi7uA Blender 5.1 Texture Painting (21m); F_JK9eaYYTQ Low Poly Animal + 7WYsdzSh5Nc Rigging low-poly animals. Gap: no recent free start-to-finish stylised scene project (the free ones are from 2019-2020, Blender 2.8).
- Playlists: [Low-Poly Modelling](https://www.youtube.com/playlist?list=PLn3ukorJv4vsPy9J9x4--pat6jaPqNm11) (32 videos, 2019-2026), [Texture Painting](https://www.youtube.com/playlist?list=PLn3ukorJv4vtvjZvdiOeoSA5kBohtnDOF) (30, to 5.1), [UV Unwrapping](https://www.youtube.com/playlist?list=PLn3ukorJv4vve0s-cq8VWS4jRQCdWSU3N) (11, to 2026).

### Free assets (all CC0: commercial use OK, no attribution needed)
- [Kenney](https://kenney.nl/assets) ([licence FAQ](https://kenney.nl/support)): stand-in 3D/2D assets.
- [Quaternius](https://quaternius.com/) ([FAQ](https://quaternius.com/faq.html)): low-poly characters and props, often rigged.
  - [Universal Animation Library (Standard)](https://quaternius.itch.io/universal-animation-library): a 1.83 m mannequin with 43 clips in one `.glb` (use `Unreal-Godot/UAL1_Standard.glb`, not `_RM`). Tested in 4.7.2. Used in L6.
- [Kenney Mini Characters](https://kenney.nl/assets/mini-characters): 12 small (0.67 m) CC0 characters, 32 clips each. Every clip imports non-looping, so set looping in Advanced Import Settings. Backup option.
- Kenney audio (CC0): [Impact Sounds](https://kenney.nl/assets/impact-sounds), [Interface Sounds](https://kenney.nl/assets/interface-sounds), [Music Jingles](https://kenney.nl/assets/music-jingles), [Digital Audio](https://kenney.nl/assets/digital-audio). All four are in carrot-game/sounds/kenney. Use for: game SFX and jingles.
- [Poly Haven](https://polyhaven.com/) ([licence](https://polyhaven.com/license)): HDRI skies, textures, models.

## Wisdom (Communities)

- [Godot Forum (official)](https://forum.godotengine.org/)
  Searchable Q&A. Use for: "why doesn't this work" questions.
- [Godot community page](https://godotengine.org/community/): official Discord, r/godot, local user groups.
  Use for: showing off progress and finding a local meetup.
- [Blender Artists](https://blenderartists.org/) · [r/blenderhelp](https://www.reddit.com/r/blenderhelp/)
  Use for: critique of models, and "why does my mesh look like this".
- [Godot Wild Jam](https://godotwildjam.com/)
  Monthly, 9 days long, starts the second Friday. That length fits 3 h/week. Use for: the first jam.
- [itch.io jams](https://itch.io/jams)
  Use for: finding other jams, and hosting games for the kids to play.

## Gaps
- No trusted source yet for designing games for very young children (ages 4-6). L15 rules are my own suggestions, flagged as such.
- No trusted tutorial yet for third-person survival (Valheim-like) or isometric action games in Godot 4. Search when the mission reaches that stage.
- No current free official Blender fundamentals course (the Blender Studio one is from the 2.8 era).
