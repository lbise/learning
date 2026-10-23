# Reaches for signals to decouple on his own; next refinement is *who* does the wiring

After Lesson 6 he questioned the solution (world calls `player.celebrate()`) and proposed a `collected_all` signal that the player connects to. That's a sound decoupling instinct, unprompted. The flaw: if the player connects itself, it has to find the world, so the reusable child scene now depends on its level. Godot's scene-organization guide says to design scenes with no dependencies and let the parent inject them: the parent connects the child's signals. The refinement: World emits `all_coins_collected`, and World (or an editor connection in world.tscn) connects it to `Player.celebrate`.

**Evidence**: His own design proposal, made without prompting.

**Implications**: He is ready for architecture discussions (dependency direction, event bus/autoload, state machines). Rule to reinforce: "the node that knows both sides does the wiring". Revisit it with an event-bus autoload when cross-scene events appear.
