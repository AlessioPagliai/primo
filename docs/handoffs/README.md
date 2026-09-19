# AI handoffs

The design is developed together with AI agents (AI, AI). These files let an agent — or a person — continue the work without redoing it.

- [ai-memory.md](ai-memory.md) — the raw working memory, source of truth for every decision, with dates, sources and open doubts. Italian and English mixed. Newest blocks are at the top; older sections below are marked when superseded. Read this first.
- [isaac.md](isaac.md) — importing the URDF into Isaac Sim / Isaac Lab, gains, acceptance tests, hip-yaw motor gate.
- [teleop.md](teleop.md) — Meta Quest teleoperation of arms and hands, legs on the RL policy.
- [mirror-debug.md](mirror-debug.md) — what is verified in the URDF mirror pipeline and what is provisional.

Rule kept throughout: no hypothesis becomes a BOM row; unknown dimensions stay `qty 0` with the missing data listed.
