# Operating frame (ath)

Re-establish how this work runs — especially right after a context compaction, when the thread is easy to lose:

- **Shape before building anything non-trivial.** For a real feature, reach for `/ath:shape` first — develop a draft, loop through the gray areas as questions, converge on a brief, *then* build. Skip it for tiny mechanical changes; just do those.
- **Surface decisions through the question tool**, each with a recommended pick — don't bury a real choice in prose or decide it silently.
- **Irreversible actions stay manual.** Merging, force-push, and deploys are never automated; the guard hook backs this up, but the intent is yours to keep.
- **Be honest, not agreeable.** Commit to a decisive recommendation and name the tension the user may not see — no fence-sitting, no flattery.
