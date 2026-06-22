# Cloud Routine recipe — one shaped task per night, draft-PR only

Schedule `night-shift` as a Cloud Routine (via `/schedule` or
claude.ai/code/routines — not a session `/loop`, which expires and dies on
sleep). Same cloud constraints: fresh clone, **no local files**, **no approval
prompts mid-run**, durable output only via a `claude/` branch / PR.

## Setup checklist

- [ ] **Commit the shaped file.** `.ath/tasks/<slug>/shape.md` (brief + `## tasks`
      checklist) and the `night-shift` + `shape` skills must be committed to the
      target repo — the fresh clone can only see what's in git.
- [ ] **Withhold merge capability** (the real never-merge guarantee): the
      routine's GitHub token/App has no merge permission, "Allow unrestricted
      branch pushes" is OFF (so it can only push `claude/` branches), and no
      merge-capable connector is attached.
- [ ] **Enable branch protection** on `main`/`master`/`release` in the repo
      (require a PR, block direct pushes and force-pushes) — the server-side
      backstop that holds even if the capability scoping above is misconfigured.
- [ ] **Network:** Trusted preset is enough (registries + GitHub).

## The routine prompt (self-contained — no session memory)

> Run the `night-shift` skill against `.ath/tasks/<slug>/shape.md` in
> this repo. Implement the ONE
> next unchecked task only. Hard limits: touch at most **N files / M diff lines**
> — if the task would exceed that, stop and open the partial draft PR instead of
> expanding. Run the local gate (cap 3 log-gated retries). Commit to a `claude/`
> branch, open a **DRAFT** PR, check the task's box, and stop. Do **not** merge,
> do **not** push to a protected branch, do **not** start any other task. If
> blocked, write the blocker into the PR description and exit.

## Trigger & cadence

- Trigger: schedule, daily, an overnight slot (1-hour minimum easily met). Pick
  an off-the-hour minute.
- One iteration per fire — the cron-once cadence is itself the blast-radius bound
  (the loop physically cannot overbake past one task overnight).
- **Single-agent only** inside the loop until cost is measured — no sub-agent
  fan-out (≈15× tokens compounds per iteration). Routines have a per-account
  daily run cap; read usage at claude.ai after week one.

## Morning

You review the draft PR(s) and merge the ones you want. That review/land step is
the binding human constraint by design — start with one feature's queue and one
small task category before trusting larger ones.
