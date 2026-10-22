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
- [Scripting languages (GDScript vs C#)](https://docs.godotengine.org/en/stable/getting_started/step_by_step/scripting_languages.html)
  The docs recommend GDScript for beginners. C# projects can't export to the web in Godot 4. Use for: justifying GDScript.
- [Your first 3D game (Squash the Creeps)](https://docs.godotengine.org/en/stable/getting_started/first_3d_game/index.html)
  A complete small 3D game: player, enemies, score. Use for: the first full project, after lesson 1-2.
- [Importing 3D scenes: available formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)
  glTF 2.0 is recommended. Includes a section on exporting from Blender. Use for: the Blender → Godot pipeline.

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
- [Grant Abbitt: Learn Blender 5](https://www.youtube.com/playlist?list=PLn3ukorJv4vv9_e-htADGsPX9TMaQpHV8) · [Low-poly modelling](https://www.youtube.com/playlist?list=PLn3ukorJv4vsPy9J9x4--pat6jaPqNm11)
  A game-art focused teacher. Low-poly fits a Valheim-like style. Use for: making game assets.
- [Blender Studio: Blender 2.8 Fundamentals](https://studio.blender.org/training/blender-2-8-fundamentals/)
  Free and official, but the UI is dated. The rest of Blender Studio is paid. Use for: second opinions on fundamentals.

### Free assets (all CC0: commercial use OK, no attribution needed)
- [Kenney](https://kenney.nl/assets) ([licence FAQ](https://kenney.nl/support)): stand-in 3D/2D assets.
- [Quaternius](https://quaternius.com/) ([FAQ](https://quaternius.com/faq.html)): low-poly characters and props, often rigged.
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
- No trusted tutorial yet for third-person survival (Valheim-like) or isometric action games in Godot 4. Search when the mission reaches that stage.
- No current free official Blender fundamentals course (the Blender Studio one is from the 2.8 era).
