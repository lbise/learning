# Mission shift: from a test game to a rabbit game for his daughters

His daughters (4 and 6) laughed a lot at the character dancing when all the coins were collected. He now wants a real project: the girls play a rabbit collecting carrots in a forest. It's the vehicle for learning level design, asset modelling, a power-up, and modelling plus simple rigging and animation of the rabbit. MISSION.md was updated with his agreement.

**Decisions**: new Godot project. Copy the player/camera/state-machine code from the test game, because code interests him less than modelling and level design. Controls: gamepad AND keyboard + mouse, with a fixed automatic follow camera (no mouse-look, too hard for a 4-year-old). Finish Grant's well (Parts 3-5) first. He describes his modelling skills as "close to 0".

**Implications**: Godot lessons provide ready-made code and spend effort on design, feel, sound and level layout. Blender lessons stay heavily scaffolded with step images. Rabbit animation goes in stages: placeholder, then model, then squash-and-stretch in Godot, then an optional rig. Each stage ships a playable game. Supersedes the parked chest-animation lesson as the animation entry point (squash-and-stretch uses the same AnimationPlayer keyframing).
