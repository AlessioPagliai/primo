# AI handoffs

The design is developed together with AI agents (AI, AI). These files let an agent — or a person — continue the work without redoing it. Entry point: [AGENTS.md](../../AGENTS.md).

- [ai-memory.md](ai-memory.md) — the raw working memory, source of truth for every decision, with dates, sources and open doubts. Italian and English mixed. Newest blocks are at the top; older sections below are marked when superseded. Read this first.
- [isaac.md](isaac.md) — importing the URDF into Isaac Sim / Isaac Lab, gains, acceptance tests, hip-yaw motor gate.
- [../../sim/isaaclab/](../../sim/isaaclab/) — the locomotion training handoff, kept with its code and policy: `HANDOFF.md` (the journey round by round), `LESSONS.md` (traps), `RESULTS.md`, `NEXT_STEPS.md`, and in `reference/` the raw work log of the simulation workstation.
- [teleop.md](teleop.md) — Meta Quest teleoperation of arms and hands, legs on the RL policy.
- [mirror-debug.md](mirror-debug.md) — what is verified in the URDF mirror pipeline and what is provisional.
- [../motor-selection.md](../motor-selection.md) — why RobStride: the comparison with Encos (Asimov), CubeMars and the others, distilled from the memory.

Rule kept throughout: no hypothesis becomes a BOM row; unknown dimensions stay `qty 0` with the missing data listed.
