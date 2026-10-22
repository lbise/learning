# Blocked on mouse → camera: the input-event model wasn't understood

In Lesson 4 he got stuck on the first spec item (mouse orbits the camera), opened every hint, then copied the full solution. Everything works, but only because of the copied solution. The missing piece was the *event* model: mouse motion arrives via `_unhandled_input(event)` as deltas (`relative`) that must be accumulated, unlike polled key actions. He also felt that having to skim the docs "defeats the purpose".

**Evidence**: His own detailed account (hints 1-4 + solution, stuck at spec item 1).

**Implications**: Treat L4 material as *exposed, not learned*. L5 re-teaches it as a worked example (encoder-ticks analogy, event path, line-by-line table), then a completion task (wheel zoom) and an independent task (sprint, known concepts only). Doc lookups are framed as a deliberate, bounded skill (Ctrl+click, F1), never as the way to discover core concepts. Don't move on to animation until he can explain the event path unaided.
