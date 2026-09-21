# primo — open hardware humanoid — shared working memory

Last update: 2026-09-21.

> **GENERATED BONES (bonegen) + STANDARD MOTORS VS HOUSING-AS-BONE — 2026-09-21 evening (AI + user):** the user wants bones generated automatically instead of flat CAD plates: place the motors, then grow each bone between their screw holes by topology optimisation, clear of everything that moves, with screws insertable; goal stated by the user: **all bones generated and the robot walking with them in Isaac Lab, loads taken from the simulation**. Built `umanoide/bones/` (local venv) and published as `umanoide-release/cad/bonegen/`: `bonegen.py` (one file: voxelise, pads on the motor screw holes, swept keep-outs of the neighbours over the joint range + 3 mm clearance, counterbores and tool paths, multi-load-case SIMP, smooth mesh of equal volume, exact booleans), `thigh_free.json` (free mode: NO CAD bone as input), `thigh.json` (CAD-interface mode, only for the baseline), `render.py`, `README.md` = handoff and plan for the workstation. **User decisions:** standard mounting for every motor (one bone on the body/outer holes, the other on the output/inner holes, both on the output face); NO back mounting even where the body holes are through; free mode preferred over optimising the CAD bone. **Measured from the meshes:** RS06 output 6 x M4 on Ø24; RS04 body 10 x Ø4 on Ø106.6 through the lobes, mounting face 3.6 mm behind the rotor face; RS04 output 6 x Ø5 on Ø36 (check against RobStride drawings). CAD knee: femur plate y -129.4..-139.4 on the body holes, shank plate from -141.5 on a Ø50 hub through the femur ring, gap 2.1 mm -> femur screw heads MUST be counterbored. **The CAD femur touches the shank assembly from about 123 deg of knee flexion** (URDF limit 165 deg inherited from the reference robot; policy uses -5..116): joint limits to be decided. The CAD femur is 188.4 cm3 solid = 0.236 kg at 1.25 g/cm3. **Pilot result (Mac, 4 mm, ASSUMED loads, equal mass):** generated thigh vs CAD femur: lateral bending x1.75, torsion x1.47, knee torque x0.92, fore-aft x0.95, axial x0.59 (0.14 -> 0.24 mm under 2x body weight) = a draw overall; the flat plate is efficient in its plane and weak sideways. Needs 2 mm and real loads: work moves to the workstation (GPU, policy, forces). Isaac Lab cannot optimise bones while walking (rigid links): loop in rounds = loads from the policy -> bones -> new masses in the URDF -> fine-tune -> loads again. **Motors:** new `docs/actuator-integration.md`: standard modules and custom housing-as-bone actuators will coexist; penalty of standard = mass/bulk (RS04 ~84 Nm/kg vs ~189 custom; 45 kg vs 35 kg), not walking ability; future proof = motor as swappable interface + regenerated bones; clamping suits aluminium links, not PA-CF (heat, creep); integrated route = frameless kit (stator + rotor bought) + own housing, bearings, gearbox, encoders, driver; a complete low-reduction hollow-shaft actuator sold without housing is not a catalogue item as far as known (the housing carries ring gear and bearing seats); metal-printed housings need finish machining; suggested path: v1 standard, metal bones on hot joints, later one bench joint. Zip for the workstation on the Desktop: `primo-bonegen-workstation.zip`. Remote Control only mirrors this Mac session: it does not run commands on the workstation.
> **WRITING RULE (2026-09-21, user):** this file is English only. Call assistants "AI" / "AI session": no product or company name of any AI tool in this file or in any shared material (repository and its history, download package, bucket, listings), and no agent-specific entry file in the repository: `AGENTS.md` is the only one. Today: the memory was translated line by line (numbers, links and code spans checked automatically; Italian original kept in `outputs/memory-backups/`), the last Italian rows of the BOM got English text in `ROW_OVERRIDES`, the repository history was rewritten without those names, `primo.zip` rebuilt. The public copy is `docs/handoffs/ai-memory.md`: copy this file unchanged. Check before every push: `python3 publishing-upload/check_public.py --history`.
> **LOCOMOTION + MOTOR SELECTION NOW SHARED — 2026-09-21 (AI + user):** the user asked to share ALL the locomotion work ("the policy, the code, how we got there... everything") and the motor comparison. **(1) Locomotion:** the folder `umanoide/humanoid_locomotion/` (48 files, 11 MB, received from the Isaac workstation: policy `kneehard_model_2999.pt`, video, `params_as_trained/env.yaml+agent.yaml`, `code/tasks` + `code/assets` + `code/symmetry` + 14 diagnostic scripts, `HANDOFF.md` round by round, `LESSONS.md`, `RESULTS.md`, `NEXT_STEPS.md`, `setup/INSTALL.md`, `reference/`) has been copied BYTE-IDENTICAL into `umanoide-release/sim/isaaclab/` (it replaces the old placeholder "not in this folder yet"). Only addition: an "In this repository" section in `sim/isaaclab/README.md` (mapping `rl_full.urdf` = `sim/urdf/primo.urdf`; table of the `C:\Users\WKS\...` paths to be edited; policy I/O) + `sim/isaaclab/code/LICENSE`. **Facts VERIFIED today (not estimates):** from the checkpoint (tensor dimensions in the .pt zip) observation = **272** = lin vel 3 + ang vel 3 + gravity 3 + command 3 + joint pos 30 + joint vel 30 + last action 13 + height scan 187; action = **13** (12 legs + waist roll), target = default + 0.5 x action, **50 Hz** (dt 0.005 x decimation 4), MLP 512-256-128 ELU without obs. normalization; trained commands: forward 0-1.0 m/s, NO lateral, yaw +-1.0 rad/s via heading; joint order = the one resolved by Isaac Lab (`preserve_order: false`), to be read from the env before every deploy. The repo's foot mesh (`sim/meshes/Part_22_foot.stl`) has EXACTLY the extents expected by `simplify_foot_collision.py` (sole z = -0.7883, center x 0.0333, y -+0.1267, AABB 48.9 x 81.4 mm) -> `sim/urdf/primo.urdf` is the same export used for the training; it still has the mesh collision at the feet, so before converting to USD the script must be run on a copy. **License:** `code/assets`, `code/symmetry`, `code/tasks` have the Isaac Lab **BSD-3-Clause** header (text in `sim/isaaclab/code/LICENSE`); scripts, documents and policy remain CC0. No credentials/IPs in the files: only workstation paths. **NOT in the package (only on the workstation, optional because reproducible):** `rl_full_isaac/usd/rl_full.usd`, the URDF already patched at the feet, the checkpoints of the other runs (KneeTorque etc.), the tensorboard logs. **(2) Motors:** new `umanoide-release/docs/motor-selection.md` = short, public version of why RobStride: requirements, timeline 06-14 -> 06-23, Asimov's Encos map (5 models: A4310 x10, A4315 x4, A6416 x3, A5013-H x4, A3814-H x4), what Encos does better (Ø56/382 g vs Ø88/621 g at 36 Nm; -3.7 kg on the legs) and why it was NOT chosen (reduction 25-36:1 and harmonic drives 100:1 = reflected inertia 8x/16x/100x+, no backdrivability/force control and not upgradable via sw, worse on the ankle; quotation-only with no public CAD; ~3.5x the price; target moved from tethered ~28-30 kg to 45 kg with on-board battery, G1 class), RobStride vs CubeMars table by torque class, CubeMars dimensional error, other candidates, open points (hip yaw, AKE90-8 as a leg upgrade). Linked from the README (new "Motors" section), AGENTS.md, `docs/handoffs/README.md`, `docs/references.md` (new section with Asimov/Encos/CubeMars/Steadywin/MyActuator/ZeroErr/Dynamixel links). **CORRECTION to `MOTORI_TABELLE.md` (and its copy `docs/actuator-tables.md`):** it still had the headings "1. CHOSEN CONFIG — Encos" and "3b. CUBEMARS — CHOSEN SUPPLIER" and two CubeMars rows with the WRONG dimensions (AK70-9 "Ø70", AK40-10 "Ø46") = misleading for anyone who downloads it. Now: sect. 1 and 3b marked SUPERSEDED, sect. 4 RobStride = **CHOSEN**, wrong rows struck through and explained, "AKE90 Ø90" note corrected (Ø107.5: thinner, not slimmer). Backup of the previous file in the session scratchpad. **Asimov links:** `docs.menlo.ai/asimov/v1/bom` now returns 404 -> use `https://docs.menlo.ai/asimov/1`, `github.com/asimovinc/asimov-1`, `tally.so/r/jaG0va` (verified 200 on 2026-09-21). `Asimov 1 BOM.xlsx` and the vendor manuals are NOT redistributed. **Rule for the next sessions:** if `humanoid_locomotion/` gets updated from the workstation, copy it again into `sim/isaaclab/` with `rsync -a` while PRESERVING the "In this repository" section of the README and `code/LICENSE`, then rebuild `primo.zip` (now ~32 MB) and upload it to `gs://riverfamily/primo/`.
> **NAME = "primo" — PUBLICATION COMPLETED ON ALL PLATFORMS — 2026-09-19 evening (AI + user) [SUPERSEDES the two bullets below]:** the humanoid is called **primo** (chosen by the user among 10 proposals in the River Family style); listing title **"Primo open source humanoid robot"** (lowercase on the website and MakerOnline). GitHub repo renamed `AlessioPagliai/primo` (the old `umanoide` URL redirects); the local repo folder remains `~/Documents/artes/umanoide-release`. **COMMIT RULE:** author ONLY `Alessio Pagliai <alessiopagliai.d@gmail.com>`, NEVER a `Co-Authored-By: <AI name>` trailer nor the Mac's default identity (`utente1`); history of `primo` and the latest commits of `RiverFamily` rewritten and force-pushed on 2026-09-19; rule written in `~/Desktop/PUBLISH_GITHUB_AS_ALESSIO.md`. No "AI made" labels on the platforms. **URLs:** YouTube https://youtu.be/6nTcHpFmKbQ (4K60 H.264 closed-GOP, chapters; the two previous uploads were deleted by the user: the HEVC open-GOP master was being played back by YouTube in repeated 4 s blocks); website https://riverfamily.art/#primo (App Engine version `gallery-primo-20260919`: "more" = video only, GCS mp4 on desktop / YouTube iframe on mobile like the other designs; "make" = downloads `primo.zip`); Printables https://www.printables.com/model/1846831 (embedded video, 26 tags, 35 STL + 2 3MF); Thingiverse https://www.thingiverse.com/thing:7411626; Cults https://cults3d.com/en/3d-model/gadget/primo-open-source-humanoid (1:1 images, 30 s clip, CC0, free); Creality Cloud https://www.crealitycloud.com/it/model-detail/6aae7192f052c066aeb8dd96 (listing complete but REJECTED by moderation: the cover must be a real photo of the print; not visible to the public, therefore NOT linked in the docs; Creality has no drafts: the rejected listing stays private and editable and serves as a draft (the user said to leave it like this); when the photos are available: profile › 3D Model › ⋯ › Edit, photo as cover, name "Primo open source humanoid robot", resubmit); MakerOnline https://www.makeronline.com/en/model/primo%20open%20source%20humanoid/331171.html; MakerWorld: draft 9688828 resubmitted, again automatically REJECTED (no real photo) and then SAVED AS DRAFT at the user's request (3D Models › Draft; the old "umanoide" draft is also there, to be deleted by hand) — without a REAL PHOTO of a printed part it always gets rejected (the user will take the photos in a few days); the MakerWorld video slot does not accept programmatic upload: drag `publishing-upload/video/primo-30s.mp4` in by hand. **Self-contained shared folder:** `gs://riverfamily/primo/primo.zip` = the whole repo (README, AGENTS.md as the entry point for a new AI session, this memory in `docs/handoffs/ai-memory.md`, BOM + generator, electrical schematic, `cad/stl/` = ONLY the 20 parts to be printed, in mm, right+left = 35 STL; the purchased components are in the BOM and their meshes only in `sim/meshes/` for the URDF `sim/urdf/primo.urdf`, mirror pipeline, Isaac/teleop handoffs). MISSING from the repo: the Isaac Lab training code, which is on the workstation (placeholder `sim/isaaclab/README.md`). Other GCS files: `primo/primo-stl.zip`, `primo/videos/{primo-4k60,primo-30s,walk-kneehard,walk-kneetorque}.mp4`, `videos/Primo_720p.mp4` (website). Texts, tags and URL list: `umanoide-release/publishing/platform-texts.md`. Walking policy chosen: KneeHard. RiverFamily repo: removed the `SECRET_KEY` line from `app.yaml` (it was a placeholder not used by `app.py`, different from the key of the live site: no real secret exposed, no history rewrite needed); the Stripe `pk_live_` in `templates/index.html` is a publishable key by design. WARNING Printables: after every edit check that the description is not empty (the ProseMirror editor replaces the selected node: insert the video in an empty paragraph between two paragraphs, never with everything selected).
> **OPEN SOURCE PUBLICATION — RELEASE PACKAGE PREPARED — 2026-09-19 (AI + user):** the user is publishing the project today on GitHub (account `AlessioPagliai`), Printables/MakerWorld/Thingiverse (@River_Family / @RiverFamily), riverfamily.art and YouTube (@art.riverfamily). Style learned from his sites: **extreme minimalism, lowercase names, English, descriptions of 0-15 words, no marketing, CC0 license, large files on the GCS bucket `gs://riverfamily/`, links to all the platforms**. Working name: `umanoide`. Created a clean folder **`/Users/artes/Documents/artes/umanoide-release/`** (local git repo, 1 commit, 1.6 MB): `README.md` (numbers, phases/costs, files, sim, open points, license), `bom/` (bom.xlsx + bom.csv 108 active rows + build_bom.py), `electrical/` (scheme md/svg/png), `cad/` (README with Onshape link, `motor_proxy.fs`, `3mf/ankle-gimbal.3mf` = Bambu PPA-CF H2C 1 wall 90% grid, `3mf/leg-test-plate.3mf` = femur+hip bracket+tibia in PLA on H2S), `sim/` (mirror_urdf.py, ankle_map.py + ankle-transmission.md WITH WARNING "provisional geometry from mesh centroids", g1_joints_reference.csv), `docs/` (hand-design, actuator-tables, references.md with 27 arXiv papers + vendor links, `handoffs/` = isaac/teleop/mirror-debug + **ai-memory.md = copy of this MEMORY.md**), `publishing/platform-texts.md` (ready-made texts for each platform, catalogue.json entry, RiverFamily README block, list of images to be made in Onshape), `LICENSE.md` CC0 (copied from RiverFamily). **Deliberately EXCLUDED:** `sources/` (papers, 400 MB: list only), `motors/`+`hands/` (vendor manuals/STEP: links only), `hydrogen/` and `noetix_manual/` (unrelated projects), `Asimov 1 BOM`, `G1.blend`, `outputs/`. **Uploaded to GCS (public):** `gs://riverfamily/umanoide/umanoide-urdf.zip` (11.8 MB = rl_full: urdf+mesh+handoff) and `videos/walk-kneehard.mp4`, `walk-kneetorque.mp4`. BOM totals as of 2026-09-19 unchanged: remaining 10.264,90 / F1 4.008,57 / F2 3.997,95 / F3 2.258,38; mass 33,24 kg. **TO DO:** Onshape images/GIFs from the user (`images/hero.webp` referenced in the README), Onshape document made public, creation of the GitHub repo `AlessioPagliai/umanoide` + push (terminal NOT authenticated: `gh auth login` or a PAT is needed, or else upload via browser), 3MF upload to Printables/MakerWorld/Thingiverse, YouTube video, website entry. Locomotion policy note: `KneeHard.mp4` vs `KneeTorque.mp4` (compare_r5 = sweep KneeDefault/Soft/Hard + KneeTorque); config on the Isaac workstation, not here.
- **PUBLISHED — 2026-09-19 (AI, autonomous session):** GitHub https://github.com/AlessioPagliai/umanoide (local repo `umanoide-release/`, branch main); Printables https://www.printables.com/model/1846831-umanoide-open-source-humanoid-in-design (RC & Robotics, CC0, origin "original", AI flag = "AI-assisted" chosen out of caution: can be changed in Edit model); Thingiverse https://www.thingiverse.com/thing:7411626 (Hobby › Robotics, Work in Progress, CC0, 2 3MF + 5 images); MakerWorld: draft 9686078 complete (texts, Robotics category, tags, cover 4:3+3:4, 4 images, print profile ankle-gimbal.3mf, CC0) SUBMITTED but REJECTED by the automatic check: "The system did not detect any real photo" → a REAL PHOTO of a printed part (gimbal or leg test plate) is needed in the model images and in the print profile, then resubmit from 3D Models › Failed › Edit (or "Appeal"); for now the docs contain the profile link https://makerworld.com/it/@RiverFamily, TO BE REPLACED with the model link as soon as it is approved (release README "Also on", publishing/platform-texts.md, README + catalogue.json of the RiverFamily repo, YouTube description); the MakerWorld print profile has only CAD renders, MakerWorld asks for a real photo of the printed part → add it as soon as the gimbal is printed, otherwise it may remove the profile; profile name left as the automatic one "0.2mm layer, 1 walls, 90% infill". YouTube https://youtu.be/bHGGjXYELUE (CAD tour, description with all the links). Website: App Engine version `gallery-umanoide-20260919` promoted (slide `#umanoide`, "more" section with CAD · files · 3MF · video; the website does not link the platforms for any model, consistent). RiverFamily catalogue repo (`/Users/artes/Documents/paths/Ben/riverfamily-github`) updated and pushed. GCS: gs://riverfamily/umanoide/ (zip, urdf zip, images, videos). Browser upload staging: `publishing-upload/` (jpg 4:3/16:9/1:1/3:4 with white padding). Walking policy chosen: **KneeHard** (the simplest one; KneeTorque adds a penalty term on the torque; the configs are on the Isaac workstation, locally only the videos). Walk videos on GCS: videos/walk-kneehard.mp4, videos/walk-kneetorque.mp4.

> **CUSTOM 15-DOF DIRECT-JOINT HAND DEVELOPMENT — 2026-07-19 (AI + user; PLANNED PROJECT WORKSTREAM, ACTUATORS NOT YET LOCKED):**
> - The project explicitly includes designing and open-sourcing its own five-finger hand with **3 independently actuated DoF per digit = 15 actuators/hand**; this is not merely an optional market comparison. For index through little finger: MCP ab/adduction, MCP flexion, PIP flexion; DIP may be passive/coupled. The thumb must instead implement CMC opposition/reposition, CMC/MCP flexion and IP flexion; do not copy the four-finger axes blindly. The preferred design has an actuator physically at each joint, not tendons, if a genuinely suitable commercial module exists.
> - **Development sequence:** start the first humanoid build with the proven `RH56DFX-2L/R` hands, while developing the custom hands in parallel through single-finger prototypes. Do not remove Inspire from the active BOM/CAD until the custom hand is complete and passes force, backlash, heating, impact and lifetime tests. The custom hand is intended as a later replacement and open-source project deliverable; only its actuator selection remains open.
> - `DYNAMIXEL XC330-T288-T` and `XL330-M288-T` share the same `20 x 34 x 26 mm` envelope, absolute magnetic encoder, current feedback/control and TTL multidrop concept, but are not equivalent internally. XC: 23 g, metal gears, coreless motor, 6.5-12 V, 1.00 Nm stall at 12 V, about 0.20 Nm conservative normal-use estimate, about EUR 110.40. XL: 18 g, plastic gears, cored motor, 3.7-6 V, 0.52 Nm stall at 5 V, about 0.104 Nm conservative estimate, about EUR 40.20. XC is roughly 2x stronger and more impact-resistant but about 2.75x the price; XL is the rational choice for protected palm/forearm tendon actuation. **Both are too bulky for a human-scale motor at every PIP:** the 20 mm bare thickness becomes roughly 24-28 mm with structural cheeks/opposite support, and the 34 mm body consumes most of a phalanx.
> - **Current direct-joint retail prototype candidate: `Waveshare SC09` / Feetech `SCS009`.** Exact published values: `23.2 x 12.0 x 25.5 mm`, 12.5 g, 4-6 V, metal gears, carbon-film potentiometer, 1024 positions over 300 deg (0.293 deg), TTL serial to 1 Mbps, position/load/speed/voltage feedback, no measured-current control and no temperature feedback. Published **rated torque = 0.7 kgf.cm = 0.0686 Nm**; stall torque = 2.3 kgf.cm = 0.2256 Nm; no-load speed 100 rpm; stall current 1 A at 6 V; about USD 8.99. Product/CAD/docs: <https://www.waveshare.com/SC09-Servo.htm> and <https://www.waveshare.com/wiki/SC09_Servo>.
> - **Torque comparison must not be lost:** XL330 is about `0.104/0.0686 = 1.52x` stronger in conservative normal use and `0.52/0.2256 = 2.30x` stronger at stall than SC09. Approximate output force using torque/lever (before linkage/contact losses): at a 70 mm MCP lever, SC09 rated/stall = `0.98 / 3.22 N`, XL330 estimated-normal/stall = `1.49 / 7.43 N`; at a 30 mm PIP lever, SC09 = `2.29 / 7.52 N`, XL330 = `3.47 / 17.33 N`. Stall values are momentary and must never be presented as sustainable grip. SC09 wins packaging/cost, not torque or control quality.
> - Fifteen direct SC09s would be about 187.5 g and USD 135 per hand, with a theoretical all-stalled demand of 15 A at 6 V. This is dimensionally plausible but a **light-manipulation hand**, especially because MCP rated fingertip force is only about 1 N per digit. Its reported `load` is not a calibrated torque sensor. XL330 gives better sensing/control and torque but is geometrically poor on the fingers.
> - Other commercial leads: `KST X06` (`20 x 7 x 16.6 mm`, 6 g, 0.04 Nm rated / 0.176 Nm stall, PWM and no runtime telemetry) physically fits but is weak; `AGFRC A20CLS` (`23 x 12 x 27.5 mm`, 20 g, 0.735 Nm advertised stall, PWM/potentiometer, no normal runtime joint/current telemetry) is stronger but poor for state logging; Harmonic Drive `RSF-3C` is a real robot-grade finger actuator (about O20 x 47 mm, 31 g, 0.03-0.11 Nm rated and 0.13-0.30 Nm maximum depending ratio) but requires an external driver and is industrial/quotation-priced; Bonsystems `BCSA Micro` is advertised specifically as an O18 mm cycloidal direct finger actuator but currently has no public torque, mass, length, encoder, bus, price or retail-stock data, so it is not BOM-ready.
> - **Next gate before choosing 30 motors:** buy/build one complete three-DoF finger or at minimum a two-flexion-joint finger, then measure sustained fingertip force (not stall), backlash/deadband, loaded position error, temperature over repeated grasps, impact survival and bus update rate with multiple nodes. Do not freeze CAD around SC09, XL330 or BCSA Micro before this test. A mixed XL330+SC09 hand would require separate protocol/UART handling even if both are powered near 5 V.

> **HANDS-ON-WEHO DECISION + ELECTRONICS AUDIT FIXES — 2026-07-17 (AI + user):**
> - **User decision: the RH56DFX-2L/R hands are CONNECTED from the very first build on the single WEHO 24 V rail** (supersedes the "no hands" of the 2026-07-12 lock below). Budget: Thor cap 130 W (5.4 A) + 2 hands at 2 A max published (96 W) + hub/interfaces ≈ 241 W vs 240 W rated / OCP 12 A: over budget only at a fully simultaneous peak. Mitigations: lower the Thor nvpmodel during sustained bimanual work, stagger the hand commands in software, bench-log the rail voltage/current with both hands gripping under full GPU load. CAVEAT: the Inspire integration manual recommends provisioning up to 5 A/hand; if the measurements get close to that value the WEHO is undersized -> switch to RSD-300C-24 or Cincon CHB350.
> - **OPEN POINT (decide before wiring the hands branch):** with the hands on the NON-switched branch, the e-stop does NOT remove power from the hands (the old dedicated Omron relay had been removed). If the hands must release on e-stop, add a small 24 V relay in the 15 A hands branch driven by the same e-stop chain.
> - **BOM corrections applied 2026-07-17 (AI audit, generator `build_umanoide_tab.py` + regeneration):** (1) hands, Waveshare 2CH RS485 adapter, LINDY 36940 cable and hands MINI 15 A fuse reactivated qty>0; 24 V output fuse holders raised to qty 3 (Thor + hands + hub). (2) New design row `SEQ-PWR-01` (precharge sequence + coil drivers): the Eaton timer and the key selector switch had been removed and the carrier board cited in the notes was qty0, so NOTHING implemented "precharge before main" nor the automatic-restart lockout; Thor GPIO cannot drive 24 V coils directly. Until release: written manual two-switch procedure, never close the LEV100 on a discharged bus. (3) Coil suppression restored: new active row `1.5KE33CA` on the 24 V coils (raised to qty 3 on the same day: LEV100 + CIT precharge + CIT latch); the old 1.5KE68CA row (sized for the removed 48 V coils) marked [REMOVED qty0]. (4) New row `[TO DESIGN qty0]` low-ESR capacitor >=22 uF at the WEHO output (required by the datasheet, previously present only in the README). (5) New row `[ORDER WITH BATTERY qty0]` for the robot-side XT90-S mate (it was missing; confirm the connector gender on delivery of the pack). (6) Phases corrected to make the bench bring-up consistent: LEV100, CIT, WEHO + input fuse/fuse holder, Thor 10 A fuse and output fuse holders -> Phase 1 (the coils are 24 V: without the WEHO on the bench the e-stop chain does not exist). (7) Obsolete notes corrected: safety control branch now documented as a 24 V branch from the WEHO rail (not "48 V with timer and key"); hands fuse note now cites the WEHO rail (not CHB350); HAR-ARM-01 now includes the 24 V hands power pair + RS485 twisted pair in the arm trunk.
> - **EXCEL TOTALS RECALCULATED AND VERIFIED 2026-07-17** (the totals "31.243,22 / 35,043 kg" written on 2026-07-12 were the midday snapshot WITH hands qty1 and had never been updated after the evening qty0 — handoff error): **Complete humanoid EUR 30.395,59; Phase 1 EUR 10.076,77 (of which Thor 4.026,00); Phase 2 EUR 494,56; Phase 3 EUR 19.824,26; purchased on-board mass 33,082 kg** (actuators 20,913 kg unchanged, battery 2,270 kg). Note: the active WEHO row still has price 0 pending a quotation, so the total underestimates by a few tens of EUR.
> - README updated in the same session: hands in the first build, Phidgets link corrected (prodid=1205, row 17 pointed to 1096), SEQ-PWR-01/TVS/capacitor rows, pre-power-up checklist extended. The historical sections further down in this file ("Electrical and safety", old CANable V2.0 note) are marked as superseded.
> - **PRECHARGE SEQUENCE SOLVED IN HARDWARE — 2026-07-17 (same session, user decision "simple component"):** no custom PCB. Chain: `24 V safety fuse -> e-stop NC -> Schneider XB5AA31 START pushbutton + CIT A2K1CSQ24VDC1.6 self-holding latch relay (second unit of the same SKU as the precharge) -> CIT precharge coil + Omron H3YN-2 DC24 ON-delay timer on PYF08A-E socket -> timer contact -> LEV100 coil`. START starts the precharge and the delay; the timer closes the LEV100 on an already charged bus; releasing the e-stop NEVER restarts the bus, only START does. Brand-name timer on purpose: a timer that closes early silently defeats the precharge and can weld the main contactor. Calibration: measure the real precharge tau by watching the RobStride VBUS telemetry on the bench, set 4-5 tau (initial guideline 10 s); Thor gates the motor enable in software but is NOT in the safety chain. `SEQ-PWR-01` in the BOM is now the "wiring drawing" deliverable. Envelopes (verify the exact drawings before the CAD freeze): latch 26.5 x 32 x 33.5 mm; timer+socket about 25 x 35 x 80 mm standing (or lying down); START panel hole Ø22, about 45 mm behind the panel, next to the e-stop; added mass ~0.15 kg, cost ~EUR 66 net (XB5AA31/H3YN/PYF08A prices to be verified at order).
> - **URDF PIPELINE + MIRROR SCRIPT — 2026-07-18:** the user models in Onshape ONLY the right side + the central chain (export in the `~/Downloads/rl/` format: urdf/rl.urdf + STL meshes). New repo script `mirror_urdf.py`: renames the 17 revolute joints with G1-style semantic names (map inside the script, identified via FK), converts continuous->revolute with sign-corrected G1 mode_11 limits + effort from the RobStride peak (virtual ankle 72/36 Nm PROVISIONAL) + PROVISIONAL velocities, mirrors the leg (subtree part_42) and arm (part_12, excluding the part_49/50 branch) subtrees with world-frame math for the crossing joints and conjugation D=diag(1,-1,1) inside, axes (-ax,ay,-az) => same command = mirrored motion and identical limits, inertias with Ixy/Iyz flipped, truly mirrored STL meshes (flip y + winding, no negative scale), first-pass collisions on pelvis/torso/thigh/shin/foot. Output `~/Downloads/rl_full/`. VERIFIED: 30 revolute joints in total, symmetry 0.000 mm on all pairs. TO DO IN ONSHAPE: missing materials/masses (total export 3.63 kg vs ~15 expected: all the imported STEPs - motors, hands, camera - have mass ~0; assign mass overrides from the manuals), real collisions, confirm the identity of part_42/49/50, neck limits and velocities from the datasheets.
> - **PHASES REDEFINED + OWNED ITEMS + SUPPLIERS — 2026-07-19 (evening; SUPERSEDES the "MS1 column" mechanism of the bullet below):** the user asked that milestone-1 BE Phase 1, not a parallel column. Done: **MS1 column removed; the Phase column now follows the real build order**: Phase 1 = right arm bench + hand + ankle kit + battery/dual-source + safety chain + Thor; Phase 2 = legs and locomotion (RS04/RS03, dedicated ankle RS06, leg wiring, IMU); Phase 3 = completion (left arm/hand, waist, neck, audio, mobile). The rows that spanned several phases have been SPLIT in the generator (`ROW_SPLIT`: 5 arm motor rows RIGHT/LEFT, upper BCCA4011 8/9, MIDI fuse holders 2/2/2, arm fuse 30A 1/1, CANable 1/2); phase corrections for the rest via `PHASE_TO`. **OWNED (lab): Thor and BOTH RH56DFX hands** — counted at EUR 0 with the reference price in a note; Thor is used RIGHT AWAY in Phase 1 (no PC-only plan; Molex J74 + 10 A fuse moved to Phase 1). **SUPPLIERS (user preference, CORRECTED in the evening after a fair objection by the user):** the first attempt (changing only the supplier column while leaving the original item/link) was INCONSISTENT and has been reverted. Final rule implemented: the supplier is changed ONLY with a verified REAL equivalent (item+SKU+link+supplier together), otherwise the specialist source stays. **Swaps verified on the web 2026-07-19:** Klauke 704F5/703F5/101R5 cable lugs → **Bürklin** (same exact SKUs, order numbers 07F1391/07F1381/07F2090, product links verified); e-stop → **Schneider XB4BS8442 on RS Italia** (RS 7951306: same Ø40 red mushroom head twist-release 1NC, METAL XB4 version of the plastic XB5AS8442 — verify the 1NC block and the price at order; README/schematic/SVG and MASSA_UNIT 0.070 updated too). **Second round on user input (same evening):** Belden → **Farnell 1891187**: the **9841NH is the halogen-free/LSZH version of the 9841**, sold BY THE METRE (order 50 m; row price still that of the Rapid reel, verify the Farnell total at order); **K05 → Bürklin 05L2734** (same cart as the cable lugs; also RS 398-2270); **Schuko cable → generic Amazon** (commodity: any H07RN-F 3G1.5 ≥3 m with Schuko plug, previous reference Craft EHK22146 in a note). Docs synchronized (schematic md+svg now cite 9841NH). **Deliberately kept (no sensible equivalent in the big stores):** Nautica Illiano for the 25/16/6 mm² cables (RS sells the super-flex H01N2-D only in 50-100 m reels; Nautica sells by the metre) and Accu for the LEFT-HAND M8 lock nut (niche; verify whether the AliExpress pushrod kit already includes them). NOTE DIN 439: the two lock nut rows are NOT a duplicate — one is RIGHT-HAND thread (for the KARM), one LEFT-HAND (for the KALM): the pushrods are RH+LH turnbuckles; the left-hand thread is a niche item (verify whether the AliExpress pushrod kit already includes them). New totals = remaining spend: complete 10.264,90 / F1 4.008,57 / F2 3.997,95 / F3 2.258,38.
> - **MS1 = FIRST PURCHASE (milestone defined with the user) — 2026-07-19 [SUPERSEDED by the bullet above: MS1 column removed, now Phase 1]:** first physical bench: **1 right arm** (motors: RS06 x3 + RS00 x4; the 2 RS06 will also act as ankle motors for the tests — NO dedicated ankle RS06 and NO RS04), **linkage kit for 1 ankle** (shoulder screws 45/16, M6 nuts, pushrods 140/40, KARM/KALM, DIN439 lock nuts), **right hand RH56DFX-2R** + 2CH RS485 adapter + LINDY 36940, **P45B battery + charger + XT90 mate** and **dual bench power supply: battery AND mains TOGETHER** — new requirement: they are NEVER put in direct parallel (the RSP-3000 would float the 13S pack without control, mutual back-feed) -> new BOM row `[TO SELECT qty0] Dual-source 48 V OR-ing stage` (ideal-diode per branch, LTC4357/LM5050 class, <=20 A for the arm bench; INTERIM: swap the source at the XT90-S, never both). Complete safety chain included (e-stop/START/latch/timer/TVS/LEV100/precharge/PDU/fuses). **Thor NOT in MS1**: the fixed-arm bench is commanded from the PC/workstation with 1 CANable Pro + RobStride debug adapter (Thor is needed only for mobility). Torso printed and fixed to the table (screws/inserts/filament non-BOM). D436 included for teleop/training data. Seeed XT30(2+2) Power Separation Board row ACTIVATED qty2 Phase 1 (power/CAN junction of the arm daisy-chain + location for the terminations, until JBOX-CAN-01 exists). **Implementation: new Excel column `MS1 qty` (col U)** written by the generator (MS1 list in `build_umanoide_tab.py`): filter the column to get the exact shopping list; the MS1 qty are FRACTIONS of the row qty (e.g. shoulder pitch/roll 2 of 4). **Priced MS1 total: EUR 12.085,36 VAT incl.** (hand 8.099 = 67%; motors 1.298; rest ~2.688), + unpriced rows to be quoted: igus KARM/KALM, charger (with battery), WEHO, 22uF capacitor, OR-ing stage. ORDER GATES still open before buying: battery (shipping to Italy/BMS/regen), igus KALM availability, DFX hand GX12 pinout to be confirmed with Inspire, XB5AA31/H3YN/PYF08A prices. Overall totals updated (separation board activated): complete 30.489,23 / F1 10.170,41.
> - **META QUEST TELEOP — MODE A CHOSEN, HANDOFF TO THE WORKSTATION — 2026-07-19:** the user wants to teleoperate the humanoid in Isaac Sim with a Meta Quest while being far away (he watches the workstation via AnyDesk and has the Quest with him). Decision: **Mode A** = Quest as tracker ONLY, the Isaac viewport is watched in 2D via AnyDesk (NOT immersive stereo in the headset = Mode B/CloudXR, discarded). Key fact: **AnyDesk does NOT carry the Quest tracking** — the poses need a separate network path (Tailscale overlay, or a public cloudflared/ngrok tunnel). The poses are tiny (~72 Hz) and travel well over the internet; the hard part (stereo video to the headset) is not in this design. Mandatory control split for a humanoid: **legs = autonomous RL policy commanded by thumbstick (vx,vy,yaw), NOT a joint-by-joint puppet** (latency kills balance); arms (7/side)/hands (RH56DFX 6 DOF/side)/neck = retargeted teleop (latency-tolerant). Wrote `TELEOP_HANDOFF.md` (in the repo) for the AI session on the workstation: architecture, phased plan (0 network -> 1 poses arriving -> 2 arms+simple grip, legs still -> 3 walking command -> 4 dexterous hands+neck), recommended stack Open-TeleVision/Vuer (WebXR in the Quest browser, poses via WebRTC; use a passthrough/immersive-ar session so that the operator still sees the 2D AnyDesk screen), dex-retargeting for the Inspire hands (phase 4). Explicit "VERIFY LOCALLY" section: Isaac/Isaac Lab version and its IK API, state of the Open-TeleVision repo, command interface of the walking policy — to be confirmed on the workstation, not to be taken for granted from memory. The execution is done by another conversation on the workstation; this Mac session only produced the handoff. **ERGONOMICS — TWO SETUPS, user still undecided (2026-07-19):** **A1 = Quest around the neck**, head out, watching the external AnyDesk screen, poses uplink only (simpler for the bring-up); constraints: proximity sensor to be disabled (tape + auto-sleep off) or the session dies, headset pose = torso reference (no head-tracking, no head->neck), controllers tracked well only in front of the torso, timer-based calibration. **A2 = Quest worn normally on the head + Isaac view inside the headset as a 2D PANEL** (mono video via the video-back channel of the teleop stack, NOT stereo/CloudXR): this is what the user means by "streaming the AnyDesk screen to the Quest" — it is implemented by having the stack stream the Isaac viewport onto a panel, NOT by running the AnyDesk app on the Quest (a 2D window and an immersive tracking session conflict). A2 is PREFERRED: it recovers head-tracking (-> head->neck available), natural controller FOV (hands in front of the face), no proximity problem; cost = one mono video over the internet to the headset (latency on the view is tolerable, the legs are autonomous). RECOMMENDATION in the handoff: bring-up with A1 poses-only (phases 0-2), then move to A2 by adding the viewport->panel stream. Handoff `TELEOP_HANDOFF.md` updated with both.
> - **ANKLE: DIFFERENTIAL TRANSMISSION MAP DERIVED FROM THE CAD — 2026-07-19 (major result):** discovered that the Onshape export ALREADY contains the pushrod geometry: the parts joined by a Group mate have their frame at the global origin and their mesh in global coordinates, so the positions of the pins (shoulder screws) can be extracted. Real geometry extracted (right leg, mm): **crank 47.75 (both motors, horizontal at zero), pushrods 208.01 (upper) and 106.01 (lower) eye-to-eye, pitch arm 47.75, roll semi-span 43.83, pushrods VERTICAL at zero pose with cranks at 90° (optimal transmission)**. This resolves the old BOM question: the AliExpress length is that of the BODY, eye-to-eye = body + ~68 mm. New file `ankle_map.py` (exact IK/FK with closed-loop solve, Jacobian, torque envelope, workspace scan; round-trip validated to machine precision) + `ANKLE_TRANSMISSION.md`. **Ratios: pitch = -0.500 x (th1+th2) = 1:1; roll = -0.545 x (th2-th1) = 1.09:1.** Motor travel for the URDF limits: ±43° pitch, ±14° roll (within RS06). **DECISION CONFIRMED: do NOT simulate the pushrods as bodies** (URDF does not do closed loops, Isaac could but it is fragile/slow and pointless); the map is analytical and lives outside the policy (deploy: policy (pitch,roll) -> ik() -> 2 RS06; feedback -> fk() -> observation). What MUST go into the sim is the COUPLED torque envelope.
> - **ANKLE — KEY NUMBERS 2026-07-19:** (1) **Torques: pitch 72.0 Nm / roll 66.1 Nm pure at neutral, coupled as a diamond `|t_pitch|/72 + |t_roll|/66 <= 1`** (not a box!). URDF corrected: the roll effort was 36 Nm by eye, the derived value is **66 Nm** (it was 1.8x too conservative); pitch 72 was right. (2) **The pitch torque DEGRADES in plantarflexion: 72 Nm at neutral -> 66.8 at -15° (typical toe-off) -> 46.0 at -50°.** The estimated requirement in push-off at 45 kg is ~67 Nm: **we are exactly at the limit**, comfortable at 35-40 kg, zero margin at 45 kg. Do NOT touch the CAD now: measure the real demand in Isaac (same philosophy as the hip yaw gate); if it saturates, the fix is a **shorter crank** (40 mm -> 86 Nm) at the cost of ankle speed and pushrod force (754 N -> 900 N, KARM-08 CL withstands 1.7 kN short-term). (3) **Continuous 22 Nm pitch / 20.2 roll**: implies the CoM while standing within ~50 mm of the ankle axis, otherwise a thermal problem (CoM at 90 mm would require 40 Nm continuous) -> add a reward term that keeps the CoP at mid-foot. (4) **ROD-END: alarm cleared.** Worst per-end misalignment over the whole workspace = **15.7°** (at max roll) versus the **35°** of the igus KARM/KALM-08 CL; pitch costs ~0° (rotation about the pin). So the old plan of limiting roll to ±12° and the conical-spacer/ball-stud upgrade paths are NOT needed: the full ±15° of roll are OK. (5) Zero unreachable poses and no singularity in the range.
> - **TRAINED POLICY "SUPER BROKEN" — DEBUG HANDOFF TO THE ISAAC PC — 2026-07-19:** the user trained a policy on `rl_full.urdf`, result broken; cause not yet isolated (mirroring? PD/reward/training-side? missing collisions on the arms? provisional velocity/effort?). Wrote `MIRROR_DEBUG_HANDOFF.md` (repo + copied into `~/Downloads/rl_full/`, inside the new zip `rl_full_isaac.zip`) for the AI session on the Isaac PC: it summarizes what has ALREADY been verified independently (symmetry 0.000 mm on 13 pairs, axis convention "same command = mirrored motion + identical limits", COM y=0.1mm, connected chain) so as not to re-derive everything from scratch, lists the real suspect PROVISIONAL values (all the velocities, ankle effort 72/36 Nm, neck limits, hip yaw 36 Nm RS06 vs RS03 gate), the known gaps (no collisions on arms/wrists, foot collisions = full visual mesh, not a primitive) and a step-by-step debug order with the 4 acceptance tests of `ISAAC_HANDOFF.md`. Key message for the other session: if tests 1-2 pass but only the trained policy is broken, the problem is almost certainly reward/PD/action-space on the Isaac Lab side, NOT the mirroring — do not restart from the already verified geometry audit. `mirror_urdf.py` copied into the zip so that the other session has the source directly without having to ask for copy-paste.
> - **COMPLETE URDF READY FOR ISAAC + SECOND AI SESSION ON THE ISAAC PC — 2026-07-18 (afternoon):** `mirror_urdf.py` is now fully automatic and robust: (1) auto-match of the joints by world POSITION (REF_POS, tolerance 40 mm — immune to renumbering/renaming by the exporter); (2) auto-derivation of the subtrees to be mirrored, excluding the central branches (Thor/WEHO under the shoulder stator); (3) AUTO-REPAIR of the hung leg: the Onshape exporter loses an edge of the Group mates (the CAD is correct!) and hangs the leg from the world with an inverted chain — the script re-roots it (pitch->roll->yaw) and re-attaches it to the pelvis from the preserved world poses, with a warning; (4) masses injected by token in the name (rs04/rs03/rs06/rs00/rs05/rh56/d435/battery/thor/weho/eaton/lev100/imu — the user's renames in Onshape identified all the electronics in the CAD); the mass override of the Onshape Properties panel is NOT exported: never trust it, the script sets the masses; (5) safety floor of 0.05 kg on moving links <5 g; (6) token-based collisions (15 bodies: pelvis/ribcage/feet/leg). VERIFIED: 30 revolute, symmetry 0.000 mm on 13 pairs, total mass 32.25 kg, hip chain correct. Output `~/Downloads/rl_full/` + `ISAAC_HANDOFF.md` (also in the repo) + zip `rl_full_isaac.zip` for the Isaac PC (a second AI session active there, monitored via AnyDesk; sessions do NOT transfer between machines: the handoff goes through MEMORY.md + ISAAC_HANDOFF.md). Division of roles: Mac = CAD/BOM/generates rl_full; Isaac PC = USD import + Isaac Lab + training. The Isaac AI session must NOT clean up the raw rl.urdf (half robot, placeholder masses): use ONLY rl_full.
> - **HIP YAW AUDIT RS06-vs-RS03 — 2026-07-18 (requested by the user; the CAD mounts RS06, the locked map says RS03):** vertical axis ≈ zero gravitational torque, only the dynamic peak matters (turning + foot pivot friction). Estimates in memory: ~28 Nm at G1-class mass, ~36 Nm at 45 kg in an aggressive turn = EXACTLY the RS06 peak -> zero margin (reason for the RS03 upgrade of 2026-06-21: 60 Nm, +0.259 kg and +Ø10 mm each). DECISION DEFERRED TO THE SIM GATE (now possible with Isaac): URDF with effort 36 Nm (RS06 as per CAD); log the hip-yaw torque while turning at ~32+ kg; if it saturates >2-5% of the steps at the target turn rates -> RS03 (order + CAD Ø98); otherwise the BOM row is downgraded to RS06. Gate note also written in the RS03 hip yaw BOM row. The gate BLOCKS the Phase 1 leg motor order.
> - **INSPIRE HAND MANUALS DOWNLOADED AND CONNECTION VERIFIED — 2026-07-18:** new folder `hands/` with 5 official PDFs: RH56 SERIES USER MANUAL V1.0.9 (2024-01, pinout + register/MODBUS protocol), DEXTEROUS HANDS INSTRUCTIONS, PC INSTRUCTIONS, RH56DFTP User Manual V1.0.0 (recent-generation reference) and Selection Guide 2026-02. Verified facts: **RH56DFX = RS485/CAN, DC 24 V ±10%, quiescent 0.09 A, PEAK 2 A (official DFX confirmation of the WEHO budget; the "5 A" was only a provisioning recommendation), 540 g.** Interface from the series manual: ONE single **GX12 5 pin** aviation connector per hand carrying power and RS485 together (1 GND, 2 VCC 24 V, 3 A+, 4 B−, 5 GND); RS485 default 115200 bps 8N1, register protocol 0xEB90 or MODBUS RTU, HAND_ID per hand (assign left=1, right=2), up to 254 hands per bus. GATE: confirm at order time that the DFX connector/pinout is unchanged (dedicated DFX manual not published — ask Inspire for it). Electrical scheme (md+svg), hand BOM notes and RS485 adapter updated with these data.
> - **COMPLETE ELECTRICAL SCHEME 2026-07-17:** new deliverable `ELECTRICAL_SCHEME.md` (written scheme: sources, 48 V distribution with the 5 motor branches and the 30 actuators, 24 V rail, safety chain, complete Thor port map, CAN rules, pre-wiring gates) + drawing `electrical_scheme.svg` / `electrical_scheme.png` (3 zones: POWER 48 V, SAFETY CHAIN 24 V, DATA). Update both together with the BOM whenever components or topology change. Totals after TVS qty3: EUR 30.477,03 / Phase 1 10.158,21 / mass 33,233 kg.

> **CURRENT POWER / PACKAGING LOCK — 2026-07-12 (AI + user):** [UPDATED 2026-07-17: the hands are now CONNECTED to the WEHO rail by user decision — see block above; everything else remains valid.] The active first mobile walking configuration is **no hands** and uses one `WEHO WH-C482410` sealed non-isolated 48 V -> 24 V, 10 A, 240 W converter (`74 x 74 x 32 mm`, `0.300 kg`, manufacturer-direct link: <https://www.wehopower.com/product/48v-to-24v-10a-240w-dc-to-dc-converter>). It powers Thor capped to 130 W, the powered USB hub and small interfaces only. It does **not** have enough verified power margin for Thor plus two RH56DFX hands. Bench validation is mandatory: Thor boot transient, sustained GPU load, converter thermal rise, 24 V ripple and EMI. WEHO requires an external low-ESR capacitor >=22 uF at its output; have an electrical engineer select/mount it at the converter output.
>
> - [SUPERSEDED 2026-07-17: hands, dual-RS485 board and USB-C-B cable are ACTIVE again qty1 on the WEHO rail — see block at the top.] Hands `RH56DFX-2L/R`, Waveshare dual-RS485 board and its USB-C-to-B cable were **deferred qty0** in the BOM on 2026-07-12.
> - `Cincon CHB350-48S24` + `UHG-PWR-001` are **qty0 alternatives**, not active: very compact but require a properly designed/released carrier PCB. The off-the-shelf no-custom-PCB fallback is `MEAN WELL RSD-300C-24`, `216 x 96.5 x 40 mm`, `1.19 kg`; it supports later hands but has a severe rear-torso packaging penalty. Do not widen the torso for it unless hands are required.
> - Front electrical bay `100 x 100 x 90 mm`: reserve it only for the 48 V motor switch/precharge/PDU, not Thor or WEHO. One `TE LEV100A5ANG` (CAD reserve `50 x 50 x 60 mm`, 0.190 kg), **one** `Eaton Bussmann 16220-2` (`76.2 x 50.8 x 25.4 mm`, 0.151 kg), `Vishay RHA050100R0FE02` (mounting envelope `70.6 x 21.4 x 16 mm`, 0.050 kg), `CIT A2K1CSQ24VDC1.6` (`26.5 x 32 x 33.5 mm`, 0.040 kg), and the main `Littelfuse BF1 70A + 04980921GXM5 holder` belong there. Exactly **one** Eaton block is needed. Put the five motor-branch fuse holders at cable exits/on a removable rear or underside panel, not all in the 100 mm cube. E-stop is externally accessible.
> - Topology: `battery -> 70A main fuse -> split`; protected **unswitched** branch -> WEHO -> 24 V fuses -> Thor/hub; **switched** branch -> precharge resistor/relay -> LEV100 -> one Eaton block -> motor branch fuses -> harnesses. E-stop interrupts the LEV100 coil independently of Thor; Thor stays live to log the event.
> - New concise build document: `README.md`. `MEMORY.md` remains the agent handoff/source-of-truth.
> - Screw/CAD mass correction: ISO 4762 standard lengths selected: `M3x10` (8 installed), `M3x15` (184), `M4x15` (201), `M4x20` (12); M3x20, M4x10 and M4x25 remain catalogue qty0. Fractional `7.5/12.5/17.5/22.5 mm` lengths are not normal ISO stock and are intentionally not listed. Motor assembly masses, including only the stated screws: RS06 `0.642930 kg`; RS04 `1.452625 kg`; RS03 `0.912625 kg` (uses the 0.880 kg manual base); RS00 `0.323320 kg`; RS05 `0.211620 kg`. Screw purchase rows deliberately have no BOM mass to avoid double counting.
> - Pushrod mass correction: the 40 mm and 140 mm links are no longer identical. Pending a scale measurement of the delivered AliExpress part, BOM CAD body estimates assume a 6061-class aluminium tube OD12/ID8: `6.8 g` for 40 mm and `23.8 g` for 140 mm, each excluding separately listed igubal ends/jam nuts. Replace these values after verifying delivered tube geometry and advertised length definition.

> **MOTOR SPEC TABLES (scannable) = separate file `MOTORI_TABELLE.md`** (Encos planetary+harmonic, RobStride, ZeroErr, CubeMars, Steadywin, Dynamixel, Damiao, sensor options). To be updated together with this memory whenever new specs are found.

> **CURRENT ACTUATOR DECISION 2026-06-20: QDD architecture, RobStride supplier. Unitree G1 is the actual reference; K-Scale K-Bot is observation only.**
> The previous CubeMars choice was based on a dimensional error. `AK70-9` is **Ø89 x 49 mm**, not Ø70; `AKE90-8` is **Ø107.5 x 43.5 mm**, not Ø90. CubeMars therefore has no decisive diameter advantage over RS06/RS04 for this robot. RobStride is retained because dimensions and torque class are comparable, price is lower, and its data are already in the CAD/BOM workflow.
> **BALANCED ACTUATOR MAP LOCKED / CURRENT 2026-06-21 (30 actuators):** `RS04 x6` = hip pitch/roll + knees; `RS03 x3` = hip yaw x2 + waist roll x1; `RS06 x11` = ankle A/B drives x4 + waist yaw x1 + shoulder pitch/roll x4 + elbows x2; `RS00 x8` = shoulder yaw x2 + wrists x6; `RS05 x2` = neck pan/tilt. Waist has roll + yaw and **no waist pitch**; as of 2026-06-27 CAD order is **waist roll below waist yaw**. Sagittal torso motion is produced by hip pitch.
> Selected actuator mass is approximately `20.913 kg`. This is the current RobStride BOM map; do not reintroduce the older `RS06 x13 / RS03 x1` map.
> RobStride and CubeMars are outer-rotor low-reduction QDD actuators. Unitree G1 remains the geometry and power baseline even though its internal motor construction is not being copied literally.
>
> **ELECTRONICS / THOR / IMU UPDATE 2026-07-12 (SUPERSEDES OLDER ELECTRONICS NOTES):**
> - The project is open source and must be reproducible by universities and makers. Prefer exact, orderable components with public dimensions and Linux support; do not require a component merely because another open robot used it.
> - Initial onboard controller is **one NVIDIA Jetson AGX Thor Developer Kit only**. RobStride actuators already contain the FOC driver and local current/position/velocity loops, so there are no 30 external motor drivers and Thor must not recreate the 10-40 kHz FOC loop. Thor runs perception, state estimation, policy and a high-priority `250 Hz` target-refresh process. Use PREEMPT_RT, CPU affinity/priority and SocketCAN. A separate low-level computer remains qty 0 and is added only if measured latency/jitter or USB-CAN reliability fails.
> - Thor developer-kit envelope is `243.19 x 112.40 x 56.88 mm`, about `1.94 kg`; reserve at least `255 x 125 x 72 mm` including cables and airflow. Set a `<=130 W` nvpmodel. Thor is the dominant unavoidable backpack dimension.
> - Five physical RobStride CAN 2.0B buses at `1 Mbps`: Thor native CAN0 = left leg (6), native CAN1 = right leg (6), three exact isolated `MKS CANable Pro` STM32F072/candleLight interfaces = left arm (7), right arm (7), waist+neck (4). Use exactly two `120 ohm` terminations per bus (`10` total), bus topology and short stubs. Do not substitute the unsupported STM32G431 MKS V2.0 silently. At 250 Hz command+feedback the conservative estimated loads are about 45%/45%/53%/53%/30%.
> - RobStride CAN timeout protection is documented but disabled at `CAN_TIMEOUT=0` by default. Set a nonzero timeout on every actuator and bench-test the resulting safe stop; the manual example `20000` corresponds to about `1 s`. A CAN timeout is not a substitute for the hardwired e-stop.
> - **Strict-minimum onboard power architecture, 2026-07-12:** `13S battery -> 70 A BF1 main fuse`; from there the two compact 24 V converter inputs remain available for compute, while the motor path goes through precharge and one exact `TE Connectivity KILOVAC LEV100A5ANG / 9-1618389-8` contactor, then one `Eaton Bussmann 16220-2` block and five branch fuses. The latching e-stop directly interrupts the LEV100 24 V coil independently of Thor. Exact LEV envelope: body Ø39.5 mm, flange width 46.3 mm, height 57.96 mm, mass 0.190 kg.
> - Removed from the active onboard BOM: Albright SW80, ED250 manual disconnect, Mean Well RSD-500C-24, second Eaton block, DIN timer, key selector, Omron hand relay, external 12,000 uF capacitors, and the ODrive Regen Clamp/plate/resistor assembly. The XT90-S battery connector is the physical service disconnect and must only be separated with the robot stopped and LEV100 open. Ground-only equipment includes the RSP-3000 bench supply, battery charger, debug PC and tools.
> - **Power correction 2026-07-12:** use one `Cincon CHB350-48S24`, exact 36-75 V input / 24 V 14.6 A / 350 W half-brick, `61.0 x 57.9 x 13.2 mm`, for Thor, both RH56DFX hands and interfaces. Thor should use its locking Micro-Fit 9-28 V input, not USB-C PD. At 130 W Thor is about 5.4 A on 24 V; the hands document 2 A maximum each. Bench-test Thor transient current and converter temperature. `UHG-PWR-001` is not a purchasable SKU: it is a required **to-design** small carrier PCB, reserve `90 x 85 x 30 mm`, mass budget `0.150 kg`, containing manufacturer-required capacitors/filtering, fuse interfaces, connectors, coil suppression, heat spreading and mechanical support. Do not represent it as purchase-ready until schematic, exact component BOM and thermal/creepage review exist.
> - **Power/packaging alternatives 2026-07-12, not yet final BOM lock:** (A) `MEAN WELL RSD-300C-24`, enclosed 24 V / 12.5 A / 300 W, 33.6-62.4 V input, `216 x 96.5 x 40 mm`, 1.19 kg. No custom PCB, can support Thor plus both RH56DFX hands in normal operation, but requires realistic rear width about 225 mm beside Thor (bare widths 112 + 96.5 = 208.5 mm). (B) compact enclosed `WEHO WH-C482410`, 30-60 V -> 24 V / 10 A / 240 W, `74 x 74 x 32 mm`, about 300 g, claimed sealed/non-isolated. Its stated range covers 13S 42-54.6 V and it is electrically suitable for Thor alone at 130 W plus interfaces; it gives a narrow back module about 200-205 mm wide beside Thor. It is **not** sufficient for Thor at 130 W plus two RH56DFX hands at their documented 2 A maxima: approximately 241 W with interfaces exceeds 240 W. It may work with Thor capped 90-100 W plus hands only after current/thermal/EMI bench validation. WEHO is a manufacturer-direct generic converter, less traceable/confident than Mean Well; treat it as a prototype candidate, not proven infrastructure. (C) Cincon plus custom carrier is compact and has full 350 W margin but needs electrical design. User prefers not to widen torso unless strictly necessary. Current recommended first walking iteration: no hands, WEHO candidate after bench validation; add hands later or move to Cincon/Mean Well choice.
> - Regen hardware is now qty 0 to meet the strict compact baseline, not because regen risk vanished. Before dynamic walking, confirm the battery BMS accepts regenerative charge, avoid full-SOC dynamic tests, and scope the motor bus. Reactivate/resize a clamp only if measurements require it. External bulk capacitors remain measurement-only qty 0.
> - USB compacted 2026-07-12: D436 directly to one Thor USB-A port; exact powered `Waveshare USB3.2-Gen1-HUB-4U`, SKU 27837, on the second USB-A. The hub is only `86.0 x 47.8 x 27.6 mm`, USD 17.99, accepts `7-36 VDC` and serves exactly three USB-CAN adapters + the pelvis IMU. The dual RS485 hand adapter connects directly to a host-capable Thor USB-C through exact `LINDY 36940`, USB-C to USB-B, 0.5 m. This supersedes the `139 x 69 x 25 mm`, EUR 105 DIGITUS seven-port hub. Keep camera bandwidth off the hub. Separate USB/data and CAN harnesses from high-current cables, add grommets, strain relief and service loops.
> - Packaging correction: the proposed internal electronics bay may be `100 x 100 x 90 mm` only if moving neck yaw out of the ribcage creates it. It fits the Cincon carrier, LEV100, precharge parts, one Eaton block and interfaces, but **cannot fit Thor** (`243.19 x 112.40 x 56.88 mm`). Reserve a separate ventilated outer rear shell/backpack for Thor of at least `125 W x 255 H x 75 D mm` if oriented vertically; allow cable and airflow space. CAD must make a component-level layout before declaring fit.
> - **Harness update 2026-07-12:** a new BOM section `5A - MOTOR HARNESS / CAN BUS` contains exact Seeed `BCCA4011 / SKU 100066605` reference lead and explicit qty0 manufacturing deliverables: left/right arm trunk, waist/neck trunk, inline CAN/power branch junction, RS03/RS04 custom harness set, strain-relief/grommet plan and final motor connector/CAN-ID map. Do not guess cut lengths: use CAD centreline length + 10% service slack + connector bend allowance, then freeze a drawing containing every connector/pin/wire gauge/branch/fuse/CAN ID/termination endpoint before buying cut-to-length harnesses. BCCA4011 is a 300 mm 16AWG power + 26AWG signal combined lead and must be physically verified against RobStride connector gender/keying.
> - **Audio selection 2026-07-12:** baseline basic voice I/O is exact `Waveshare USB TO AUDIO / SKU 18833` plus `PUI Audio AS03604AR` bare 36 mm / 4 ohm / 3 W speaker. Waveshare is USB/Linux driver-free, includes basic microphone and a PH2.0 speaker output rated 2.6 W/channel at 4 ohm. It uses Thor USB-C #2 through exact `LINDY 41899` USB-C male to USB-A female adapter; port map remains: USB-A#1 D436, USB-A#2 4-port hub (three CANable + IMU), USB-C#1 dual RS485 hands, USB-C#2 audio, debug USB-C recovery only. Speaker has no mounting holes: `AUD-MNT-01` visible BOM design deliverable specifies a printed pocket/retaining ring/grille, 1 mm diaphragm clearance, shallow rear cavity and strain-relieved wire exit. This baseline does not have far-field mic-array/AEC quality: begin with push-to-talk/half duplex. Possible later upgrade is Seeed ReSpeaker XVF3800 4-mic array (USB/Linux, AEC/beamforming/DoA) after its speaker output path is selected.
> - Selected pelvis IMU is **Phidgets MOT0110_0 PhidgetSpatial Precision 3/3/3**, exact enclosed size `38.989 x 37.846 x 13.380 mm`, CAD mass `0.030 kg`, USB/Linux Phidget22, synchronized timestamps, up to `1 kHz`, accelerometer `+/-16 g`, gyro `+/-2000 deg/s`, magnetometer `+/-8 G`. Exact short cable is `CBL4011_0`, USB-A to right-angle Mini-B, `280 mm`. Mount rigidly on the pelvis below the articulated waist, document axes, and isolate structurally from cable pull. Use gyro+accelerometer for locomotion; magnetic yaw near QDD motors/high-current wiring is untrusted until in-situ calibration. The D436 head IMU is not a pelvis-IMU substitute because the neck moves.
> - Isaac Sim/Isaac Lab work can begin now, but train on a desktop/workstation GPU rather than Thor. Gate before RL: one rigid link per body, correct revolute axes/limits/zero pose, measured masses/inertias, simplified collision meshes, foot friction and selected self-collisions, actuator torque/speed/sign limits, and stable standing PD. The offset ankle gimbal is two serial revolute joints (pitch above roll), not a ball joint. For the first URDF/RL model use virtual ankle pitch/roll joints with the real axis offset; omit the closed pushrod loop from dynamics or keep it visual-only, then apply the measured motor-to-joint differential/Jacobian map and domain randomization later.
> - The BOM “purchased onboard mass” excludes the 4 kg bench supply but conservatively counts full purchased cable lengths. It is therefore not the final CAD mass; replace cable rows with installed lengths after harness routing.
>
> **CAMERA, HANDS AND BATTERY UPDATE 2026-07-11 (AI + user; shared handoff for the other AI session):**
> - Camera selected: `RealSense D436`, SKU `99CWHP`, `90 x 25 x 25 mm`, `75 g`, global-shutter stereo depth + global-shutter RGB + IMU. The official D400 CAD archive does not yet contain D436; use the same-envelope D435i CAD provisionally and verify the physical camera before releasing the bracket.
> - Hands selected: `Inspire RH56DFX-2L` + `RH56DFX-2R`, **without Inspire wrist** because the robot already has RS00 3-axis wrists. Each hand is `540 g`, `217.8 mm` long, about `80.7 mm` palm width, 6 actuators / 12 moving joints, `24 V`, RS485. Cleaned one-file visual meshes for Onshape are `cad_reference/RH56DFX-2L_reference.stl` and `cad_reference/RH56DFX-2R_reference.stl`; they are packaging meshes, not watertight manufacturing solids. Their dedicated `CHB300W-48S24` rail is disabled through hardware remote-on/off during e-stop; no separate Omron relay. Communication remains one isolated two-channel Waveshare USB-RS485 adapter.
> - **Battery superseded again 2026-07-11 after the user rejected the Tattu envelope as too large.** Current CAD/procurement baseline is the commercial Bicycle Motor Works `48 V 9 Ah Molicel P45B` pack: `13S2P`, `46.8 V` nominal / `54.6 V` full, exactly `421.2 Wh` like G1, integrated BMS `45 A continuous / 100 A maximum`, XT90-S discharge, XT60 charge, published `165.1 x 101.6 x 76.2 mm`. Published mass is “under 5 lb”; use conservative `2.27 kg` until the supplier gives the exact finished mass. This is smaller than the G1 battery (`182 x 120 x 80 mm`) in every oriented dimension. CAD reserve `170 x 106 x 81 mm` plus `35-50 mm` cable bend at the connector face. ORDER GATE: confirm Italy lithium shipment, exact mass, duration of the 100 A rating, BMS trip curve, short-circuit current, regen charge-current limit, charger and lead lengths. The original Unitree G1 battery remains unsuitable because its load detection prevents generic standalone power-on. The previous Tattu and 25 Ah ENERprof selections are superseded.
> - EU fallback: Tõuksi Vabrik in Estonia publishes the same `13S2P / P45B / 9 Ah / 421.2 Wh` architecture with a `60 A BMS`, `2.04 kg` and EUR 416 VAT included. It is qty 0 until they provide a drawing and guarantee a finished envelope no larger than about `165 x 102 x 76 mm`; use it if Bicycle Motor Works cannot legally ship to Italy.
> - Secondary EU softpack fallback is Dan-Tech `13S2P 48 V 10 Ah 60 A`, `280 x 35 x 130 mm`, `2.2 kg`, EUR 347 VAT included. It remains qty 0 because it is longer than desired and its page contradicts itself: the selected configuration says `No BMS`, while the feature list claims full BMS/CAN/RS485/UART protection.
> **2026-06-21 — CubeMars 36:1 (AK45-36, Ø55x54, 24/8 Nm) EVALUATED and REJECTED. STAY ALL-QDD, no high-reduction anywhere.** User's 3 questions settled it: (1) QDD is more FUTUREPROOF — 36:1 permanently closes force/impedance control + compliance + impact tolerance on that joint (hardware life sentence, not sw-upgradeable). (2) 36:1 is WORST on the ANKLE (contact joint, wants compliance most) -> keep ankle QDD. (3) On the arms 36:1 helps only today's position-based ACT/diffusion, but kills future contact-rich/compliant manipulation. User values futureproofing -> all-QDD. Chunky Ø88 arms/ankle = cosmetic + ~2.5 kg, does NOT cap capability; 36:1 does. RobStride QDD map (earlier AI lock) STANDS; CubeMars-QDD AKE90 only if stronger legs wanted (170 vs 120 Nm, same Ø). The AI over-sold AK45-36 the prior turn; user correctly pushed back.
> **2026-06-21 — REAL PROJECTED MASS ≈ 45 kg, HEIGHT ≈ 1.40 m (user's numbers, agreed). SIZE AGAINST THESE, not the old 35 kg / 1.2 m.** Why heavier than G1's 35 kg: RobStride ≈ 84 Nm/kg (RS04) vs Unitree custom ≈ 189 Nm/kg, so ~2× actuator mass per Nm. 20.35 kg motors + structure + on-board battery + push-rod/shaft/bearing hardware -> 40–45 kg; budget the top. Height rises to ~1.40 m partly from the 2× Ø88 ankle stack lengthening the shin.
> **TORQUE re-scaled (first-pass rules of thumb, ±25%, NO CAD mass model yet — re-validate after CAD):** 35->45 kg (×1.29) and 1.2->1.4 m (longer levers, ×~1.17) push proximal-joint torque ~1.3–1.5× above the old estimates. Binding joints @45 kg/1.4 m (hold/peak Nm vs motor rated/peak):
>   - Ankle pitch: ~40 / **~67** push-off vs RS06 11/36 -> **needs ~1.9:1 push-rod leverage** (was 1.45). MANDATORY. Less leverage = flat-foot ZMP only, no energetic toe-off.
>   - Ankle roll: ~20 / ~24 vs RS06 11/36 -> OK; **RS02 (17) now too small, do NOT shrink ankle roll.**
>   - Knee: ~43 / ~53 vs RS04 40/120 -> peak fine; **continuous ~43 ≈ rated 40** -> marginal for SUSTAINED deep-knee holds.
>   - Hip roll: ~41 / ~50 vs RS04 40/120 -> peak fine; **continuous ~41 ≈ rated 40** -> marginal for PROLONGED single-leg stance.
>   - Hip pitch: ~35 / ~78 vs RS04 40/120 -> OK. Shoulder pitch/roll: sustained arm+payload-out ~22 Nm > RS06 rated 11 -> go **RS03** only if sustained extended-load holds are required; else RS06 ok for motion.
> **CONSEQUENCE: RS04 legs are now RIGHT-sized, NOT oversized — RETRACT the earlier "shrink legs to RS03" idea; keep RS04.** Only safe shrink left = **wrists RS00 -> RS05** (~0.7 kg). Robot WALKS fine: walking single-support is brief/dynamic, lives in PEAK numbers (RS04 120 ≫ 78); only SUSTAINED static high-torque poses (long single-leg, deep squat, payload at arm's length) are thermally marginal.
> **Roll < Pitch at the ankle CONFIRMED (physics):** pitch CoP travels the foot LENGTH (half ~0.10 m) + has push-off (1.5 Nm/kg); roll CoP travels the foot WIDTH (half ~0.045 m, ~2.2× shorter lever) and has NO sideways push-off. Heavy lateral balance in single-support is the HIP roll (RS04), not the ankle. -> in the 2-push-rod ankle the PITCH rod can carry MORE leverage than the ROLL rod (need not be symmetric even with 2× RS06).
> **ANKLE ARCH (corrected by user 2026-06-21): DIFFERENTIAL / parallel, NOT serial.** 2 push-rods from 2 shin motors to the SAME shaft on the foot: both push/pull = PITCH, opposed = ROLL (sum=pitch, diff=roll). Both motors drive BOTH DOFs. Map = clean sum/diff mix (m1 = pitch/2k + roll/2k', m2 = pitch/2k - roll/2k') + geometric corrections; RL trains in (pitch,roll), the map converts at deploy. **BONUS: pitch = SUM of both motors -> up to ~72 Nm (2× RS06) -> covers the 45 kg push-off (~67 Nm) with NO leverage; flat-foot now, push-off-capable later.** Diamond torque envelope (can't max pitch+roll simultaneously; fine in practice). Body weight rides a CENTRAL 2-DOF pivot; rods carry only torque. (The AI's earlier serial/"triangular" description was WRONG.)
> **2026-06-21 — HIP YAW upgraded RS06 -> RS03 (user).** Reason: at 45 kg projected mass the aggressive-turn peak (~36 Nm) sat exactly at RS06's 36 Nm limit; RS03 = 60 Nm peak gives headroom for snappy turns (gravity-free axis, so only peak matters). **NEW LOCKED MAP (30): RS04 x6** (hip pitch/roll + knees) | **RS03 x3** (waist roll x1 + hip yaw x2) | **RS06 x11** (ankle pitch/roll x4, waist yaw x1, shoulder pitch/roll x4, elbows x2) | **RS00 x8** (shoulder yaw x2 + wrists x6) | **RS05 x2** (neck). New actuator mass ≈ **20.913 kg** (+0.558 vs 20.355). RS03 body drawing from the RobStride 2025-06-26 PDF is OD 98 x length 54.1 mm; RS04 is OD 120 x length 56 mm; RS06 OD 88 x 49 mm; RS00 OD 57 x 51 mm; RS05 OD 46 x 44 mm. BOM Excel re-synced 2026-06-27.
>
> **ROBSTRIDE vs CUBEMARS CONTENDERS BY TORQUE CLASS (2026-06-23, comparison only, NOT a BOM switch).** `Height`
> means actuator axial thickness. Use real outer actuator dimensions, not model names (`AK70` is not Ø70; `AKE90` is
> not Ø90). CubeMars `AKE` motors may require external driver packaging; RobStride modules are integrated.
>
> | Torque class / project use | RobStride contender | RobStride dimensions / mass / torque | CubeMars contender | CubeMars dimensions / mass / torque | Verdict |
> |---|---|---|---|---|---|
> | ~5 Nm, neck | `RS05` | Ø46 x 44 mm, 191 g, 5.5 peak / 1.6 rated Nm | `AK40-10` | Ø53 x 37 mm, 185 g, 4.1 peak / 1.3 rated Nm | Keep `RS05`: smaller diameter and stronger; CubeMars only thinner. |
> | ~10-15 Nm, wrists + shoulder yaw | `RS00` | Ø57 x 51 mm, 310 g, 14 peak / 5 rated Nm | `AKE60-8` or `AK45-10` | `AKE60-8`: Ø69 x 25 mm, 260 g, 12.5 / 5 Nm. `AK45-10`: Ø53 x 43 mm, 260 g, 7 / 2.5 Nm | `RS00` remains simplest and smaller than AKE in diameter. `AKE60-8` is attractive only if axial thickness is the binding CAD problem; `AK45-10` is too weak for the same class. |
> | ~25-36 Nm, ankles + shoulder pitch/roll + elbows | `RS06` | Ø88 x 49 mm, 621 g, 36 peak / 11 rated Nm | `AK70-9 V3.0` or `AKE80-8` | `AK70-9`: Ø89 x 49 mm, 540 g, 29.2 / 8.5 Nm. `AKE80-8`: Ø87 x 32 mm, 570 g, 30 / 12 Nm | No strong CubeMars win. `AK70-9` is same size but weaker; `AKE80-8` is thinner but external-driver and still weaker peak. |
> | ~50-60 Nm, hip yaw + waist roll | `RS03` | Ø98 x 54.1 mm body, 900 g, 60 peak / 20 rated Nm | `AK10-9 V3.0` | Ø98 x 61.7 mm, 940 g, 53 peak / 18 rated Nm | `RS03` wins on same diameter, lower mass, shorter length and more torque. |
> | ~120-170 Nm, hip pitch/roll + knee | `RS04` | Ø106 face / about Ø120 envelope x about 56 mm, 1420 g, 120 peak / 40 rated Nm | `AKE90-8` | Ø107.5 x 43.5 mm, 1400 g, 170 peak / 55 rated Nm | Only serious CubeMars upgrade: same weight/diameter class, thinner and much stronger. Tradeoff = external driver + mixed software/spares. |
>
> Ranking summary: diameter smallest->largest = `RS05` 46 < `AK40/AK45` 53 < `RS00` 57 < `AKE60` 69 < `AK60-6` 79
> < `AKE80` 87 < `RS06` 88 < `AK70-9` 89 < `RS03/AK10/AK80` 98 < `RS04/AKE90` ~106-120. Weight smallest->largest =
> `AK40` 185g ~= `RS05` 191g < `AK45/AKE60` 260g < `RS00` 310g < `AK60-6` 380g < `AK80-9` 490g < `AK70-9`
> 540g < `AKE80` 570g < `RS06` 621g < `RS03` 900g < `AK10` 940g < `AKE90` 1400g ~= `RS04` 1420g.

> **SPECIFIC-TORQUE AUDIT 2026-06-20.** Formula: `specific torque [Nm/kg] = output torque [Nm] / complete actuator mass [kg]`. The stated major-joint target `>10 Nm/kg` normally uses peak torque. Rated values are also recorded as a conservative thermal check. Source: official RobStride Product Specification 2025-06-26.
>
> | Model | Peak / rated Nm | Mass kg | Peak Nm/kg | Rated Nm/kg | Result |
> |---|---:|---:|---:|---:|---|
> | RS04 | 120 / 40 | 1.420 | 84.5 | 28.2 | PASS peak and rated |
> | RS03 | 60 / 20 | 0.900 | 66.7 | 22.2 | PASS peak and rated; reserve, not selected |
> | RS06 | 36 / 11 | 0.621 | 58.0 | 17.7 | PASS peak and rated |
> | RS00 | 14 / 5 | 0.310 | 45.2 | 16.1 | PASS peak and rated |
> | RS05 | 5.5 / 1.6 | 0.191 | 28.8 | 8.4 | PASS peak; FAIL rated, neck only and not a major load-bearing joint |
>
> All selected models meet the quoted target on the usual peak basis. RS05 must not be promoted to a continuous major-joint role based on this metric.
>
> **Torque rationale for balanced substitutions:** hip yaw and waist yaw remain RS06 because gravity torque is approximately zero and the estimated aggressive dynamic demand near G1 mass is about `28 Nm < 36 Nm peak`; this becomes borderline if the finished robot approaches `46 kg`. Waist roll remains RS03 because an estimated `12-17 Nm` continuous demand at 30 degrees fits its `20 Nm rated`, while RS06 has only `11 Nm rated`. Shoulder yaw uses RS00: at the approximately `0.24 m` G1 shoulder-yaw-to-palm lever it supplies about `21 N/hand` rated and `58 N/hand` peak, sufficient for roughly a 1 kg box with friction and safety margin. Elbows stay RS06 because RS00 would be near rated torque with a 1 kg payload.
>
> **ACTUATOR-MODEL AUDIT 2026-06-21, against MIT Humanoid paper `sources/2104.09025v1.pdf`:** the MIT flips/spins are strictly simulation results, but the actuator hardware tests are real. MIT used a custom dynamometer with a FUTEK TRS300 torque sensor to measure current-vs-output-torque and the 60 V torque-speed envelope; an impedance analyzer for resistance/inductance; measured battery impedance for voltage sag; and included output/rotor inertia plus estimated friction and damping in simulation. RobStride's local manuals/specification provide mass, ratio, rated/peak torque, current limits, scalar torque constant, back-EMF, line resistance, scalar inductance, 48 V torque-speed plots, overload-duration plots, temperature limits, dual encoders, FOC/MIT/current modes and CAN telemetry. They do **not** provide output/reflected rotor inertia, friction/stiction maps, damping, backlash/compliance/gear efficiency, current-loop bandwidth, guaranteed command-to-torque latency, a full thermal RC model, battery/bus sag, or raw numerical curve data. Active reporting is documented down to 10 ms (100 Hz), but this is not a guaranteed internal-control or request-response bandwidth.
> Documentation inconsistencies must be bench-resolved: RS03 mass is `880 g +/-20 g` in its later user manual but `900 g +/-20 g` in the 2025-06-26 family specification; RS00 rated speed is `260 rpm` in its later manual but `100 rpm` in the family specification. RS04 has no separate local user manual, only the family sheet.
> **Required test level:** calm first walking can begin with conservative datasheet limits plus domain randomization; do not wait for an MIT-grade dynamometer. Before serious sim-to-real tuning, identify one sample per load-bearing model in priority order `RS04 -> RS06 -> RS03`: output torque versus reported `Iq` in both directions, breakaway/Coulomb/viscous friction versus speed and temperature, command/feedback latency and frequency response, effective output inertia, thermal derating, and bus-voltage sag. RS00/RS05 can be characterized later. Full high-speed torque-speed dynamometer testing is required only before acrobatics or planning close to actuator limits. Never assume the plotted datasheet curves constitute a complete validated actuator model.
>
> **ACTUATOR-ARCHITECTURE CHECK AGAINST FIRGELLI GUIDE 2026-06-20.** The guide does not invalidate QDD for this project: it explicitly places Unitree G1/H1 in the QDD class and reserves harmonic + planetary-roller-screw systems mainly for high-payload continuous-duty factory humanoids. Important correction to its loose wording: a planetary roller screw is resistant to impact because line contact distributes Hertzian stress; it is still a rigid, high-reduction transmission and does not inherently absorb impact energy. True passive absorption requires a separate compliant element, for example a Series Elastic Actuator spring. High-reduction harmonic actuators normally need an output torque sensor for accurate force control; this is commonly a strain-gauged flexure. A linear screw actuator analogously uses an axial force sensor/load cell, commonly strain gauges, or an SEA spring measured by encoders. These sensors are optional for position control but required for accurate output-force control when current estimation is corrupted by friction.

> **ANKLE - CURRENT CAD DIRECTION (updated 2026-06-27, SUPERSEDES the Ø12 note of 2026-06-21):**
> The user has designed a 3D-printed gimbal/Cardan solution with two 45 mm pins one above the other in Z. It is not a
> mathematical single-center Cardan joint: it is an offset gimbal. Higher pin = pitch; slightly lower pin = roll. Current
> BOM/CAD direction: use shoulder screws `Ø8 mm` with `M6` thread both for the two axes of the ankle gimbal and for the pivots
> of the pushrod rod-ends. The previous
> direction "ankle axes Ø12/M10 and pushrod pins Ø12" is superseded for the ankle; it remains only in the history. Also the
> old Ø12/M10 idle pin of the waist roll is now deactivated qty0: there are no active Ø12/M10 items in the current CAD/BOM.
>
> Hardware selected in BOM 2026-06-27:
> - First-choice shoulder screw listing: `https://it.aliexpress.com/item/1005007885495357.html`.
> - Old shoulder screw listing kept only as second source / backup: `https://it.aliexpress.com/item/1005007481484485.html`.
> - Offset-gimbal ankle axes: `2 x` shoulder screws `Ø8 x M6 x 45 mm`; upper-Z pin = pitch, lower-Z pin = roll.
> - Pushrod rod-end pivots: `4 x` shoulder screws `Ø8 x M6 x 16 mm`.
> - Retaining nuts: `6 x` M6 nuts/locknuts for the shoulder screws only; nut must clamp the shoulder stack, not crush the
>   spherical bearing. Geometry noted in BOM: M6 hex AF 10 mm, circumscribed diameter about 11.55 mm, normal locknut
>   height about 6 mm.
> - Pushrods: AliExpress adjustable aluminum M8 rods from `https://it.aliexpress.com/item/1005008935554718.html`,
>   active variants `2 x 140 mm` and `2 x 40 mm`. CAD must confirm whether advertised length is body length or eye-to-eye.
> - Pushrod rod ends: `2 x` igus `KARM-08 CL / KARM_08_CL_1` right-hand male M8 + `2 x` igus `KALM-08 CL` left-hand
>   male M8. This is for turnbuckle adjustment: rotating the aluminum rod body changes length only with RH/LH threads.
>   Availability of KALM-08 CL must be confirmed before ordering.
> - Pushrod length locknuts: `2 x` DIN 439 M8 right-hand thin jam nuts + `2 x` DIN 439 M8 left-hand thin jam nuts.
>   Standard geometry in BOM: height 4.0 mm, across flats 13 mm, circumscribed hex diameter about 15.0 mm. These are M8,
>   not M6, because they lock on the rod-end external thread.
>
> GIMBAL / CARDAN MODEL: use the real Z offset between pitch and roll pins in CAD/simulation. Do not use an ideal
> intersecting-axis Cardan map unless a later CAD revision makes the axes intersect. The offset does not add a DoF, but
> it moves the foot center slightly during combined pitch/roll and changes the motor-to-pitch/roll geometry. The current
> BOM quantities above are the user's literal current prototype quantities, not an automatically doubled full-robot estimate;
> revisit after left/right CAD is frozen.
>
> ANKLE MOTORS: `RS06 x2` per leg are still the active actuator choice. Physical ankle motors are A/B differential
> drives through pushrods, not direct pitch/roll labels. Virtual pitch/roll comes from the linkage map. Keep the two
> RS06 close to the knee/proximal shin when possible; verify collisions, cable exits, crank geometry and conditioning of
> the motor-to-pitch/roll matrix in CAD.
>
> ROD-ENDS: the M8 rod ends run on Ø8 shoulders. Perfect perpendicularity of the threaded heads is not required because
> the spherical joints compensate, but the actual misalignment angle must stay inside the joint limit across the full
> ankle workspace and must not contact screws, foot or tibia. Active BOM rod ends are `2 x` igus `KARM-08 CL /
> KARM_08_CL_1` right-hand male M8 plus `2 x` igus `KALM-08 CL` left-hand male M8, both with Ø8 E10 ball bore and target
> ±35 deg pivot. KARM mass is 6.2 g each; KALM assumed same until supplier data is confirmed. Price is still `0` in the
> sheet until the exact igus cart/quote is confirmed.

> **KEY CLARIFICATION 2026-06-20 (correction of an over-emphasis by the AI): WALKING WITH RL DOES NOT REQUIRE TORQUE SENSORS.** RL policies (Unitree, ToddlerBot, etc.) take joint positions/velocities + IMU as input (NOT torques), output POSITION targets, tracked by a joint-level PD, with torque applied OPEN-LOOP from the current. No torque sensor, on ANY motor. ToddlerBot does it with Dynamixel 288:1 (stiffer than the Encos) and walks + manipulates. **So Encos WITHOUT sensors = valid robot** (position control + Isaac Lab RL, already in the user's plan); the high reduction is in fact GOOD for position control (stiff/precise, the friction is absorbed by the policy with domain randomization). Torque sensors are needed ONLY for FORCE/IMPEDANCE control, contact-rich tasks, force-safety — NOT for walking. -> Encos-vs-RobStride is NOT "sensor yes/no" (both zero sensors for RL), but **compact-stiff (Encos, ASIMO/ToddlerBot class) vs bulky-compliant (RobStride QDD, Unitree class)**. Scale caveat: ToddlerBot 3.4 kg (forgives everything), us ~20 kg (feasible, ASIMO at ~50 kg, but keep it light/slow/cautious gait). The whole sensor-dressing/UKF/Bota saga = NOT necessary for the goal "walks calmly + basic tasks".

## Collaboration rule between AI sessions

Two AI sessions take turns following this project, whenever one of the two runs out of its available context.
This file is the single source of truth for the handover: update it at the end of the session with decisions, changes,
sources and open doubts. Do not recreate a second status file. The next agent must read everything, verify the sources
and criticize the weak technical choices before adding components or ordering material.

Mandatory mechanical rule: do not turn a hypothesis into a BOM choice. If CAD, loads, seats, thicknesses, tolerances
or retention system are not known, leave the row `DA DIMENSIONARE qty0`, list the missing data and ask for confirmation
from the user before proposing SKUs, quantities or geometries. Do not infer construction details from partial images.

Workspace:

```text
/Users/artes/Documents/artes/umanoide
```

Updated deliverable:

```text
BOM umanoide G1 - RobStride.xlsx
```

Verified BOM totals, VAT included. WARNING 2026-07-19: the totals are now the REMAINING SPEND
(Thor + both RH56DFX hands are ALREADY OWNED in the lab and counted at EUR 0 with the reference price
in the notes; the PHASES have been REDEFINED on the real build order):

| Scope | Total (to be spent) |
|---|---:|
| Complete humanoid (remaining) | EUR 10.264,90 |
| Phase 1 - arm+hand teleop bench | EUR 4.008,57 |
| Phase 2 - legs and locomotion | EUR 3.997,95 |
| Phase 3 - completion (left arm, waist, neck, mobile) | EUR 2.258,38 |

(Excel totals recalculated and verified 2026-07-17 after the reactivation of the hands on the WEHO rail, the new rows
SEQ-PWR-01/TVS 33CA/capacitor/XT90 and the phase corrections; the active WEHO row has price 0 pending a quotation.
The previous totals 31.243,22 / 35,043 kg were the 2026-07-12 midday snapshot with hands qty1, never realigned
after the evening qty0.
WARNING: the purchased mass excludes the PA-CF frame; with about 10 kg of frame the finished robot can exceed
45 kg. At that mass the ankles, knee/hip roll in continuous duty and waist roll must be re-evaluated after the real CAD/mass budget.)

Estimated purchased on-board mass: `33,233 kg`, excluding the printed PA-CF frame. Of this, the selected actuators alone
weigh about `20,913 kg`. The mass is conservative because it counts the full purchased lengths of the power cables; replace
with the lengths actually installed after the routing. The full 50 m spool of CAN cable and the bench items
are not counted as on-board mass.

Generator:

```text
python3 build_umanoide_tab.py
```

The generator now creates a blank workbook with only the `umanoide` sheet; it no longer copies the historical Excel file in `~/Downloads`
and no longer generates the sheets `G1 joints CAD`, `MOTORI premium`, `MOTORI Encos (quote)` or `MOTORI RobStride`. Local backup
from before the cleanup: `BOM umanoide G1 - RobStride.backup-before-single-sheet-20260623.xlsx`.
Update 2026-06-26: the row style is now driven only by the `Unita` column: `0` = automatic gray, quantity
other than zero = black. Even rows labeled `[SCELTO qty0]` stay gray until they are actually given a quantity.
Update 2026-06-27: workbook `BOM umanoide G1 - RobStride.xlsx` translated into English in the active view; column
`Uniqueness` removed; headers now `Item/Supplier/Unit cost/...`; Excel filter on `Qty != 0` (`A1:T164`) and rows with
`Qty=0` hidden automatically on opening. The links on `Qty=0` rows do not stay blue: the whole row is gray if
it is unhidden. Further update 2026-06-27: ankle rod-ends now `2 x KARM-08 CL` right-hand + `2 x KALM-08 CL`
left-hand, plus `4 x` thin DIN 439 M8 jam nuts to lock the adjustment; the `6002-2RS` waist-roll bearing and the related `Ø12/M10` idle-side pin have been
deactivated qty `0` because they belonged to the old idle support of the waist and are not needed in the current CAD. The historical
qty0 rows may still contain mixed IT/EN notes, but the filtered active view is in English.

## Objective

Build a humanoid that is printable in PA-CF as far as possible, with architecture, geometries and power ratings taken from the reference
Unitree G1. Unitree G1 is the only baseline of the project. K-Scale K-Bot is not a dimensional or kinematic reference:
it may be consulted only as a secondary open hardware example for packaging, manufacturability and practical
wiring problems. Do not invent dynamic simulations: they are not available. Before the purchases, CAD and geometric checks
on the real components are needed.

## Official Unitree G1 baseline

Use the updated G1 model `g1_29dof_mode_11`, not the old `g1_29dof` marked deprecated.

Official sources:

- Repository and README: <https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description>
- Current URDF: <https://github.com/unitreerobotics/unitree_ros/blob/master/robots/g1_description/g1_29dof_mode_11.urdf>
- Meshes: <https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description/meshes>
- G1 product page: <https://www.unitree.com/g1/>
- Official G1-Comp page with 2 DOF head: <https://www.unitree.com/robocup/>
- Official G1-EDU Waist Fastener manual: <https://marketing.unitree.com/article/en/G1/Lumbar_fasteners.html>

`effort` limits of the current official model:

| Axis | Nm |
|---|---:|
| Hip pitch / roll | 139 |
| Hip yaw | 88 |
| Knee | 139 |
| Ankle pitch / roll | 35 |
| Waist yaw | 88 |
| Waist roll / pitch | 35 |
| Shoulder pitch / roll / yaw | 25 |
| Elbow | 25 |
| Wrist roll | 25 |
| Wrist pitch / yaw | 5 |

The URDF provides joint origins, limits and external meshes. For the ankle it describes the two virtual kinematic axes pitch
and roll, but it does not expose the internal CAD of the linkage. Do not treat the virtual values as a trivial sum of the torques of the
two parallel motors.

The same applies to the waist: the virtual kinematic chain `yaw -> roll -> pitch` of the URDF does not prove that the three
physical actuators are mounted in series. The current CAD choice of this project is different from the old pushrod
scheme: direct serial waist with `roll` below `yaw`, no waist pitch and no waist pushrod. The torso pitch comes
from the hip pitch joints.

The `g1_29dof_mode_11` model does not include the neck. The official G1-Comp page instead states `Head 2 degrees of
freedom = 2`, but does not publish the torque of the two motors. The neck of this project therefore uses two RS05 as a compact
provisional choice, not as a Unitree-certified torque equivalence.

### Exact G1 joint positions and CAD (extracted 2026-06-04)

Extracted from the official URDF `g1_29dof_mode_11.urdf` (downloaded and saved in the project). Files in the workspace:
`g1_29dof_mode_11.urdf` and `g1_joints.csv` (relative parent-child offsets + rpy + absolute positions + axes + limits).
Convention: X forward, Y left, Z up; origin = pelvis; mm. 29 DOF; the neck (2 DOF) is NOT in the model, it must be added
separately. Use these to draw the Onshape skeleton: one mate connector per joint, name = G1 name.

Absolute positions (pelvis frame, mm) - left side; right side mirrored in Y:

| Joint | x | y | z | axis | limits rad |
|---|--:|--:|--:|---|---|
| hip_pitch | 0 | 64.4 | -102.7 | Y | -2.53..2.88 |
| hip_roll | 0 | 116.5 | -133.2 | 0.98,0,0.17 canted | -0.52..2.97 |
| hip_yaw | 46.2 | 116.5 | -251.0 | -0.17,0,0.98 canted | -2.76..2.76 |
| knee | 0 | 118.6 | -439.3 | Y | -0.09..2.88 |
| ankle_pitch | 0 | 118.5 | -739.3 | Y | -0.87..0.52 |
| ankle_roll | 0 | 118.5 | -756.9 | X | -0.26..0.26 |
| waist_yaw | 0 | 0 | 0 | Z | -2.62..2.62 |
| waist_roll | -4 | 0 | 44 | X | -0.52..0.52 |
| waist_pitch | -4 | 0 | 44 | Y | -0.52..0.52 |
| shoulder_pitch | 0 | 100.2 | 291.8 | 0,0.96,0.28 canted | -3.09..2.67 |
| shoulder_roll | 0 | 140.6 | 289.0 | X | -1.59..2.25 |
| shoulder_yaw | 0 | 146.8 | 185.8 | Z | -2.62..2.62 |
| elbow | 15.8 | 146.8 | 105.2 | Y | -1.05..2.09 |
| wrist_roll | 115.8 | 148.7 | 95.2 | X | -1.97..1.97 |
| wrist_pitch | 153.8 | 148.7 | 95.2 | Y | -1.61..1.61 |
| wrist_yaw | 199.8 | 148.7 | 95.2 | Z | -1.61..1.61 |

Notes: hips and shoulders have CANTED axes (not orthogonal); ankle pitch/roll 17.6 mm apart in Z (it is the cardan joint of the 2 Ø12 pins);
waist roll and pitch coincident. Joint torques (URDF effort, Nm): hip pitch/roll 139, hip yaw 88, knee 139, ankle 35,
waist yaw 88, waist roll/pitch 35, shoulder 25, elbow 25, wrist roll 25, wrist pitch/yaw 5. Total G1 mass (sum of the URDF
links) 33.3 kg.

**z offset hip pitch->roll (G1: ~30 mm, the line connecting them inclined ~30 degrees downward according to the user's
calculation).** It is NOT dead length: it is a real trade-off.
- The pitch torque = m*g*D*sin(theta), with D = depth of the leg CoM below the pitch axis. The offset is part of D:
  as soon as the pitch rotates, the block below the roll acquires an X coordinate = offset*sin(theta) that it would not have with the axes aligned
  (user correction: the AI's "x=0 so it does not count" held only at theta=0, a pose in which the torque is zero regardless).
- Aligning pitch/roll in z -> leg CoM 30 mm higher -> -2.1 Nm of peak = ~10% less pitch torque
  (leg ~7.3 kg, CoM ~305 mm below the pitch). Real but modest (the dominant lever arm is the leg length).
- BUT aligning brings the housings closer together: in adduction the YAW motor hits the PITCH at a roll angle that is much
  smaller -> ROM in adduction is lost. With the RobStride motors (housings BIGGER than the Unitree actuators) the problem
  gets worse. So keeping the G1 stagger (or a touch more) is probably right: the ~10% of pitch torque is a
  low price for the roll ROM + no collision.
- TO BE DECIDED in CAD with the real envelopes of the three motors (pitch+roll+yaw): find the minimum offset that avoids the
  collision at the maximum required adduction; that also fixes the pitch torque. (Exact positions: the user will provide them.)

### Onshape skeleton: simplified CAD coordinates

CAD decision 2026-06-05, corrected after user review: the `G1 joints CAD` sheet keeps the exact G1 coordinates and
adds simplified CAD columns to draw the skeleton in Onshape without useless geometric noise.

- `exact_x/y/z`: absolute G1 URDF coordinates;
- `cad_x/y/z`: primary CAD coordinates; `-` means equal to the respective `exact_*` coordinate, not zero;
- `pose_down_x/y/z`: auxiliary column only, to visualize the arms along the body; `-` means equal to the primary
  CAD pose `cad_*`.

Primary CAD rule:

- `X`: set to `0` when the URDF has forward/backward shifts that disturb the skeleton;
- `Y`: in the vertical columns it is aligned to the first upper joint of the chain. Leg: from `hip_roll` to `ankle_roll`
  use the `Y` of `hip_roll`. Arm: from `shoulder_yaw` to `wrist_yaw` use the `Y` of `shoulder_yaw`;
- `Z`: remains the exact G1 height in the primary table. Do not lower `hip_yaw` and do not redistribute its `X` onto the `Z`;
- `axis_preciso`: it is not simplified. The canted axes remain annotated as URDF data.

Primary CAD coordinates left side, pelvis frame, mm. The right side is mirrored in `Y`.

| Joint | x CAD | y CAD left | z CAD | Note |
|---|--:|--:|--:|---|
| hip_pitch | 0.0 | 64.5 | -102.7 | X=0 only |
| hip_roll | 0.0 | 116.5 | -133.2 | X=0 only |
| hip_yaw | 0.0 | 116.5 | -251.0 | exact_x 46.2 -> 0 |
| knee | 0.0 | 116.5 | -439.3 | Y aligned to hip_roll |
| ankle_pitch | 0.0 | 116.5 | -739.3 | Y aligned to hip_roll |
| ankle_roll | 0.0 | 116.5 | -756.9 | Y aligned to hip_roll |
| waist_yaw | 0.0 | 0.0 | 0.0 | X=0 only |
| waist_roll | 0.0 | 0.0 | 44.0 | exact_x -4 -> 0 |
| waist_pitch | 0.0 | 0.0 | 44.0 | exact_x -4 -> 0 |
| shoulder_pitch | 0.0 | 100.2 | 291.8 | X=0 only |
| shoulder_roll | 0.0 | 140.6 | 289.0 | X=0 only |
| shoulder_yaw | 0.0 | 146.8 | 185.8 | X=0 only |
| elbow | 0.0 | 146.8 | 105.2 | Y aligned to shoulder_yaw |
| wrist_roll | 0.0 | 146.8 | 95.2 | Y aligned to shoulder_yaw |
| wrist_pitch | 0.0 | 146.8 | 95.2 | Y aligned to shoulder_yaw |
| wrist_yaw | 0.0 | 146.8 | 95.2 | Y aligned to shoulder_yaw |

To draw or visually check the arms hanging along the body, use only the auxiliary `pose_down_*` columns.
In those columns the elbow and wrist are computed by converting the relative `X/Z` length of the URDF pose into a `Z` drop.
This is not the primary joint table and must not be used as new G1 kinematics.

Physical meaning of the points: they are origins of the URDF joint frames, hence kinematic centers of the rotation axes. In
Onshape treat them as the mate connector of the joint: the point crossed by the `axis_preciso` axis. They are not automatically
the center of the motor cylinder and they are not automatically the center of the outer face of the cylinder. For a coaxial
motor, the motor cylinder must be positioned relative to this mate connector with the real offset between the output plane/flange,
the motor body and the geometric center of the cylinder. For the pushrod-driven ankle and waist, these points are virtual G1 joints and not
positions of the physical motors.

RobStride motor CAD: STEP downloadable from the Seeed pages (in the BOM in the "Purchase link" column and now also "CAD 3D").
Direct STEP source per model: AIFITLAB `aifitlab.com/products/robstride-0X-motor` (STEP + installation drawing with the
bolt pattern). Alternatives: robstride.com download center, GrabCAD (RS06).

## K-Scale K-Bot: secondary note, not a baseline

Sources:

- Mechanics and public CAD: <https://docs.kscale.dev/robots/k-bot/mechanical/>
- Motor mapping: <https://docs.kscale.dev/robots/k-bot/motor-id-mapping>
- Repository: <https://github.com/kscalelabs/kbot>

Do not copy K-Bot geometries, motors or kinematics into the baseline. Its ankle is different; our project instead replicates
the G1 concept with two actuators in the calf and two pushrods to obtain pitch and roll. K-Bot remains useful only for
observing construction solutions and as a reminder that dynamic wiring requires careful design. Its
documentation is under development: do not use it to size components.

## Motor decision: RobStride only

Damiao and CubeMars have been removed from the selected BOM. The single ecosystem reduces firmware, debug tools, spare parts
and wiring variants. The BOM contains only the relevant RobStride alternatives.

### Legs, phase 1

| Position | Motor | Quantity | Peak | Dimensions | Note |
|---|---|---:|---:|---|---|
| Hip pitch / roll + knee | RS04 | 6 | 120 Nm | 120 x 120 x 56 mm | maximum available from RobStride |
| Hip yaw | RS06 | 2 | 36 Nm | 88 x 88 x 49 mm | vertical axis: gravity 0, ~28 Nm in an aggressive turn at G1 mass; borderline if the robot reaches 46 kg |
| Pushrod ankle, one motor per axis | RS06 | 4 | 36 Nm peak | 88 x 88 x 49 mm | matches the 35 Nm of the G1 per axis at peak; minimum linkage ratio 1:1, preferably 1.3-1.6:1 if the robot becomes heavy |
| Lightened ankle alternative | RS00 with ~2:1 reduction | qty 0 | 14 Nm peak | 57 x 57 x 51 mm | saves 1.244 kg but reduces speed and margin; not selected |

Known limitation: the RS04 remains 13.7% below the 139 Nm of the G1 on hip pitch, hip roll and knee. Copying exactly the
G1 power is not possible while staying within the current RobStride range. The trade-off is explicit, it must not be hidden.

Torque density issue (analysis 2026-06-04, raised by the user): the G1 gets ~120 Nm in a Unitree actuator of
~80 mm (user's mesh measurement); RobStride for ~120 Nm requires the RS04 of ~110-120 mm. So it is NOT possible to respect together
the G1 joint positions (designed for ~80 mm motors) and the G1 torque. Raw reference: the hip_pitch link of the G1 weighs
1.35 kg (motor+structure), as much as just ONE RS04 (1.4 kg) -> with RS04 the legs become heavier than the G1. And there is no
intermediate RobStride: between RS03 (60 Nm peak, 106 mm) and RS04 (120 Nm peak, ~110 mm) there is nothing, and RS03 is only slightly
smaller (downgrading to RS03 saves mass, not diameter). Real options for the legs: (a) keep RS04 -> torque close
to the G1 but bigger/heavier legs, hip geometry to be readapted (the exact G1 joints do not fit); (b) RS06 ~88 mm -> close
to the G1 geometry but only ~36 Nm peak, a quarter of the G1, suitable only for a lighter/less dynamic robot. The choice depends
on the ambition (G1-style dynamic locomotion vs walking + RL on flat ground): 139/120 Nm are needed for dynamic motion, for
slow walking the requirement is lower. Do NOT change the leg motors in the BOM until the user decides the ambition.

The ankle keeps the requested architecture: two actuators in the calf, two adjustable pushrods and a two-axis
joint between foot and shin. They are distinct subsystems:

- The four M8 ankle pushrods remain selected: two per leg. They push on a transverse pin fixed to the foot.
- The transverse pin of the pushrods has a diameter of 8 mm, consistent with the bores of the M8 rod ends. Length, material,
  tolerance, lateral distance between the balls and retention remain to be defined in the CAD.
- The foot-shin joint allows pitch and roll and carries the structural loads of the foot. It uses two orthogonal pins of
  12 mm diameter per ankle: they serve only as rotation axes of the joint and do not receive the pushrods. Length,
  material, tolerances, retainers, type and quantity of the supports remain to be defined in the CAD.
- The two M10 waist pushrods remain selected: the robot total is therefore six pushrods, four M8 at the ankles and two
  M10 at the waist.

Geometry clarified by the user for both 12 mm diameter axes: the two outer lugs are fixed relative to the pin;
the central part of the ankle rotates on the pin. Do not automatically put radial supports both in the center and in the
lugs: it would be redundant and would risk misalignments. The lugs must carry and retain the fixed pin; the
moving central part contains the radial support.

FINAL DECISION for the ankle (2026-06-03) - flanged igus plain bearing, axial in the flange. It applies to each of the two
12 mm diameter axes. It is the solution chosen as the simplest and it replaces the hypotheses NKI / sleeve-column / separate
thrust washers described below, now archived as alternatives.

- Pin = ISO 7379 shoulder screw `Ø12 / M10`. It acts as the pin, as the race on which the igus slides and as the retainer. It is fixed
  to the lugs by the AXIAL CLAMPING (shoulder on one side, M10 self-locking nut + Loctite 243 on the thread on the other),
  not by a heavy press fit. Shank-to-lug-bore fit: sliding-locked (snug), just enough to remove the radial
  play and avoid fretting; no heavy interference in the printed PA-CF (it cracks the layers and is hard to assemble on two coaxial
  bores). Almost no torque reaches the pin because the moving part turns on the low-friction igus: the clamping
  is enough to hold it still. Clean variant: thread the far end into a metal insert/nut embedded in the lug,
  so the clamping reacts on metal. Extra anti-rotation (flat on the shank) only if needed.
- Support = igus flanged bushing in the moving part. PRIMARY chosen by the user: multi-material J260+PA-CF PRINTED bushing
  integral with the moving part in FDM (J260 both on the bore and on the flange faces; filament already purchased). FALLBACK
  that can be purchased if the print does not hold up: `GFM-1214` iglidur G (drop-in `Q2FM-1214` for shocks/dirt or
  `JFM-1214` low friction) PRESS-fitted into the moving central part, flanges facing outward. The bushing carries the
  RADIAL load; the FLANGE carries the AXIAL load, one per direction. So no separate thrust washers, no thrust bearing, no
  sleeve/column. Bushing retention: interference in the seat + stop flange. On printed PA-CF the bore is not
  precise: print, test the fit, adjust the Ø in CAD; backup `Loctite 603/638` (anaerobic retaining compound for
  fits). Never cyanoacrylate (Attak): brittle and wrong for retaining bushings.
- Clamping = M10 self-locking nut DIN 985 + wide washer DIN 9021.
- Counterface on which the flange slides = OPTIONAL. STARTING POINT chosen by the user: PA-CF shoulder formed from the lugs toward the inside, on which the
  printed igus flange slides (contact PA-CF against igus, not PA-CF against PA-CF over the whole face, concentrated on the flange
  ring). Alternatively the flange slides directly on the PA-CF face
  of the lug (estimated axial ~1.3 MPa, slow oscillation, ok for a prototype, validate wear on the test specimen). Upgrade if
  the PA-CF wears: a METAL flanged bush press-fitted into each lug (`DIN 172-B12-20` or
  similar), fixed by interference like the igus (no glue), its flange is the metal counterface and the bore
  guides and protects the pin. Do NOT use a loose washer in a pocket: it does not stay fixed to the lug, it spins and ends up
  sliding on PA-CF on one face anyway.
- Load checks: radial ~8 MPa, axial ~1.3 MPa on the igus, against the iglidur G limit `>60 MPa`, margins ~10x and ~45x.
  The type of support is not driven by the load (negligible) but by simplicity and by the oscillation: needle roller bearings risk
  false brinelling under oscillating motion, the plain bearing does not.
- Quantities: 2 pins per ankle x 2 ankles = 4 axes. Per axis: 1 shoulder screw, 2 igus flanged bushings, 1 nut +
  1 wide washer, plus (optional) 2 metal flanged bushes.
- Left to the CAD: length of the two bushings = real thickness of the moving part (e.g. two of 9 mm in 20 mm); shoulder
  length = real fork stack (~60-70 mm); axial play 0.1-0.3 mm (bushings + moving part a touch narrower than the gap
  between the lugs).

Suppliers verified 2026-06-03 (several choices, common stuff):

| Part | SKU / family | Suppliers |
|---|---|---|
| igus flanged bushing | `GFM-1214` iglidur G, Ø12/Ø14, flange ~Ø20x1, L from CAD ~9-10 | igus direct, RS, Misumi, Minetti, F.lli Bono, Solema, ERIKS |
| Shoulder screw | ISO 7379 `Ø12-M10`, shoulder L from CAD | RS PRO `292-417` (12x60), Rubix `GN.35185`, Elesa, Puntoviti, Berardi, KIPP |
| Metal flanged bush (optional) | `DIN 172-B12-20` | Verzolla `Y1137`, Best4Automation, KIPP `K1022.A1200X20` |
| Nut + washer | M10 DIN 985 self-locking + DIN 9021 | everywhere |
[ARCHIVED ALTERNATIVE - superseded by the ankle FINAL DECISION above; kept only as a needle-roller option in case one day
it is needed] First simple architecture to draw in CAD, requested by the user:

- outer PA-CF lug about `20 mm`;
- moving central part about `20 mm`, with SKF `NKI 12/16` `16 mm` wide in its own seat;
- second outer PA-CF lug about `20 mm`;
- preliminary structural stack about `60 mm`, excluding small amounts of play and retention details.

With `NKI 12/16` the separable inner ring must be clamped between the integrated shoulders of the two PA-CF lugs and stays fixed
together with the pin; the outer ring stays in the seat of the moving central part. The running play must be left between
the lugs and the moving central part, not between the shoulders and the inner ring. The shoulders must not squeeze the
moving part. Verify in CAD the abutment area, PA-CF creep and clamping: if the local pressure is excessive, insert
metal load-spreading spacers or switch to the flanged metal inserts documented below.

Caution: `NKI 12/16` carries the radial load but does not replace a thrust bearing. If the moving central part ends up touching
the lugs axially under load, provide a pocket for a thin, located igus thrust washer or a separate thrust bearing.
Do not leave PA-CF against PA-CF as a wear surface.

Preliminary clamping of the axle with `NKI 12/16`: do not use the bolt to bend the lugs inward until
a dimensional error is taken up. The fixed chain must already be closed at the nominal dimension; fine corrections are made
with shims selected after the test of the first prototype. Sequence from the outside to the outside: head of the shoulder
bolt and large washer, PA-CF lug, annular shoulder integrated in the lug, `NKI` inner ring, second
integrated annular shoulder, second PA-CF lug, large washer and self-locking nut. The moving central body and
the outer ring of the bearing must stay excluded from the clamped chain and keep a small controlled axial play
relative to the lugs. The thread must not work in the shear zone or in the bearing raceway. Use large washers
to spread the load on the PA-CF; tightening torque and creep must be verified on the real test specimen. If the local pressure is
excessive, add metal load-spreading spacers or switch to the variant with DIN 172 bushes.

Preliminary references to be confirmed against the final dimension of the stack:

| Component | Useful dimensions | Link |
|---|---|---|
| RS PRO `292-417`, ISO 7379 shoulder bolt | plain shoulder `12 x 60 mm`, thread `M10 x 16 mm`, total length `84 mm` | <https://it.rs-online.com/web/p/viti-a-colletto/0292417> |
| RS PRO `797-6254`, DIN 9021 large washer | hole `10,5 mm`, outer diameter `30 mm`, thickness `2,5 mm` | <https://it.rs-online.com/web/p/rondelle/7976254> |

The `60 mm` plain shoulder is consistent with the preliminary structural stack `20 + 20 + 20 mm`, but the final dimension
depends on the real play, shims and seats.

Do not yet definitively select bearings, bushings or needle rollers for the ankle joint: first CAD, loads,
seats, thicknesses and tolerances are needed. The earlier hypotheses `6001-2RS` and `6801-2RS` were removed from the BOM because premature.
If mechanical data are missing, ask the user for confirmation instead of proposing a solution as if it were already defined.

First alternative to evaluate for the two 12 mm diameter axles: long plain bushings, not necessarily rolling
bearings. The ankle joint performs limited, oscillating rotations, with shocks and low speeds: a plain bushing,
metal/PTFE composite or heavy-duty polymer, can turn out simpler, more compact and more tolerant than needle rollers.
To separate the tasks correctly:

- the cylindrical bushing in the moving central part carries the radial load;
- one dedicated plain thrust washer per side carries the axial load and must be located, not left free between two faces;
- a fixed flanged metal insert in each lug, similar to a top-hat bushing, contains or guides the
  12 mm diameter pin and gives the igus thrust washer a smooth, replaceable axial counterface;
- any DIN 988 shims only correct the residual play after assembly: they are not the primary wear surface.

Do not let igus work directly against the PA-CF of the lug and do not use the printed PA-CF directly as
a sliding surface. Do not leave a washer free to rotate randomly against both faces. The thrust washer can
be located in a shallow pocket of the moving part; the metal insert is instead rigidly fixed to the lug.

The top-hat metal inserts are no longer the first architecture to draw, but remain a standard alternative that is easy
to buy if a printed central igus bushing is used or if the PA-CF shoulders are not enough. The real size
identified is Elesa+Ganter `DIN 172-B12-20-A` / `GN.12825`: bore `12 mm F7`, outside `18 mm n6`, flange diameter `22 mm`,
body `20 mm` long, flange `4 mm` thick. A top hat must be used on both lugs. The bore guides the pin but does not
automatically lock it in rotation: design anti-rotation and axial retention. If the structural reference
`20 + 20 + 20 = about 60 mm` is kept, recess the `4 mm` flange into the lug; otherwise the two flanges add to the envelope.

Suppliers verified on 2026-06-02 for standard top hats, 12 mm bore, 20 mm length:

| Supplier | SKU | Price | Declared availability | Link |
|---|---|---:|---|---|
| Verzolla Italia | Elesa+Ganter `DIN172-B12-20-A`, code `Y1137` | EUR 6.89 each | 5 available | <https://www.verzolla.com/elesa-bussola-di-guida-flangiata-din172-b12-20-a-y1137> |
| Best4Automation | Otto Ganter `172-B12-20-A` | EUR 5.26 net each | ships in 2-3 working days, B2B | <https://www.best4automation.com/positionierbuchse-mit-bund-bohrung-eins.-gerundet-sc-4042-172-b12-20-a/> |
| Normteile Leinigen | KIPP `K1022.A1200X20`, DIN 172 form A equivalent | EUR 4.50 net / EUR 5.36 VAT included each | available, 2-5 days | <https://www.normteile-leinigen.de/Bundbohrbuchse-12-x-20-DIN-172-Form-A/K1022.A1200X20> |
| TME | Elesa+Ganter `DIN172-B12-20-A` | USD 10.04 each | zero stock: use as datasheet or backup request | <https://www.tme.eu/en/details/din172-b12-20-a/indexing-plungers/elesa-ganter/din-172-b12-20-a/> |

Official Elesa+Ganter datasheet: <https://www.elesa.com/siteassets/PDF/PDF_IT/DIN%20172.pdf>.

Useful catalogues for ankle pins and retainers, kept in the BOM at zero quantity to verify what really exists before
closing the CAD dimensions:

| Family | Reference | Link |
|---|---|---|
| Assorted shoulder screws | legacy AliExpress set `M3-M10` | <https://it.aliexpress.com/item/1005007481484485.html> |
| Short shoulder bolt | RS PRO `822-9316`, `12 x 20 mm`, thread `M10` | <https://it.rs-online.com/web/p/viti-a-colletto/8229316> |
| Full-axle shoulder bolt | RS PRO `292-417`, `12 x 60 mm`, thread `M10 x 16 mm` | <https://it.rs-online.com/web/p/viti-a-colletto/0292417> |
| Ground shaft to be cut | Motedis `12 mm h6`, hardened and ground | <https://www.motedis.it/it/Albero-di-precisione-12-mm-h6-acciaio-temprato-e-rettificato> |
| Short cylindrical dowel pin | Wurth DIN 6325 / ISO 8734 `12 x 20 mm` | <https://eshop.wurth.fr/Goupille-cylindrique-DIN-6325-acier-brut-GOUPILLE-CYL-DIN6325-M6-12X20/025201220.sku/fr/FR/EUR/> |
| Elastic retainers | assortment of internal and external Seeger rings | <https://www.amazon.it/ANELLI-ELASTICI-INTERNI-ESTERNI-ASSORTITI/dp/B09CZKWD5J> |
| Split collar for `12 mm` axle | Ruland `MSP-12-F` | <https://www.ruland.com/msp-12-f.html> |
| Ground shaft to be cut for pushrod pin | Motedis `8 mm h6`, hardened and ground | <https://www.motedis.it/it/Albero-di-precisione-8-mm-h6-acciaio-temprato-e-rettificato> |
| Split collar for `8 mm` axle | Ruland `MSP-8-F` | <https://www.ruland.com/msp-8-f.html> |

If instead a radial needle roller bearing is evaluated:

- SKF `HK 1216.2RS` is compact but has no inner ring: it requires a hardened and ground pin raceway;
- SKF `NKI 12/16` includes the inner ring: the fixed shoulders of the lugs can clamp that ring while
  the outer ring stays in the seat of the moving central part;
- a radial needle roller bearing does not automatically replace the axial stop: for the axial load a
  dedicated sliding interface or a separate thrust bearing is still needed. Do not clamp the moving central part between the shoulders.

Do not yet choose SKU or length `20-25 mm`: what is needed is maximum radial load, axial load, angle and frequency of
oscillation, maximum outer diameter of the seat, pin material, surface finish, tolerances and axial space.

Real examples added to the BOM as `qty 0` alternatives, not yet selected:

| SKU | Type | Dimensions | Price verified 2026-06-02 | Note |
|---|---|---|---:|---|
| SKF `PCM 121420 E` | metal/PTFE | 12 x 14 x 20 mm | EUR 2.13 net | first simple candidate |
| SKF `PCM 121425 E` | metal/PTFE | 12 x 14 x 25 mm | EUR 2.94 net | shows that 25 mm is a standard length |
| igus `Q2SM-1214-20` | heavy-duty polymer | 12 x 14 x 20 mm | about EUR 6.15 net | candidate for oscillation, shocks and dirt |
| igus `Q2FM-1214-12` | flanged heavy-duty polymer | 12 x 14 x 12 mm, flange 20 x 1 mm | to be verified | only if the CAD allows the flange |
| igus `GTM-1224-015` | separate plain thrust washer | 12 x 24 x 1.5 mm | EUR 1.49 VAT included | one per side, to be located, not free |
| SKF `HK 1216.2RS` | radial needle roller without inner ring | 12 x 18 x 16 mm | quotation | requires hardened pin raceway |
| SKF `NKI 12/16` | radial needle roller with inner ring | 12 x 24 x 16 mm | EUR 22.15 net | consistent with fixed shoulders, but does not carry the axial load by itself |
| SKF `AXK 1226` + `AS 1226` | needle roller thrust bearing with raceways | 12 x 26 x 4 mm per side | EUR 4.10 + 2 x EUR 1.86 net | bulkier alternative to the igus thrust washer |
| HGI `PS12X18X1` DIN 988 | adjustment shim | 12 x 18 x 1 mm | EUR 0.48 net | only final correction of the play |
| Elesa+Ganter `DIN 172-B12-20-A` / `GN.12825` | alternative fixed flanged metal insert | 12 x 18 x 20 mm, flange 22 x 4 mm | EUR 6.89 each Verzolla | standard top hat for both lugs if the igus route is chosen |

The user is buying three printable igus tribofilaments to run comparative tests: `iglidur i150`, `iglidur i190`
and `iglidur J260-PF`. Three separate `[ALT CUSTOM qty0]` rows were added. Custom bushings can be useful
for quickly iterating length, flange and play, but they are not yet a sized choice nor a replacement
automatically equivalent to the SKF metal/PTFE or igus `Q2` injection-moulded bushings. Print comparable test specimens
and validate surface pressure, wear, print orientation, pin finish, tolerances and play. `i150` is the
easiest to process; `i190` favours strength and wear and is sensitive to humidity; `J260-PF` is more demanding to print
but must be compared for friction, wear and temperature.

### Upper body, phase 3

The waist keeps the requested physical architecture: a vertical yaw motor below that rotates the whole torso, then a central
cardan joint and two actuators connected to two pushrods to produce pitch and roll. The yaw motor is bigger; the two pushrod
motors are smaller but must not be sized by automatically assuming half the load each.

| Position | Motor | Quantity | Dimensions | Weight | RobStride torque | G1 reference |
|---|---|---:|---|---:|---|---|
| Waist yaw | RS06 (downgraded from RS03) | 1 | 88 x 88 x 49 mm | 0.621 kg | 11 rated / 36 peak | 88 Nm; check ~28 Nm aggressive torsion < 36 |
| Waist pitch / roll via 2 pushrods | RS06 (downgraded from RS03) | 2 | 88 x 88 x 49 mm | 0.621 kg | 11 rated / 36 peak | 35 Nm/axis; joint ~18-37, shared by the 2 pushrods |
| Proximal shoulder pitch / roll | RS00 (downgraded from RS02, 2026-06-16) | 4 | 57 x 57 x 51 mm | 0.310 kg | 5 rated / 14 peak | 25 Nm; dynamic ~12 < 14; horizontal hold 6.8 not continuous (already so with RS02). -95 g and Ø57 vs 78.5. Dual encoder. RS06 alt qty0 |
| Distal shoulder yaw | RS00 (downgraded from RS02) | 2 | 57 x 57 x 51 mm | 0.310 kg | 5 rated / 14 peak | 25 Nm; gravity 0, ~4-6 Nm. dual encoder |
| Elbow | RS00 (downgraded from RS02, 2026-06-16) | 2 | 57 x 57 x 51 mm | 0.310 kg | 5 rated / 14 peak | 25 Nm; ~6.9 with 2 kg -> ~1.2 kg continuous / 2 kg peak. -95 g, Ø57. Dual enc. RS06 if 2 kg continuous is needed |
| Uniform wrist roll + pitch/yaw | RS00 | 6 | 57 x 57 x 51 mm | 0.310 kg | 5 rated / 14 peak | roll 25 / pitch-yaw 5; holds 2 kg in the hand, dual encoder |
| Neck pan / tilt G1-Comp | RS05 | 2 | 46 x 46 x 44 mm | 0.191 kg | 1.6 rated / 5.5 peak | torque not published |

Reserves qty0: shoulder pitch/roll RS06; shoulder yaw RS02; wrist RS02 (robust) + RS05 (ultralight pitch/yaw); ankle RS03.

**RS01 TRAP (verified 2026-06-08).** RS01 and RS02 have the SAME torque (6/17 Nm) but RS01 has **only 1 encoder
(motor side)**, RS02 has **2 (motor + output)**. The output encoder reads the true joint angle after the gearbox
(compensates the backlash) -> needed for RL and manipulation. RS01 is the cut-down version: 36V only, no IP, -$15 and -5.5mm.
So on the controlled joints (shoulder, elbow) **RS02** is kept, NOT RS01. RS00 (wrist, shoulder yaw) has dual encoder.
**RS01 not used.** RS00 verified dual encoder, 5 rated / 14 peak, 57x57x51, 0.310 kg, ~$125.

**Arm check (real G1 positions, wrist lightened to RS00).** Holding the arm extended horizontally = **6.8 Nm
static**, dynamic peak ~12 Nm < 17. The ELBOW motor with the arm straight accounts for 1.14 Nm (lever X = 187 mm with the arm extended,
not the 16 mm at rest). RS02 covers it: the hold with the arm horizontal is an occasional pose (not continuous), dynamic 12 < 17.
Elbow with payload at 90 degrees: ~4.7 Nm with 1 kg, ~6.9 with 2 kg -> RS02 holds ~1.5 kg continuous / 2 kg peak; RS06 reserve.

**Ankle + waist pitch/roll = LINKAGES, not direct drive (user correction 2026-06-08).** The torque at the JOINT is fixed
by the load (ankle ~46 Nm = weight x toe lever 130 mm); the MOTOR torque = joint x (crank_motor / crank_foot). The
pushrods push ~40 mm from the pin: pushing close to the pin does NOT reduce the motor torque (it raises the force in the rod ~1150 N);
what reduces it is the motor crank being shorter than the foot crank (reduction), which costs joint speed. FINAL CHOICE
(2026-06-16, see session bullet item e): walking only -> ankle = 2x RS00 at ~2:1 reduction (BOM). At 1:1 it would take
2x RS06 (alt qty0, for dynamic gaits); the RS02 is eliminated. Exact cranks (per axis) TO BE SET in CAD with the 2x2 Jacobian.

The G1 EDU body remains a 29 DOF baseline. Adding the selected G1-Comp neck, the project rises to 31 motorized
axes, excluding any hand motors. The G1-Comp neck torque is not public: RS05 `5.5 Nm picco / 1.6 Nm
nominali` is a provisional choice based on compactness and mass. The wrist is all RS00 (dual encoder, 57 mm, 5 rated /
14 peak): it holds 2 kg in the hand and halves the size vs RS02. Reserves qty0: RS02 (robust) and RS05 (ultralight pitch/yaw).

## Motor brand comparison at equal torque (size, weight, cost) - 2026-06-14

Comparison requested by the user: at EQUAL TORQUE what counts first is size+weight, then cost, then availability.
Specs verified via web (Seeed, CubeMars, ROBOTIS emanual, Foxtech). Dynamixel added to the comparison.

**CLASS ~36 Nm - ankle (4) + hip yaw (2) + waist pushrods (3) = 9 motors. HERE is where the weight saving is.**

| Brand / model | Peak Nm | Size mm | Weight | Nm/kg | Type + encoder | Cost each | Availability |
|---|---:|---|---:|---:|---|---|---|
| RobStride RS06 | 36 | Ø88 x 49 | 621 g | 58 | QDD, dual enc | ~200 EUR | good (Seeed, AliExpress) |
| **Encos EC-A4310-P2-36** | 36 | Ø56 x 60.5 | **382 g** | 94 | QDD 36:1, dual enc | ~700 USD | **poor (Foxtech only, on quotation)** |
| CubeMars AK10-9 v3 | ~48-53 | Ø98 x 62 | 940 g | ~53 | QDD, dual enc | ~700 USD | excellent (T-Motor) |
| Dynamixel PH42-020-S300 | ~25 (max) | 42 x 84 x 42 | 340 g | ~74 | cycloidal >300:1, NOT backdrivable | ~900-1100 USD | excellent (ROBOTIS) |

**CLASS ~120-170 Nm - legs: hip pitch/roll + knee = 6 motors. CubeMars here is CAPACITY, not weight.**

| Brand / model | Peak Nm | Size mm | Weight | Nm/kg | Type + encoder | Cost each | Availability |
|---|---:|---|---:|---:|---|---|---|
| RobStride RS04 | 120 | Ø106 x 56 | 1420 g | 85 | QDD, dual enc, INTEGRATED | **~255 USD** | good (8+ resellers) |
| **CubeMars AKE90-8** | **170** | Ø107.5 x **43.5** | 1400 g | 121 | planet. 9 arcmin, dual enc, BARE (+driver) | ~484 USD + driver | excellent (T-Motor) |
| Encos A10020 | 150 | not published | 1350 g | 111 | QDD | ~2250 USD | poor (Foxtech) |
| Dynamixel PH54-200-S500 | 44 (rated) | 54 x 126 x 54 | 855 g | 52 | cycloidal ~500:1, NOT backdriv. | **3541 USD** | excellent (ROBOTIS) |

(Dynamixel PH54 = flagship and does NOT reach the leg torque: 44 Nm vs 120-170 required. Out of the running for the legs.)

**CLASS <=17 Nm - shoulders/elbow/wrist/neck. RobStride unbeatable, no premium.**

| RobStride RS00 | 14 | Ø57 | 310 g | 45 | QDD dual enc | ~116 EUR | good |
| RobStride RS02 | 17 | Ø78.5 x 45.5 | 405 g | 42 | QDD dual enc | ~135 EUR | good |
| RobStride RS05 | 5.5 | compact | 191 g | 29 | QDD | ~100 EUR | good |

(Below ~20 Nm no premium beats RobStride on weight+cost+integration. RS00 310 g is lighter than any alternative at that size.)

**WHERE we really save, in plain terms:**
- **Weight = ONLY Encos on the 36 Nm**: -244 g x 9 motors = **-2.2 kg**, and all DISTAL (ankle/leg) -> gold for the walking dynamics. Cost: ~700 USD vs ~200 EUR each (~3.5x) and very poor availability.
- **CubeMars AKE90-8 on the legs = NOT weight** (1.40 vs 1.42 kg, the same): it is +50 Nm (exceeds the G1, removes the 0.86x of the RS04) and **13 mm thinner** (43.5 vs 56) -> better hip packaging. Cost ~2x and "bare" (driver+encoder separate).
- **Small ones (<=17 Nm)**: no gain, RobStride stays.

**AVAILABILITY worldwide (order):** Dynamixel (ROBOTIS, global distributors) > CubeMars/T-Motor (worldwide retail) > RobStride (Seeed + 8 resellers, AliExpress, growing) > **Encos (Foxtech, on quotation only, does not even publish the dimensions)**. So YES: RobStride is MUCH easier to source than Encos.

**Dynamixel = WRONG CLASS for us.** They are POSITION servos with a high-ratio cycloidal gearbox (300-500:1): dense torque but NOT backdrivable, slow (29-33 rpm), low backlash but poor force/impedance control, and very expensive (PH54 = 3541 USD, 14x an RS04). Excellent for slow position-controlled arms, UNSUITABLE for a G1 clone with RL locomotion and force-controlled manipulation, which wants backdrivable QDDs (RobStride/Encos/CubeMars). Top availability, but irrelevant if the category is wrong. (NB: the ToddlerBot paper - Stanford - uses precisely Dynamixels and is in fact small/slow/position-servo, confirmation of the category.)

**NB "T-Motor" = CubeMars.** Same company (Sanrui Intelligent): CubeMars is the robotics sister brand of T-Motor, and the AK series manuals are hosted on store.tmotor.com. The AK10-9 / AKE90-8 already in the table ARE the "T-Motor" ones: there is no separate T-Motor option to evaluate. The other T-Motor lines (U/Antigravity) are RC/drone motors, not robotic actuators.

## Due diligence on premium motors / suppliers + ASIMOV reference (2026-06-16)

Market research for a "light + elegant + powerful + force control humanoid", after the WALL POWER decision
(tethered, battery on the ground for the peaks, NO on-board battery -> robot ~28-30 kg -> legs and ankles require
less torque). Direction: SMALL and DENSE motors everywhere, all CAN + dual-encoder + TORQUE control (homogeneous for RL).

**REFERENCE = ASIMOV v1 (our open-source twin).** 1.2 m, 35 kg, 25 DOF, **parallel RSU ankle identical
to ours**, **ENCOS motors everywhere**, complete public mechanical+electrical CAD + BOM. Actuators ~$7.000 for 25
(~$280 average). The exact ENCOS MODELS for each joint are in their Tally BOM (link from docs.menlo.ai/asimov/v1/bom);
CAD on github.com/asimovinc/asimov-1 (file mechanical/FABRICATION_MANIFEST.csv + sim model). TO BE COPIED joint-by-joint.
Confirmation: Encos is on ASIMOV (not X-Humanoids, the user had corrected himself). Asimov compute = Raspberry Pi 5 + Radxa CM5.

**ENCOS (the lightest at 36 Nm: A4310 377 g).** Available from: Foxtech (store.foxtech.com) + aifitlab.com +
arcsecondrobo.net (all Chinese resellers). International shipping declared, Italy TO BE CONFIRMED (the user
sent an inquiry to Foxtech on 2026-06-16: ask for shipped-to-Italy price + STEP CAD files + lead times/customs). Reliability:
validated by Asimov; independent failure data scarce. WEAK POINT = documentation: NO public CAD/dimensions ->
CAD to be REQUESTED from Foxtech or measure a sample. Lineup (module Ø): A2806 (12 Nm, Ø44, 162 g) / A4310 (36 Nm, Ø56, 382 g) /
A4315 (75 Nm, Ø56, 485 g) / A6416 (120 Nm, Ø88, 805 g) / A8112 (Ø81) / A10020 (Ø100) / A13715-720 (Ø137).
CORRECTION 2026-06-19 (datasheet V3.15): the A2806 Ø44 exists -> Encos DOES HAVE a wrist option (the old "nothing below Ø60" is refuted).

**STEADYWIN (micro, cheap, MIT protocol).** Available from: steadywin-motor.com, OpenELAB, Alibaba, aifitlab (niche but ok).
Driver: integrated CAN/UART, **open-source MIT protocol** (Mini-Cheetah standard, community code) or SHS; can also be driven
with Arduino+MCP2515. 2D+3D CAD + manuals at steadywin-motor.com/products/document-download. ROS2 tested (Ubuntu/
Iron, Linux ONLY). **IDEAL WRIST = GIM3510-64: Ø35 mm, reduction 64:1, dual encoder, FOC** = micro + lots of torque +
slow (exactly the wrist requirement). Niche but integrable, no serious red flag.

**MYACTUATOR (the best SUPPORTED).** Mature ROS2 (github 2b-t/myactuator_rmd_ros) + C++17 SocketCAN SDK + Python +
official CAD; Amazon/RobotShop/Dings (USA/EU). Dual encoder. BUT the small RMD-L are weak DIRECT-DRIVE units (5015=0.7 Nm,
9015=3.4 Nm); for torque you need the planetary RMD-X (a bit larger). It wins on support, not on minimum size.

**SURVEY "the best per category" (small+powerful+force control):**
- LEGS 120-170 Nm: physics = ~Ø100 minimum, it does NOT get any smaller. Encos A10020 (Ø100, 150) or **CubeMars AKE90-8**
  (Ø107, 170, 9 arcmin, $484, CAD ready). With the tether the RS04 (120) also comes in handy again.
- MID 36 Nm (hip-yaw, waist, shoulder p/r, ankle): **Encos A4310** (Ø60, 377 g) = the lightest; alt CubeMars
  AK10-9 (Ø98, 940 g) / Steadywin GIM8108-36.
- WRIST/small force-control: **Steadywin GIM3510-64** (Ø35, 64:1) or MyActuator RMD-X (top CAD/ROS) or **Harmonic Drive
  RH-mini** (premium, zero backlash, €€€). Dynamixel REJECTED (position servo, no force control).

**Key TENSION:** the best in weight/size (Encos A4310, Steadywin micro) are NICHE (China, poor support/CAD);
the best supported (MyActuator, CubeMars) are a bit larger/more expensive but with CAD+drivers ready. Asimov proves that
the niche route (Encos + MIT protocol) can really be built.

**CAD/manuals:** CubeMars (product page) / Steadywin (document-download) / MyActuator (myactuator.com/dowload +
ROS driver) have public CAD. Encos does NOT -> request from Foxtech. Entire Asimov: github.com/asimovinc/asimov-1.

**SEQUENCE:** 1) copy the models from Asimov's Tally BOM; 2) wait for the Foxtech quote (Italy price + CAD + lead times);
3) if Encos ok -> Encos (legs A10020 + mid A4310) + Steadywin GIM3510-64 at the wrists; 4) if not -> fallback CubeMars +
Steadywin (CAD ready). Main track for the wrist = Steadywin GIM3510-64. The current RobStride BOM remains intact as baseline.

**Complete ASIMOV MOTOR MAP (reconstructed 2026-06-16: v0 legs BOM CERTAIN + matching `armature` in the v1 sim model
sim-model/xmls/asimov.xml -> joints with the same armature = same actuator). Encos naming = EC-A[Ø frame][h]-[P plan /
H harmonic][reduction]:**
- Hip pitch: **EC-A6416-P2-25** (Ø64, planetary) | Hip roll: **EC-A5013-H17-100** (Ø50, HARMONIC 100:1) |
  Hip yaw: **EC-A3814-H14-107** (Ø38, HARMONIC 107:1) | Knee: **EC-A4315-P2-36** (Ø43) |
  Ankle A+B (parallel RSU pitch+roll): **EC-A4310-P2-36** (Ø43, 377 g) x2  [all CERTAIN from the v0 BOM]
- CONFIRMED by the Asimov Excel BOM ("Asimov 1 BOM.xlsx" in the folder, the qty add up: A4310x10, A6416x3, A5013x4, A4315x4,
  A3814x4 = 25): Waist yaw = A6416 (Ø64) | Shoulder pitch = A5013-H harmonic (Ø50) | Shoulder roll = A4315 (Ø43) |
  Shoulder yaw = A3814-H harmonic (Ø38) | **Elbow + Wrist yaw + Neck = EC-A4310 (Ø43)** [same as the ankle, qty 10 =
  ankle4+elbow2+wrist2+neck2]. So Asimov uses ONLY 5 MODELS, 4 frame sizes (Ø38/43/50/64); the A4310 Ø43 does the bulk of the work.
- Real SUPPLIER: **ENCOS = Nanjing Inks Intelligent Technology (Nanjing)**, resold by Foxtech/aifitlab. Asimov BOM
  ~$15k target, "shipment in a few months". **STEP CAD of the entire robot: mechanical/ASV1/ASIMOV_V1.STEP** + STL meshes per
  joint in sim-model/assets/meshes -> CAD base. Tally BOM: tally.so/r/jaG0va.
- IMPORTANT: hip pitch/knee/ankle = PLANETARY (backdrivable enough for walking); ONLY hip/shoulder roll-yaw =
  harmonic. So the legs are NOT stiff-harmonic (the AI's earlier error, corrected). For WALKING the planetary
  25-36:1 is enough; the QDD 9:1 (RobStride) is only needed for running/jumping, which we do not need.

**OUR ALL-ENCOS LIST = 3 MODELS (user choice 2026-06-19, FINALIZED; 3rd Excel sheet "MOTORI Encos (quote)"; 30 in the robot + 4 trial = 34 purchased):**
- **EC-A6416-P2-25 (legs) x6: hip pitch x2 + hip roll x2 + knee x2.** (Ø88, 805 g, 120 Nm peak)
- **EC-A4315-P2-36 (mid) x16: ankle x4 + shoulders x6 + elbow x2 + hip yaw x2 + waist x2.** (Ø56, 485 g, 75 Nm peak)
- **EC-A2806-P2-36 (wrist+neck) x8: wrist 3 DOF x2 + neck x2.** (Ø44, 162 g, 12 Nm peak, 220 RPM) <- NECK moved here (75 Nm useless up high, lightens the head).
- **EC-A4310-P2-36 (trial) x4: bought to TRY OUT the ankles** (slow planetary OK: the robot does NOT have to run). Ankle baseline remains A4315.
- A4315 = the only mid size (Ø56). Ankle = FIGURE hybrid (pitch via PROXIMAL pushrod in the shin + direct roll at the foot, A4315 kept on purpose). Waist = yaw+roll.

**OPTION REOPENED 2026-06-20 by the user: RobStride LIGHT, NO SENSORS (pure Unitree route).** RS06 (Ø88, 36/11 Nm) on hip/knee/shoulder; RS00 (Ø57, 14/5 Nm) on the rest INCLUDING the ankle; RS05 neck. **NO torque sensors, not even at the foot** (= QDD 9:1, current=torque, like the Unitree G1 which walks/runs without a torque-sensor or foot F/T). This single choice CANCELS the whole instrumentation/UKF/foot sensors problem.
- SOLVES 2 long-standing problems at once: (1) ankle = RS00 Ø57 (small, NOT RS06 Ø88) -> gone is the packaging problem that had pushed us to Encos; (2) sensors -> none (QDD).
- MATH (robot ~20 kg; the motors alone ~12 kg, very light PA-CF structure): hip/knee/shoulder RS06 36/11 = comfortably OK for flat-ground walking (RMS << 11). Ankle = the ONLY critical point: RS00 direct 14 Nm < ~16 Nm of balance at 20 kg -> ~2:1 IS NEEDED, which however is provided for FREE by the ankle pushrod/linkage (already planned) -> ~28/10 Nm. OK.
- Honest CAVEATS: keep it LIGHT (~20 kg); it is a WALKER not a squatter (RS06 11 Nm continuous does NOT hold a deep static squat/stairs); modest dynamics (flat-ground ZMP, Asimo style, not Cheetah); = optimization for SIMPLICITY (~EUR 4k, zero sensors, proven) NOT "maximum quality" (weaker/bulkier than Encos, no fine torque-control). Deliberate choice.
- RobStride LINEUP VERIFIED (web 2026-06-20): RS05 Ø46/5.5Nm/191g | RS00 Ø57/14Nm/10:1/310g | RS02 Ø78/17Nm/7.75:1/405g | RS06 Ø88/36Nm/9:1/621g | **RS03 Ø106/60Nm/9:1/880g** | RS04 Ø110/120Nm/40 rated/9:1/1400g. (RS01 = single encoder, avoid.) **RS03 = useful discovery = HIP sweet-spot** (between RS06 36 and RS04 120; lighter than RS04).
- **ASYMMETRIC ANKLE (user idea 2026-06-20, VALIDATED):** pitch = RS06 (36 Nm) in the SHIN via pushrod (~30 needed: balance M·g·half-foot-length + push-off); roll = RS00 (14 Nm) on the FOOT, direct (only ~9 needed: NARROW foot -> half-width ~4.5cm = half the lever arm of pitch, and NO push-off in roll). RS00 is enough, with margin. Packaging: large motor proximal (shin), small one distal (foot). Caveat: CoM over the support foot (RS00 5 Nm continuous is thin in static single-leg, ok while walking).
- "RS05 on the hip" = user TYPO: RS05 is 5.5 Nm (too little for ANY hip DOF, 16-40+ are needed). For the hip: RS03 (60) or RS04 (120).
- RobStride HEAVY mapping: hip pitch/roll RS03 (or RS04) | knee RS03/RS06 | ankle pitch RS06 + roll RS00 | shoulder RS06 | elbow RS00/RS02 | wrist RS05 | neck RS05 | hip-yaw RS00/RS02 | waist RS06/RS03.

**ToddlerBot (Stanford 2025, user question): NOT QDD.** It uses **Dynamixel XC330/XM** = high-reduction POSITION servos (~288:1 cycloidal), not backdrivable, no force-control from current. Tabletop robot ~0.5m/3-4kg for ML research, small/slow/cheap. Opposite corner of the design space compared with the user's dynamic G1-class -> it is not our route. (Confirms the old note: Dynamixel = wrong category for us.)

**EMAILS prepared (2026-06-20): ZeroErr, Leaderdrive, Honpine, Laifual** (turnkey torque-sensored harmonic: spec, physical torque sensor vs encoder, datasheet+STEP, price/MOQ/lead, EtherCAT/CAN, shipping to Italy).

**CONTROL CLARIFICATIONS (2026-06-20, user questions):**
- RL locomotion (Unitree/ToddlerBot/G1) = NN policy (small MLP) with OBSERVATIONS of joint pos/vel + IMU (NOT torque) -> POSITION targets -> PD -> torque applied via current. **No torque sensor, torque is NOT an input of the policy.** Runtime = deterministic NN ~50-200 Hz + PD ~1 kHz. (Classic deterministic alternative = model-based ZMP/MPC, ASIMO style; the modern approach is the learned NN policy.)
- Unitree G1: NO torque sensors; robustness = MECHANICAL COMPLIANCE of the QDD (backdrivable), not torque data. RobStride is the same, BUT the QDD keeps the DOOR OPEN (current=clean torque -> you can add force control/contact detection later). The stiff planetary Encos CLOSES that door.
- ACT / Diffusion Policy (manipulation): data = IMAGES + joint positions -> POSITION actions. Torque NOT used (only the contact-rich branch adds it). Position = backbone, torque = optional specialization.
- Encos "middle 25-36:1": GOOD for POSITION control (stiff enough, precise, less reflected inertia than a harmonic); AWKWARD MIDDLE only for FORCE control (too stiff for current=torque like a QDD, does not self-sense via deflection like a harmonic). Since RL walks in POSITION, Encos is in its GOOD regime.

**AI RECOMMENDATION (2026-06-20) - REFINED after the user clarified the GOAL: "humanoid that walks (calmly) + manipulates with ACT/diffusion policies".**
- MECHANISM (clarified to the user): the policy always outputs POSITION; the difference QDD vs high-reduction = how STIFFLY it tracks. (1) Stiff servo (Dynamixel/Encos): brute-force position loop, torque-accuracy IRRELEVANT, STIFF joint. (2) QDD + low-gain PD: small torque ∝ error = compliant SPRING; torque-accuracy IS NEEDED (the torque IS the spring). QDD = you can MODULATE the stiffness (stiff or compliant); high-reduction = stiff ONLY. ToddlerBot walks stiff because small(3.4kg)+flat ground+RL.
- TURNING POINT: ACT/Diffusion output POSITION and run on STIFF position-controlled hardware (ALOHA = stiff Dynamixel arms). STIFF = MORE PRECISE in free-space (the compliant QDD YIELDS/flexes = less precise). So for the user's MANIPULATION, the Encos stiffness is an ASSET. Calm walking = ok stiff.
- **For the user's EXACT goal (calm walking + ACT/diffusion manipulation in a controlled environment) -> ENCOS is the BEST fit**: precise where it matters (manipulation), compact/elegant, zero sensors, sufficient walking. (Correction of the earlier "RobStride" lean, which applied to a DYNAMIC capability that is not required.)
- **RobStride IF** you want the future OPTION: robust/dynamic locomotion (varied terrain, pushes, running) or CONTACT-RICH manipulation (insertion, safe contact) -> only the QDD lets you modulate compliance later. Bulkier, future-proof.
- CLEAR-CUT DECISION open: maximum manipulation precision + compactness NOW (Encos) vs being able to become robust/contact-capable/dynamic LATER (RobStride). For "walk + ACT/diffusion" as stated: lean ENCOS. (ZeroErr = out: heavy/expensive/slow, and its compliance/torque is of no use to position-based manipulation.)
- STATUS: strong hypothesis, NOT yet BOM. Direct comparison vs the Encos plan still to be done. The AI has NOT yet rebuilt the Excel sheet for this one (offered).

**OPTION REVISITED 2026-06-20: ZeroErr eRob (turnkey torque-sensored).** The user reopens ZeroErr as the "buy the complete joint, zero DIY" route. eRob module = frameless motor + harmonic + DUAL encoder + TORQUE SENSOR + brake + driver, all integrated (CAN/EtherCAT). Lineup verified (zeroerr.com): 70F Ø70/35Nm/0.77kg, 70I Ø70/70Nm/0.88kg, 80F Ø80/71Nm/0.89kg, 80I Ø80/112Nm/1.09kg, 90I Ø90/191Nm/1.64kg, 110I Ø110/408Nm/2.68kg; max 60 RPM (40 on the large ones). T series = RIGHT-ANGLE versions (heavier). **Minimum Ø70 -> NOTHING for the WRIST** (a separate small one is needed: Steadywin GIM3510 Ø46 / RS05 Ø46 / Encos A2806 Ø44).
- User mapping: 70F ankle, 80I knee/hip (the "strong" one), 70F/70I shoulders/elbow/waist, wrist = other.
- HONEST VERDICT: it solves turnkey sensing, BUT = **the HEAVIEST and MOST EXPENSIVE option**: ~19-21 kg of actuators alone -> robot ~35-40 kg (more than the G1!), premium price (~$700-1500 each, ~$20k+). It CONTRADICTS the "light humanoid" and the rejection of Bota for weight/cost. 60 RPM = ok for calm walking, borderline for the knee at normal cadence. Worth it only if the user pays weight+money to eliminate all DIY.
- ALTERNATIVES in the same category (turnkey torque-sensored): **Honpine** (direct peer, CN, cheaper), **Leaderdrive** (= RobotEra supplier, already contacted), **Laifual**, **HEBI X-series** (US, SEA, top API, premium), **Innfos/DAMIAO SCA** (QDD, lighter). Advice: Honpine+Leaderdrive quotes before ZeroErr.
- EMAILS prepared for ZeroErr + Leaderdrive (spec+quote: physical torque sensor vs encoder, datasheet+STEP, price/MOQ/lead, EtherCAT/CAN, shipping to Italy).

**ENCOS SPECS (name decode + data found). NAME = EC-A[Ø stator][h stator]-[P plan / H harm][stages]-[REDUCTION]; the number
at the end is the REDUCTION, not the torque. Torque = motor x reduction.**
- IMPORTANT: the Ø in the name is the STATOR; the actual MODULE is larger. A6416 -> Ø88 (like RS06); A4310/A4315 -> **Ø56 (= like RS00 Ø57!)**; A2806 -> Ø44.

**REAL SPECS FROM THE DATASHEET V3.15EAP (read 2026-06-19, no more estimates):**
| Model | Reduction | Ø mod | Length | Weight | Rated Nm | Peak Nm | Rated/Peak RPM | Kt | Nm/kg |
|---|---|---|---|---|---|---|---|---|---|
| EC-A2806-P2-36 | 36:1 | Ø44 | 44 | 162 g | 3 | 12 | 207/220 | 1.35 | 74 |
| EC-A4310-P2-36 | 36:1 | Ø56 | 60.5 | 382 g | 12 | 36 | 75/89* | 1.4 | 94 |
| EC-A4315-P2-36 | 36:1 | Ø56 | 69.5 | 485 g | 25 | 75 | 109/117 | 2.8 | **155** |
| EC-A6416-P2-25 | 25:1 | Ø88 | 67.5 | 805 g | 40 | 120 | 107/120 | 2.74 | 149 |

All: dual encoder, CAN/CAN FD 1M, cross-roller bearing at the output. *(A4310 measured at 24V -> at 48V speed ~1.5-2x.)*
- **3 DISCOVERIES from the datasheet:** (1) A4310/A4315 are **Ø56** (not Ø63 as the AI had estimated) = like an RS00 -> ankle advantage EVEN clearer vs RS06 Ø88.
  (2) **A4315 = same Ø56 as the A4310, +9mm/+103g, but DOUBLE the torque (75 vs 36 Nm)** and MAX density 155 Nm/kg -> it is THE "2 models always 43" (A4310 light + A4315 strong, same diameter).
  (3) **A2806 exists** (Ø44, 162g, 12Nm, 220 RPM): it was NOT in the Foxtech catalog -> "tiny" wrist/hands option (3rd size).
- LEGS A6416 vs RS04 (datasheet): A6416 smaller (Ø88 vs Ø106), lighter (805 vs 1420 g = **-3.7 kg over the 6 joints**), +continuous torque (40 vs 30 Nm);
  RS04 faster (~333 vs 120 RPM) and backdrivable (9:1 vs 25:1, reflected inertia ~8x less). 120 RPM A6416 = 12.6 rad/s = OK for walking (even a light trot), Encos is NOT slow like ZeroErr.
- SIZE DECISION OPEN: (A) 2 modules A6416+A4310 (ankle with A4310 36Nm at the limit, or A6416 Ø88 large) | (B) 3 modules +A4315 ankle (Ø56/75Nm perfect). Technical specs = WE HAVE THEM. To ask Foxtech: only the per-unit price for Italy + STEP CAD + lead time + MOQ.

**ENCOS HARMONICS (datasheet V3.15, read 2026-06-19; all DUAL ENCODER + CAN/CAN-FD, backlash ~10 ARCSEC = 60x less than the planetaries):**
- A3814-H14-107: 107:1, Ø53x78.5, 434g, 20/60 Nm, 47/52 RPM, Kt 4.2. | A5013-H17-100: 100:1, Ø63x81.5, 630g, 30/90 Nm, 33/38 RPM, Kt 5.9. | A6013-H20-100: 100:1, Ø73x84, 906g, 40/130 Nm, 45/47 RPM, Kt 5.6.
- KEY POINT: the harmonic flexspline is COMPLIANT -> the dual encoder CAN estimate torque from deflection (like ZeroErr), something that does NOT work on the Encos planetaries (stiff). BUT: harmonics are SLOW (33-52 RPM, like ZeroErr) and Encos does not provide a turnkey torque function (DIY, marginal with 0.1-0.2 deg encoders). They are the ones Asimov uses on hip-roll/yaw/shoulder.

**PAPER "UKF Sensor Fusion for Joint-Torque SENSORLESS Humanoids" (Sorrentino/Romualdi/Pucci, IIT, ICRA 2024; arxiv 2402.18380; read 2026-06-19) = POSSIBLE STRONG SOLUTION:**
- It estimates the joint torques WITHOUT torque sensors, by fusing (UKF) motor current + encoder + IMU + **F/T at the FEET**. It models the gearbox friction (Coulomb+viscous). It handles external contacts (beats RNEA: 1.96 vs 18.3 Nm under contact). RMSE 0.05-2.5 Nm. Tested on ergoCub. **OPEN-SOURCE CODE** (github ami-iit).
- FOR US: instead of instrumenting 10-18 joints, GRF at the foot + Encos current+encoder (already there) + IMU -> the observer estimates ALL the torques. Total sidestep of the instrumentation. Cost = software + friction identification (the user's control engineers). Caveat: validated on a robot on a pole (not free walking yet), a good friction model is needed, accuracy < dedicated sensor (ok for the legs, for fine manipulation maybe sensors later). = the "4th card" now concrete and proven.
- REPO (github ami-iit/paper_sorrentino_2024_icra...): Python on **bipedal-locomotion-framework** (IIT), dataset+example ergoCub right leg. To port it: our URDF + framework + dataset logged from our motors + **per-joint friction identification** + UKF covariance tuning. Well-defined sw work (control engineers' stuff), BUT the hard part (the estimator) is already written and open.
- ergoCub (the paper's robot) = HARMONIC + frameless (IIT-custom, like RobotEra; harmonic friction paper arxiv 2410.12685). WARNING: the UKF friction model is for HARMONICS; our Encos are PLANETARY -> re-identify the friction (the method generalizes: tau_j = rid*tau_m - tau_attrito).
- **BOTA REJECTED by the user 2026-06-19 (cost + distal WEIGHT).** Substitute: the paper mainly wants **vertical force + center of pressure (ZMP)** at the foot -> **4 load cells at the corners of the foot** are enough, or better **strain gauges on the foot PLATE** (already there -> ~zero mass, ~50 EUR of gauges). It gives Fz+2 moments (the bulk of the wrench); the horizontal shear is missing (secondary on flat ground). Standard humanoid approach (4 load cells).

**CORRECTION 2026-06-19 "harmonics/ZeroErr too slow" = IT WAS TOO ABSOLUTE.** It depends on the cadence. Critical joint = KNEE in swing: NORMAL cadence ~50-67 RPM, SLOW cadence ~25-40 RPM.
- ZeroErr 60 RPM = borderline at normal cadence, ok when slow. Encos-H 38-52 RPM = below at normal cadence (knee), ok when slow. NOT a flat "too slow".
- The REAL reasons NOT to put harmonics on the legs remain: (1) REFLECTED INERTIA ∝ rid^2: a 100:1 harmonic reflects ~10.000x (vs 625x for our 25:1 planetary, 81x for the QDD 9:1) -> legs deaf to impacts/disturbances unless you add an SEA spring (ANYmal trick); (2) ZeroErr Ø70 too large/heavy for the ankle. Our PLANETARY A6416 (120 RPM, 625x) = more speed margin AND less reflected inertia -> the right choice for the legs.
- "Torque estimation from dual-encoder marginal for 0.1-0.2 deg encoders" = EASY to try (sw, free), HARD to make usable: signal (harmonic windup 0.2-0.5 deg at full torque) / noise (diff. of 2 encoders ~0.15-0.3 deg) = only 1-3x at full load, BELOW noise at low/medium torque -> rough estimate (ok for collision detection, useless for fine force control). ZeroErr manages it with better encoders + stiffness/hysteresis calibration. On the Encos PLANETARIES it does not work at all (stiff).

**BRAND COMPARISON for single-brand (research 2026-06-17, IMPORTANT):**
- **CubeMars HAS A GAP in the mid range ~36 Nm**: it jumps from AK40-10 (Ø46, 4 Nm) to AK70-10 (Ø89, 25 Nm) / AK10-9 (Ø98, 50 Nm,
  940 g!). Nothing compact at 36 Nm. Our robot has ~14 joints at 36 Nm (ankle4+hip-yaw2+waist2+shoulders6) ->
  with CubeMars they would all be Ø89-98 = ABSURD. **All-CubeMars REJECTED** (good only for wrist AK40 + legs AKE90).
- Compactness at 36 Nm: **Encos A4310 Ø56 < Steadywin GIM6010-36 Ø70 (but 36:1 stiff) < RobStride RS06 Ø88 < CubeMars Ø98.**
  Encos wins exactly where we have the most motors. RobStride = COMPLETE family with no gaps (RS00->RS06->RS04).
- CubeMars was NOT rejected for control reasons (the AI's confusion with the user): it was removed for SINGLE ECOSYSTEM (line 215). The control
  problem was the RS01 (SINGLE encoder). CubeMars with DUAL-encoder versions (AK10-9 v3) is ok. Universal rule:
  ALWAYS take the 2-encoder version, of whatever brand (applies to RS01 vs RS02, base-AK vs AK-dual, etc.).
- FOXTECH RESPONSIVE: they replied right away (mail + WhatsApp), datasheet+CAD on the way -> Encos sourcing is NOT the
  ordeal that was feared. Only the REDUCTION remains to be evaluated (below).

**MIT CHEETAH = origin of the QDD (background for the user's interview, 2026-06-19):** Lab = MIT Biomimetic Robotics, PI **Sangbae Kim**.
Cheetah 1/2/3 robots -> **Mini Cheetah (2019)**. Pioneering idea = "PROPRIOCEPTIVE ACTUATION": BLDC motor with a large air-gap radius +
a low SINGLE-stage reduction (~6:1, "quasi"-direct-drive) -> BACKDRIVABLE transmission, minimal reflected inertia (∝ N^2) = mitigates impacts, and
**joint torque = Kt*I*N read from the CURRENT, without a torque sensor**. Canonical paper = **Wensing, Wang, Seok, Otten, Lang, Kim,
"Proprioceptive Actuator Design in the MIT Cheetah", IEEE T-RO 2017** (+ Seok et al. T-Mech 2015 on efficiency). **Ben Katz (MS thesis 2018)**
= low-cost modular QDD actuator + the CAN "MIT mode" (pos/vel/torque-ff/Kp/Kd packet). FROM THERE descend CubeMars/T-Motor AK, **RobStride**,
Damiao, MyActuator and the Unitree motors - and they all speak "MIT mode" (the Encos implements it too). Interview PUNCHLINE: RobStride (~9:1) =
the pure MIT-Cheetah philosophy (current=torque); Encos (25-36:1) = a DEPARTURE from the QDD (compact) which, to get force control back, must
RE-ADD the torque sensor (like Tesla: high reduction + torque sensor). OpenTorque (Gabrael Levine) = the MIT QDD scheme + SEA spring.

**REDUCTION VERDICT for WALKING (research 2026-06-17, MIT QDD/biomimetics papers) - DECISIVE:**
- QDD sweet-spot = **6-9:1**; RobStride (~9:1) is right there. The research says "9:1 = balance between torque density
  and impact mitigation for dynamic walking".
- **Reflected inertia ∝ reduction².** So vs RobStride 9:1: **Encos 25:1 = ~8x reflected inertia, 36:1 = ~16x.** NOT marginal.
- Effect: more reduction -> less backdrivable, less responsive to impacts, worse at regulating contact. The research:
  "20-30:1 greatly increases the reflected inertia and reduces the response to impacts".
- VERDICT: Encos 25-36:1 **CAN walk** (slow, flat-ground, tethered = our case) but it is a **real step backwards
  vs 9:1, not marginal.** The WORST point = the **ankle at 36:1** (impact/contact joint: heel-strike, terrain).
  -> For walking QUALITY RobStride 9:1 is genuinely better; you pay for the Encos compactness in compliance/impacts.
  If you go Encos, consider a LOW-reduction motor at least on the ANKLE (RobStride or a 1-stage option), that is where the 36:1 hurts.

**RESOLUTION of "but Tesla walks like a dream with high reduction!" (2026-06-17, VERIFIED) - closes the brand choice:**
Tesla Optimus = high reduction (roller screw, NOT backdrivable) BUT with a **non-contact TORQUE SENSOR in EVERY actuator**
+ position sensors at INPUT and OUTPUT -> ACTIVE force control (measures the real force at the output, controls fast).
So there are TWO routes to walking well: (a) **low-reduction QDD** (RobStride ~9:1 / Unitree / MIT) = force control
through TRANSPARENCY, for FREE, no sensor; (b) **high reduction + torque SENSOR** (Tesla) = active force control.
ENCOS is high reduction (25-36:1) **BUT WITHOUT a torque sensor** (dual-encoder only, poor for estimating torque on a
stiff planetary) -> it can do NEITHER the one NOR the other = the compromise that walks WORSE than both.
**CONCLUSION (decisive, somewhat ironic):** to "walk like the humanoids of the FUTURE" with ACCESSIBLE stuff (no
Tesla control team, RL approach), the route is the **low-reduction QDD = RobStride (9:1)**, which is EXACTLY
what **Unitree G1/H2** use (the best accessible walkers: somersaults, running, all RL). The "futuristic one that
walks well" is obtained with RobStride, NOT with the Encos. Encos = only if you want compact and accept a less smooth walk.
The Tesla route (high reduction + integrated torque sensor) is NOT accessible: actuators with a torque-sensor cost an
arm and a leg and the Encos does not have them.

**UPDATE 2026-06-19 (user's interview + sensor choice) - "magnetic" means TWO different things, KEY distinction:**
- TESLA confirmed (web): rotary = frameless motor + **HARMONIC reducer** + **non-contact torque sensor** + encoder + cross-roller;
  linear = planetary roller screw. So Tesla = HIGH REDUCTION (NOT QDD) + non-contact torque sensor (MAGNETOELASTIC family).
  It is EXACTLY the camp the user is heading into with Encos+sensor: Encos+magnetic = DIY/low-cost version of the Tesla recipe.
- FIGURE: actuator architecture NOT disclosed; secondary sources say "QDD" but are not very reliable (the same ones get it wrong by saying Tesla=QDD). Do not state numbers.
- QDD camp (current=torque, no sensor) = Unitree G1/H1 (= RobStride lineage), MIT Cheetah. Opposite POLE to Tesla.
- **"MAGNETIC" = 2 different sensors:** (a) **dual magnetic encoder on a torsion flexure** = LIGHT/CHEAP/DIY (~$30-50/joint,
  AS5047/MT6701), BUT to get a signal a twist of ~1-2 deg at full scale is needed -> COMPLIANT flexure (~2000 Nm/rad) -> the joint becomes a
  **stiff SEA** (compliance ok/useful for walking, NOT for stiff manipulation). (b) **MAGNETOELASTIC** (NCTE/Magcanica, = Tesla):
  non-contact, STIFF shaft (no compliance), elegant BUT DIY = research (shaft magnetization, fluxgate, temp/hysteresis) -> in practice you BUY it.
- The user understood correctly: the bulky ready-made sensors (Bota/FUTEK flange) RE-BLOAT the in-line joints (knee/hip) = they ruin the Encos advantage.
  EXCEPTION = the FOOT: there you want a 6-axis F/T anyway (GRF/ZMP), it mounts BELOW the ankle, and there are only 2 -> Bota Rokubi at the feet remains justified.
- USER'S LEAN = magnetic route (a) = light/cheap stiff SEA on the leg joints. 4th CARD (control engineers): MODEL/LEARNING-based torque estimation from the
  dual-encoder alone + friction model (zero hardware, arxiv 2410.16591) -> prototype A/B vs the flexure. NB: (a) is a SEA, not Tesla's stiff sensor.

**WHO USES WHAT - torque sensing by brand (web 2026-06-19). CORRECTION of the AI's OVER-GENERALIZATION: it is NOT true that "almost all premium joints use strain gauges".**
- STRAIN GAUGES on a dedicated element at the harmonic output = standard in premium COLLABORATIVE ARMS: **DLR LWR -> KUKA LBR iiwa, Franka Emika Panda** (torque sensor in EVERY joint);
  UR/Yaskawa/Fanuc (F/T at flange/base). They are ARMS, not humanoids. (They do NOT instrument a random part: a DEDICATED spoke/ring at the reducer output.)
- **ANYmal (ANYbotics/ETH) = SEA, NOT strain gauges**: motor + harmonic + SPRING in series + 2 absolute encoders (output pos + spring deflection) -> torque from deflection.
  Torque res. ~8 mNm, pos 0.025 deg, +impact protection. = the CLOSEST analogue to the user's Encos+magnetic-deflection plan (high reduction + deflection readout).
  PAPER: Hutter et al., "ANYmal - A Highly Mobile and Dynamic Quadrupedal Robot", IROS 2016 (DOI 10.1109/IROS.2016.7758092; open access SciSpace/ETH). Bonus: arxiv 2511.06796 "Human-Level Actuation for Humanoids".
- TESLA = non-contact magnetoelastic. UNITREE(G1/H1)/MIT = QDD from current (NO sensor). Many humanoids = SENSORLESS (estimation by observer/learning: UKF arxiv 2402.18380, PINN 2507.10105).
- **RobotEra = LEADERDRIVE motors (stated by the user, who OWNS the robot; web 2026-06-19 confirms): Leaderdrive = HARMONIC (strain-wave), one of the 2 Chinese majors together with Laifual.**
  Ratios 30-500:1 (typical joint modules 50-160:1) -> RobotEra = HIGH HARMONIC REDUCTION = GEARED camp (Tesla/ANYmal/DLR), NOT Unitree QDD. Confirmation: the user feels the joints
  (with the motor off) as "movable but with resistance, not free" = consistent with a harmonic, NOT with the 9:1 QDD (which turns almost freely). NB: the test with the motor OFF only tells you the MECHANICS
  (geared vs QDD), NOT whether there is a torque sensor (= active behaviour, with the motor ON). Leaderdrive offers modules with an optional INTEGRATED torque-sensor; moreover the harmonic flexspline
  is compliant -> torque estimation from dual-encoder WORKS (unlike the stiff Encos planetary). RobotEra sensor = to be confirmed with the exact MODEL / SDK (measured-torque field vs current).
  IMPLICATION for us: RobotEra validates the compact high-reduction route for a serious humanoid, BUT they = HARMONIC (easy torque-sensing via flexspline) vs us = stiff PLANETARY (sensor to be ADDED). Real tradeoff.
- **X-Humanoid/Tiangong(TienKung): sensor type NOT public** (searched, not found; do NOT invent). Tiangong partly OPEN-SOURCE -> one can search in their repos/SDK.
- NET: there is no such thing as "everyone does it this way". Arms->gauge; ANYmal->SEA; Tesla->magnetoelastic; Unitree->nothing. The 3 candidate methods each have a premium precedent -> choose on OUR constraints, not by imitation.

**CORRECTION 2026-06-17 (the user reports being able to get the control engineers): reopens the Encos.** (1) The AI was too categorical about
"Encos without sensor": the DUAL-ENCODER is there precisely to estimate torque (motor position vs output -> deflection across the
reducer = torque). On a stiff planetary the signal is noisy but it IS THERE, and it is what a good control engineer exploits
(+ friction models). (2) SPECTRUM: Encos+current only = poor force control; Encos+dual-encoder+good control engineers =
DECENT (walks well); Encos + added dedicated torque SENSOR = Tesla-grade. RobStride QDD 9:1 = good out-of-the-box
with little control effort. (3) For Tesla-grade add TRUE torque: a reaction load-cell at every joint, OR
SEA (series elastic element -> the dual-encoder reads the spring = clean torque, costs bandwidth/stiffness), OR actuators
with an integrated torque-sensor (expensive, not Encos). (4) Updated CONCLUSION: IF the user really has the control team,
the compact Encos + dual-encoder + control becomes a valid choice again for "small + walks well"; the torque-sensors get added
at the transition to HW. In sim (now) force control is modelled anyway -> we can proceed with the CAD without deciding the
sensors today. The fork remains: QDD/RobStride (simple, bulky) vs Encos+control (compact, more control work).

**DEEP DIVE 2026-06-17 (verified, SCALES BACK the dual-encoder estimation):** the research confirms that at HIGH
reductions the reducer friction makes torque estimation from current UNRELIABLE -> dedicated strain gauges are needed. The
dual-encoder estimates torque from DEFLECTION: decent on a HARMONIC (compliant flexspline), **POOR on a stiff PLANETARY**
(A4310/A6416 = almost all of ours: minimal deflection + it does not capture friction). So the Encos dual-encoder **does NOT
replace a torque sensor** on planetaries (the AI had overestimated it). Steadywin GIM3510 = dual-encoder YES + **8:1 low
reduction** -> there the estimation from CURRENT works (almost QDD), force control ok. Vs a real sensor: strain gauge ~1-2% error,
high bandwidth, captures friction; the deflection on a planetary is noisy and systematically wrong -> not comparable.
**MOTORS already with an INTEGRATED torque sensor (found but PREMIUM, ~1000-3000 EUR/joint -> 30 joints = 30-90k):**
SensoDrive SENSO-Joint (DE: sensor+HarmonicDrive+motor+driver, certified, 5 sizes), TQ-RoboDrive ILM (DE, heritage from
DLR), Kinova (torque-sensored but sold as arms), Harmonic Drive FHA. **There is NO actuator with a torque-sensor that is
integrated AND cheap** (CubeMars/Unitree/RobStride/Encos = current+encoder, no sensor).
**FINAL RULE - pick 2 out of 3:** small+cheap = MEDIOCRE force control; small+TOP-force-control = EXPENSIVE (Encos+sensors
or SensoDrive); cheap+GOOD-force-control = BULKIER (RobStride QDD 9:1, current is enough as with Unitree). The user's control
engineers are NOT enough on their own: the torque SIGNAL is needed = HARDWARE (sensor), either expensive or DIY strain gauges x30.

**OPTION 1 PREFERRED by the user (2026-06-17): compact ENCOS + DIY torque OUTFITTING (the user knows guys who know how to
do it, to be confirmed).** 30 sensors are not needed, only the LEG joints where force control matters. PRIORITIES:
1) ANKLE (4: pitch+roll x2) = contact joint + the stiffest (36:1), the most important. Better still a SEA
(series elastic element): the dual-encoder reads the spring = clean torque AND it absorbs the impact -> 2 birds with one stone. 2) KNEE
(2) + HIP PITCH (2). 3) HIP ROLL (2). -> "walks well" set = 10 joints (legs excluding hip yaw). Do NOT sensorize: hip
yaw (gravity 0), WRIST (Steadywin 8:1 low reduction, current is already enough), neck, shoulders/elbow (optional for
fine manipulation, later). DIY sensor components: Bota Systems (6-axis F/T), FUTEK (torque sensor).

**OUTFITTING - concrete DIY METHODS (2026-06-19, user's question "if I want to do it on my own, how is it done"):** principle = add
an element that deforms in a MEASURABLE way between the reducer output and the link (the internal dual-encoder is NOT enough: deflection < noise). 3 routes:
1) STRAIN-GAUGE FLANGE: spoked disc (shear), 4 gauges at +-45 in a FULL Wheatstone bridge (rejects bending/axial/temp),
   sized for ~1000-1500 ue at full scale; amp INA826/AD8421 + 24-bit ADC (ADS1235/1262) at >=1 kHz -> CAN. Stiff, high bandwidth;
   bonding = an art. No slip-ring if ROM is limited (cable loop). It is what the user's friends mean. (HX711 for proto only, slow.)
2) SEA (known spring + 2 encoders, ANYmal ANYdrive type): torsional spring -> at full scale 5-15 deg = LARGE deflection, read by
   2 magnetic 14-bit encoders (AS5047/MT6701), no gauges. +IMPACT PROTECTION (gold on a leg). Costs position bandwidth + resonance.
   Perfect DIY REFERENCE: **OpenTorque Actuator** (Gabrael Levine, open-source QDD+SEA for legs).
3) NON-CONTACT MAGNETIC TORSION: torsion bar + magnetic encoder at the 2 ends, angle difference = twist (tune for ~1-3 deg at
   full scale). Middle way (no bonding/slip-ring); sensitive to concentricity/temperature. It is the simplified "Tesla route".
INTEGRATION: the Encos in MIT-mode does NOT hand you the torque loop -> YOU close it (read state via CAN + sensor -> command current/Tff)
at ~1 kHz, low latency, sensor synchronized with the telemetry. DIFFICULTY: 1 joint = 1-2 weeks (for someone who knows how to strain-gauge);
~18 joints = a sub-project lasting months = THE work that RobStride 9:1 saves you. Solo strategy: prototype 1 leg joint, SEA on the
legs, arms current-based at first. The distal mass of the sensor matters (on the foot).
**READY-TO-MOUNT (buy & bolt-on, NO DIY; requested by the user 2026-06-19):** FIRST CHOICE = **Bota Systems (CH, ETH spin-off)**: 6-axis F/T
robot-grade, CAN-FD/EtherCAT/ROS -> **Rokubi** (legs/ankle = ground reaction force; manipulation), **PixONE** (humanoid joints),
**MiniONE** (30 g, fingertips/hands). At the FOOT and at the HANDS you want a 6-axis F/T anyway (GRF/ZMP, contact) -> Bota there. For 1-axis torque at
knee/hip/waist = hollow flange: **Sunrise Instruments** (CN, value) / **FUTEK** (US, easy to order) / **ME-Mess.** (DE) / **HBK-Kistler**
(premium metrology). Non-contact magnetoelastic (no spring/bonding): **NCTE** (DE) / **Magcanica** (US). Ready-made cost ~$1-3k/joint x ~10 = $10-30k.

**MOTORS ALREADY "OUTFITTED" with the torque sensor, ready-made (2026-06-17, discovered with the user):**
- **ZeroErr eRob** (I-type, sizes 70I/80I/90I/110I = Ø70-110): HARMONIC + dual-encoder + "VIRTUAL torque sensor"
  (torque estimation from flexspline deflection + stiffness/hysteresis model). EU-cert + first CR-cert for humanoid joints.
  PLUG-AND-PLAY, no DIY. Key INSIGHT: the virtual-torque-sensor from dual-encoder WORKS on the HARMONIC (compliant
  flexspline = measurable deflection), and is POOR on the stiff planetary -> so the HARMONICS (ZeroErr, or the Encos-H
  A3814/A5013) give torque sensing "for free"; the planetaries (A4310/A6416) do not. HOWEVER harmonic = high reduction = high reflected
  inertia = CONTROLLED/precise walking (Tesla/Figure/DLR-HRP style), NOT dynamic like the QDD. Price premium.
- Honpine / Makongear / Oz Robotics: Chinese harmonics with a PHYSICAL torque-sensor but customizable (MOQ, not off-the-shelf),
  cheaper than ZeroErr, less plug-and-play. SensoDrive/TQ/Kinova/HarmonicDrive = German premium (already in the list above).
- DAMIAO (Dynamic-Motion) DM-J4310-2EC: cheap QDD ($116) dual-encoder MIT-mode -> it is in the QDD camp (like RobStride),
  it does NOT have a physical torque sensor. (Damiao had already been excluded for single-ecosystem.)

**EXCEL SHEETS: now 4 motor sheets - "umanoide" (complete RobStride BOM), "MOTORI RobStride" (clean motor list),
"MOTORI Encos (quote)" (3 models: A6416/A4315/A2806), "MOTORI premium" (CubeMars/Encos mix).**
**ENGLISH VERSION (for the user's interview Mon 2026-06-22): SEPARATE script build_umanoide_en.py -> "BOM umanoide G1 - EN.xlsx",**
**5 sheets: Summary | Joint map (30 DOF) | Motors-Encos (chosen) | Motors-RobStride (alt) | Torque sensing. To be kept in sync by hand with the IT one.**

**THREE WALKING CAMPS (summary):** (a) low-red QDD (RobStride/Unitree) = dynamic/agile, force control from current,
cheap, bulkier; (b) HARMONIC+virtual-torque (ZeroErr / Encos-H) = controlled-precise walking in the style of Tesla/
Figure, ready-made but premium, less dynamic (reflected inertia); (c) PLANETARY+DIY-sensors (Encos-P + strain gauges) =
compact but a lot of work. For "Unitree-dynamic" -> (a). For "Tesla/Figure-controlled compact" -> (b) ZeroErr.

**ZeroErr DROPPED for the LEGS (2026-06-17, from the official eRob page):** eRob lineup 70F(Ø70,35Nm,0.77kg)/70I(70Nm,
0.88kg)/80I(Ø80,112Nm,1.09kg)/90I(Ø90,191Nm,1.64kg)/110I(Ø110,408Nm,2.68kg)... BUT **MAX speed = 60 RPM** (all of them).
The knee in normal walking reaches ~300-400 degrees/s = 50-67 RPM -> ZeroErr is ALREADY at the limit for walking slowly,
too slow for dynamics. They are actuators for precision COBOTS, NOT for locomotion. And below Ø70 it does not exist (no wrist).
Moreover ZeroErr != Tesla: Tesla uses ROLLER SCREWS (fast) + sensor; ZeroErr uses a HARMONIC (slow). -> ZeroErr out of the
legs. To walk you need SPEED = low reduction = QDD. CONCLUSION: the sane default is RobStride QDD (fast/dynamic,
force control from current, cheap, complete); the only alternative = Encos+DIY-sensors if compactness is worth the work.

**OFFICIAL ENCOS MANUAL read (Motor Debugging Manual V1.18, 2026-06-17) - CONFIRMS and REINFORCES:**
- ENCODER: dual (motor + output), 14-bit, BUT real accuracy only **0.1-0.2 degrees** ("quality issues"). -> the
  deflection on a stiff planetary (at rated torque) is minimal and GETS SWAMPED by the encoder error (0.1-0.2 deg) ->
  **torque estimation from dual-encoder is NOT usable on the planetary Encos** (confirmed: the AI was right to scale it back).
  Output encoder single-turn (loses the turn count at power-off).
- CONTROL: it has MIT mode (Power-Position Mixed: i=(Kp*(p_des-p)+Kd*(v_des-v)+Tff)/Kt, "for foot-type robots") + Current/
  Torque mode + Servo pos/speed. BUT the **torque is ALWAYS from CURRENT x Kt (open-loop), NO torque sensor**. Force
  control = like RobStride (from current) -> at high reduction it is unreliable because of friction -> for true torque you NEED an
  added PHYSICAL sensor (the DIY outfitting is mandatory, the dual-encoder does NOT replace it). CAN 1M, 2 kHz, fb 0.4ms.
- THERMAL: torque derating above 105 degrees C coil (max 120 stop); high continuous torque heats it up -> derating. XT30 15A/30A
  peak; capacitors ARE NEEDED for the energy-return (regen) or the driver burns out. Voltage 20-57V.
- MODELS in the manual = EC-4310 / 8112 / 10020-24 / 13715 / 13720 (planetary P series). The A6416/A4315/A5013-H/A3814-H of
  Asimov are NOT in the manual -> they could be CUSTOM/non-standard: VERIFY availability with Foxtech (the standard
  leg catalogue is A8112 94Nm / A10020 150Nm). For VESC debugging an M2 screwdriver is needed to open the back on 4310/8112/10020/13715/13720.

**CORRECTION "legs = Ø100 mandatory" (WRONG):** Asimov does hip pitch + waist in **Ø64** (A6416, planetary 25:1) on
35 kg, "up to 120 Nm peak". The legs do NOT have to be Ø100: with a higher reduction (25:1 or harmonic) you get
~120 Nm in **Ø64**, less backdrivable but OK for WALKING ONLY. Our tethered robot (~28-30 kg) fits within that. -> elegant legs
in Ø64 are possible. The Encos harmonic (H) gives high reduction + ZERO backlash in small frames (Ø38-50): excellent for compact joints.

**Asimov joint ranges (from the sim):** hip pitch -120/+57, hip roll/yaw ±45, knee 0-86, ankle pitch ±20 / roll ±5.7 (SMALL),
waist yaw ±90, shoulder pitch -50/+180, elbow 0-140, wrist yaw ±180 (degrees). NB the Asimov ankle has a smaller range than ours.

## Torque calculation method + final post-downsizing check (2026-06-08)

**How to calculate the torque required at a joint (for the other AI session and for every recalculation).** Basic rule: continuous hold ->
compare with the RATED value; motion/short peak -> compare with the PEAK value. A motor "holds up" if static < rated AND
dynamic < peak.

1. STATIC (holding still in the worst pose): `tau_stat = g * SUM(m_i * b_i)`, with `b_i` = HORIZONTAL
   lever arm of mass i from the joint axis in the worst pose. g = 9.81.
2. DYNAMIC (bang-bang: accelerate for half the travel, decelerate for half): `tau_dyn = tau_stat + I*alpha`, with `I = SUM(m_i * b_i^2)`
   and `alpha = 4*theta / t^2` (theta = amplitude in rad, t = time). Realistic speeds: 90 degrees in 0.5 s = moderate;
   0.3 s = fast (manipulation does not require it); 0.8 s = slow.
3. VERTICAL AXES (yaw): gravity ~= 0 -> dynamics only (inertia about the vertical).
4. LINKAGES (ankle, pushrod-driven waist): the torque at the JOINT is fixed by the load; `tau_motor = tau_joint *
   (crank_motor/crank_foot)`, then / n motors sharing it. At 1:1 with 2 motors -> tau_joint/2 per motor.

**Inputs used.**
- Motor masses (they become lever-arm loads when they are distal): RS00 0.310, RS02 0.405, RS04 1.420, RS05 0.191,
  RS06 0.621 kg.
- JOINT POSITIONS from the G1 mode_11 (`g1_joints.csv`) -> they give the lever arms. E.g. arm: shoulder->shoulder_yaw 0.106,
  shoulder->elbow **0.187** (projection with the arm EXTENDED, not the 16 mm at rest!), shoulder->wrists 0.287/0.325/0.371,
  shoulder->hand 0.412 m; elbow->payload 0.22 m.
- Estimated PA-CF segment masses: upper arm ~0.30, forearm ~0.25, hand ~0.30 kg.
- Global masses: robot ~35 kg; leg below the pitch ~7.0 kg (CoM 0.305 m below the axis); upper body above the waist
  ~10-14 kg (depends on the battery, CoM ~0.25 m above the joint); arm below the shoulder ~2.9 kg.

**Worst poses considered per joint (what goes into the calculation).**
- Shoulder pitch: ARM EXTENDED HORIZONTALLY forward, each mass at its own lever arm, including the elbow motor (0.405 kg
  at 0.187 m: it gets lifted) -> 6.3 Nm static.
- Shoulder roll: arm extended horizontally to the side (abduction) = same as pitch.
- Shoulder yaw: arm RAISED, payload 2 kg at 0.20 m from the upper-arm axis (with the arm down gravity is 0).
- Elbow: forearm at 90 degrees, payload at 0.22 m from the elbow.
- Hip pitch: leg cantilevered horizontally, leg CoM 0.305 m below the axis.
- Hip roll: single support, mass above the hip ~28 kg x lateral offset 0.10 m.
- Knee: squat, robot weight x lever arm (0.04 straight / 0.15 half / 0.22 deep).
- Ankle: tipping over, robot weight x ankle-to-toe lever 0.13 m = ~46 Nm at the joint, /2 motors (at 1:1).
- Waist pitch/roll: upper body x 0.25 m x sin(bend angle), /2 pushrods.
- Yaw (hip/waist/shoulder): gravity 0, dynamics only (turning/twisting).

**Results with the final motors** (stat% relative to rated, dyn% relative to peak):

| Joint | Motor | Result | Numbers |
|---|---|---|---|
| Hip pitch/roll | RS04 | OK | stat 52-69%, dyn 58-75% (max RobStride, 86% of the G1) |
| Hip yaw | RS06 | OK/TIGHT | ~28 Nm at G1 mass = 78% peak; ~37 Nm if scaled to 46 kg = beyond peak |
| Knee | RS04 | WARNING | standing/walking OK (34%); deep squat HELD 129-189% rated (max motor, inherent limit) |
| Ankle pitch/roll | RS06, one per axis | OK with CAD | 36 Nm peak vs 35 G1; normal walking estimated 17-32 Nm. Toe-edge case 45-59 Nm: needs mechanical advantage or must be avoided |
| Waist yaw | RS06 | OK/TIGHT | ~28 Nm at G1 mass < 36 peak; vertical axis, no gravitational load |
| Waist roll | RS03 | OK | 12-17 Nm estimated at 30 degrees < 20 rated; 21-30 Nm at 60 degrees only intermittent < 60 peak |
| Waist pitch | none | REMOVED | torso pitch comes from the hip pitch joints, Figure-like choice |
| Shoulder pitch/roll | RS06 | OK/TIGHT | ~10.8 Nm static with arm horizontal + payload 1 kg, just below 11 rated; 36 peak > 25 G1 |
| Shoulder yaw | RS00 | OK for 1 kg | ~21 N per hand continuous at the G1 lever arm of 0.24 m; about 1 kg of box reliably, with friction and SF2 |
| Elbow | RS06 | OK | ~4.4 Nm static with 1 kg, ~6.6 Nm with 2 kg < 11 rated |
| Wrist x3 | RS00 | OK | 51% rated with 2 kg in hand |
| Neck x2 | RS05 | OK | head 1.5 kg, 46% rated |

**3 usage rules so that everything holds up:** (1) legs almost straight, no held deep squat; (2) battery LOW in the
pelvis + do not keep the torso bent for long; (3) arms <=1.5 kg comfortably / 2 kg at moderate speed, no flinging.

**2 mandatory checks in CAD:** (a) ankle crank ratio >=1:1; (b) waist pitch/roll crank ratio + battery
position (they decide whether RS06 is enough or RS03 is needed). Fallbacks already in the BOM: waist->RS03, elbow->RS06. No motor is rejected
for the intended non-acrobatic use; the legs (RS04 not downgraded) hold up when standing and when walking.

## Motor mounting rule (user decision 2026-06-08)

**ALL motors are mounted from the FRONT (output face).** Universal: every QDD has its output at the front, only some also offer
the rear -> by standardizing on the front you are fine with any brand (RobStride/CubeMars/MyActuator). Scheme:
the fixed bone is a plate screwed to the STATOR holes of the output face, with a central clearance hole; the motor body sits
behind the plate; the output (rotor) protrudes through the hole; the moving bone is screwed to the rotor at the front. The rear is NOT
a mounting interface (on the RS06 drawing the rear Ø70 is in parentheses = reference/cover; the rear screws
hold the motor together, they are not to be used). RS06 dimensioned interface = output face: 6xM4 (rotor) + 8xM3 on Ø82
(stator) + 3xØ4 dowel pins.

NO adapters or extra parts (the user is happy to reprint; larger envelopes are not a problem). The POSITIONS
OF THE JOINTS are set by the MOTORS with their envelope (packing), as in the G1: changing a motor moves the joints, and that is
fine -> the RL gets redone FROM SCRATCH (user choice accepted, it is not a tragedy). The joint axis is NOT frozen: the
real motors are packed and the joints fall where they fall. The G1 mode_11 joint coordinates (`g1_joints.csv`) are a
REFERENCE for proportions (leg length, pelvis width...), NOT a rigid target to hit (they were for motors of
~80 mm). The ONLY thing that stays fixed is the mounting TOPOLOGY: front-mount for all -> a motor change remains
"re-pack the same type of skeleton + RL from scratch", never a mount that flips front/rear and completely upsets the shape
of the bones.

Purchase links and spec sheets:

- RS04: <https://www.seeedstudio.com/Robostride-04-Actuator-p-6775.html>
- RS03: <https://www.seeedstudio.com/Robostride-03-Actuator-p-6774.html>
- RS06: <https://www.seeedstudio.com/Robostride-06-Actuator-p-6668.html>
- RS02: <https://www.seeedstudio.com/Robostride-02-Actuator-p-6665.html>
- RS05: <https://www.seeedstudio.com/Robostride-05-Actuator-p-6666.html>
- RS00: <https://www.seeedstudio.com/Robostride-00-Actuator-p-6664.html>
- RobStride USB-CAN debug: <https://www.seeedstudio.com/Robostride-CAN-USB-Driver-Board-p-6708.html>
- RobStride family specification with CNY prices: <https://files.seeedstudio.com/products/RobStride/%E7%81%B5%E8%B6%B3%E6%97%B6%E4%BB%A3%E4%BA%A7%E5%93%81%E8%A7%84%E6%A0%BC%E4%BB%8B%E7%BB%8D%20RobStride%20Product%20Specification%20Document%2020250626.pdf>

## RobStride prices: clarification

The `1199` shown for RS04 in the RobStride specification is in Chinese yuan (`CNY`), not in US dollars. The PDF also lists
RS06 at `849 CNY`, RS05 at `499 CNY` and RS00 at `598 CNY`. For a real order do not automatically use the lowest value seen on
AliExpress: verify SKU, version, accessories, VAT, shipping, customs duty, returns and warranty.

Seeed retail prices verified on 2026-06-02:

| Model | Retail price |
|---|---:|
| RS04 | USD 255, quantity discount USD 242 |
| RS03 | USD 225, quantity discount USD 214 |
| RS06 | USD 210, quantity discount USD 200 |
| RS02 | USD 145, quantity discount USD 138 |
| RS05 | USD 110, quantity discount USD 105 |
| RS00 | USD 125, quantity discount USD 119 |
| Debug USB-CAN | USD 15 |

The BOM uses conservative net EUR estimates, then applies VAT at 22%. Re-evaluate the quotation before ordering.

## Electrical and safety

> **WARNING 2026-07-17: HISTORICAL SECTION.** It describes the 2026-06 bench architecture (SW200/SW80, Eaton timer, key
> selector switch, 48 V coils, KEMET capacitors, RobStride bleeder, ED250, SD-200C/RSD-300C) superseded by the 2026-07-12 lock
> and by the 2026-07-17 hands-on-WEHO decision. The current source is the dated blocks at the top of this file, the
> README and the Excel BOM. Do not order components from this section.

The electrical part is not a decorative list: before the first power-up a 48 V panel must be built and checked.
The BOM now contains a concrete electrical baseline with specific SKUs, fuses and cable cross-sections. It is sized on the
bench source of `62,5 A`; the candidate mobile baseline is now P45B 13S2P with BMS `45 A continuous / 100 A maximum`, with the duration of the maximum still to be
confirmed in writing. Do not add up the
maximum phase currents of the individual RobStride units as if they were all DC currents drawn simultaneously from the pack.

This is a prototype baseline for bring-up and progressive tests, not a machine safety certification. Before
dynamic walking, measure currents, voltage drops and harness temperatures; verify fastener tightness and insulation;
confirm with the pack supplier the prospective short-circuit current, trip thresholds and BMS behavior. The selected BF1 main fuse has
an interrupting rating of `1 kA`: do not declare it sufficient for a pack short circuit without the manufacturer's confirmation.

Power chain, in order:

1. On the bench the `MEAN WELL RSP-3000-48` converts 230 VAC to 48 VDC. It uses L/N/earth terminals, not an IEC C13 socket.
2. On the 48 V positive, place near the source the main fuse `Littelfuse BF1 142.5631.5702`, `70 A 58 VDC
   M5`, in the insulated fuse holder `04980921GXM5`. The main positive and negative trunk is `25 mm2`.
3. The e-stop `Schneider XB5AS8442` and the key selector switch `Schneider XB5AG21` carry only the control circuit. The
   key prevents the mere release of the mushroom button from automatically re-powering the bus. The DC contactor `Albright SW200-20`
   with 48 V coil and blowouts physically opens the motor positive. In mobile use add the manual disconnect switch
   `Albright ED250B-1`, `250 A 96 VDC`, for maintenance and emergency physical disconnection: it does not replace the contactor.
4. Before the contactor closes fully, precharge is needed. The relay `CIT A2K1CSQ48VDC1.6` connects the chassis-mount resistor
   `Vishay Dale RHA050100R0FE02`, `100 ohm 50 W`, in parallel with the SW200. The ON-delay timer `Eaton 262684 / ETR2-11`,
   powered at 48 VDC and set to about `10 s`, then enables the SW200 coil, which bypasses the resistor. With the two
   capacitors already chosen: `C = 24.000 uF`, `Vmax = 54,6 V`, `I0 = 0,546 A`, `P0 = 29,8 W`, `tau = 2,4 s`; after `10 s`
   the bus is at about `98,5%`. Mount the resistor on the metal panel. The TVS `Littelfuse 1.5KE68CA` go directly
   on the terminals of the SW200 and CIT coils.
5. The distribution block `Eaton Bussmann 16220-2` receives positive and negative and splits into six branches: left leg, right
   leg, waist-neck, left arm, right arm and services/Thor DC-DC. The fuse holders must not be left hanging from the cables:
   fix them to the panel under a ventilated insulating cover.
6. Two bulk capacitors `KEMET ALS80A123KE100`, 12000 uF 100 V with screw terminals, go in parallel near the
   distribution, with short runs and ring terminals. They are not left hanging: each uses a `KEMET V4` clamp, a rigid
   panel and a ventilated insulating cover to be designed. The 100 V rating leaves margin over the 54.6 V of the full battery
   and over regenerative transients; they were chosen instead of snap-in types to avoid a power PCB.
7. The `ROBSTRIDE Bleeder Module` limits regenerative overvoltage by dissipating energy when the motors brake.
   The Mean Well bench power supply must not be assumed capable of absorbing regeneration.
8. For mobile use the selected/order-gated candidate is Bicycle Motor Works `13S2P P45B`: 46.8 V nominal, 54.6 V full,
   9 Ah / 421.2 Wh, BMS 45 A continuous / 100 A maximum, 165.1 x 101.6 x 76.2 mm, conservative CAD mass 2.27 kg.
   Do not order it before confirmation of shipping to Italy, exact mass, duration of the maximum, BMS trip, regen and charger.
   Tõuksi Vabrik is the EU fallback at 60 A / 2.04 kg if it guarantees the same envelope by drawing. `ENERprof TN13S5P`
   remains qty 0: 1200 Wh and 5.2 kg are excessive compared with the G1 for the current prototype.
9. Thor must not be connected to the 48 V bus: the `MEAN WELL SD-200C-24` creates the 24 V rail. Thor accepts `9-28 V DC` at the Micro-fit.
10. The two RH56DFX hands use a second converter `MEAN WELL RSD-300C-24`, 24 V / 12.5 A / 300 W, on a dedicated 48 V
    branch with a MINI 10 A fuse. Do not use the 10 A Thor branch for both converters. The split point for the services
    positive/negative must be a properly sized and secured component, not two conductors pushed into the same terminal.

Selected positive segmentation:

| Branch | Fuse | Cable | Note |
|---|---|---|---|
| Main | `BF1 142.5631.5702`, 70 A 58 VDC | `25 mm2` | P45B baseline; re-check coordination with the 45/100 A BMS before mobile use |
| Safety control | `MINI 0997002.WXN`, 2 A 58 VDC | `12 AWG` pigtail of the fuse holder `0FHM0002XP` | e-stop, key, timer and coils |
| Left leg | `BF1 142.5631.5702`, 70 A 58 VDC | `16 mm2` | verify temperature during testing |
| Right leg | `BF1 142.5631.5702`, 70 A 58 VDC | `16 mm2` | verify temperature during testing |
| Waist-neck | `BF1 142.5631.5402`, 40 A 58 VDC | `6 mm2` | active in phase 3 |
| Left arm | `BF1 142.5631.5302`, 30 A 58 VDC | `6 mm2` | active in phase 3 |
| Right arm | `BF1 142.5631.5302`, 30 A 58 VDC | `6 mm2` | active in phase 3 |
| Thor services | `MINI 0997010.WXN`, 10 A 58 VDC | `12 AWG` pigtail | SD-200C-24 only |
| Hand services | `MINI 0997010.WXN`, 10 A 58 VDC | `12 AWG` pigtail | RSD-300C-24 only; services split to be defined |
The sum of the branch fuses can exceed `70 A`: each fuse protects its own cable and isolates the fault of its branch;
it does not constitute a simultaneous power reserve. The overall limit remains the main branch and, in mobile use, the BMS.

Minimal functional diagram of the panel:

```text
BENCH: 230 VAC -> RSP-3000-48 -> main BF1 70 A -----------\
                                                                  +-> protected source node -> SW200-20 -> motor bus
MOBILE: battery -> main BF1 70 A -> ED250B disconnect ---/

protected source node -> MINI 2 A fuse -> e-stop NC -> enable key NO
                                              +-> CIT relay -> 100 ohm resistor -> motor bus
                                              +-> timer Eaton 10 s -> SW200-20 coil

motor bus -> bleeder + two KEMET capacitors + PDU Eaton
PDU -> BF1 70 A left leg / BF1 70 A right leg / BF1 40 A waist-neck
    -> BF1 30 A left arm / BF1 30 A right arm / MINI 10 A Thor services
```

The resistor and the CIT relay form the temporary precharge path in parallel with the SW200: they must not be placed
permanently in series with the motors. Pressing the e-stop drops out both the CIT and the SW200. In mobile use the main fuse
must stay as close as possible to the battery; the ED250B manual disconnect switch comes after the fuse.

The selected power cables are Nautica Illiano `CABATR25/CABATN25`, `CABATR16/CABATN16` and `CABATR06/CABATN06`. The cable lugs
are chosen for flexible conductor and actual hole size: Klauke `704F5`, `704F10`, `703F5`, `101R5`; the crimping tool is
`Klauke K05`, range `6-50 mm2`. The BOM quantities of the cable lugs include two spare pieces for crimping trials.

Main envelope sizes, already recorded in the Excel notes as well, for drawing the panel: RSP-3000-48 `278 x 177,8 x 63,5 mm`
bench only; Eaton PDU `76,2 x 50,8 x 25,4 mm`; KEMET capacitors `diameter 51 x H84 mm` each; RHA050 resistor
`about 50,0 x 21,4 x 16,0 mm`, mounting hole spacing `about 70,6 mm`; Eaton timer `17,5 x 63 x 70 mm`; CIT A2K
`26,5 x 32,0 x 33,5 mm`; Thor DC/DC `215 x 115 x 50 mm`; Jetson AGX Thor dev kit `243,19 x 112,40 x 56,88 mm`,
with T5000 module configurable `40-130 W`.

Important datasheet note for the handover: for the fuse holder `04980921GXM5` there is still in circulation an old PDF from
Littelfuse that states `32 V DC`. The current official Littelfuse page instead identifies the same part as
`MIDI 498-IL Series 58 V In-Line Fuse Holder`, BF1/MIDI M5 compatible. Use as the current source:
<https://www.littelfuse.com/products/fuse-blocks-fuseholders-and-fuse-accessories/automotive-and-commercial-vehicle-fuse-holders/midi-498-il/04980921gxm5.aspx>.

Wiring and CAN:

- RS03 and RS04 use, on the line side, power `AMASS XT30UW-F` and CAN `GH1.25-T`. The BOM contains purchasable SKUs
  `AMASS XT30UW-F.G.Y`, housing `JST GHR-02V-S` and contacts `JST MINI-SSHL-002T-P0.2`; buy a sample and physically
  verify the GH mating before the batch, because non-interchangeable clones exist.
- RS02, RS05 and RS06 use the ready-made Seeed cable `BCCA4011`, XT30 `(2+2)` female-female, 300 mm, with one straight end and
  one at 90 degrees. The old BCCA4009 was removed because the Seeed page returns 404. Verify in the CAD
  the orientation, bend radius and any extensions with strain relief.
- There is no complete purchasable harness for this humanoid: the RS03/RS04 harnesses must be designed and built to
  measure after the CAD. The old generic line "Harness RobStride XT30 + GH1.25 CAN" was misleading and has been deleted.
  For the JST GH micro-contacts, preferably commission the harnesses from a cable assembly shop with pull test and continuity test:
  the official JST crimping tool `YRS-1590` is listed at qty 0 for transparency but costs over EUR 1.500.
- RobStride uses CAN 2.0B at 1 Mbps. Use 120 ohm shielded twisted pair `Belden 9841LSZH`, bus topology and one resistor
  `YAGEO MFR-25FBF52-120R` at only the two physical ends of each bus.
- The Thor Dev Kit exposes two CANH/CANL buses on connector J47: no external SN65HVD230 transceivers are needed on the kit. The harness for
  J47 and the Thor Micro-fit cable remain qty 0 until the mating connector and pinout are verified on the physical kit.
- [CORRECTION 2026-07-17: this line is SUPERSEDED. Use exactly `MKS CANable Pro / CANable-MKS 1.0` with
  STM32F072 (candleLight/gs_usb); NOT the "V2.0" STM32G431, not supported by the upstream candleLight firmware —
  see the ELECTRONICS 2026-07-12 note at the top of the file.] Old text: for the additional upper-body buses use
  `MKS Makerbase CANable Pro V2.0`: isolated, available and compatible with
  `candleLight / SocketCAN`. It replaces the CANable OpenLight, which cannot be ordered from the unreachable official site.

### Control architecture: Thor-only baseline, optional low-level controller

The RobStride units already contain the local actuator loops: the on-board computer does not have to directly implement the
motor current control. It must read feedback and IMU, run the policy or the joint control and send
periodic setpoints over CAN with limits, heartbeat and watchdog.

To reduce components, the initial baseline uses only `NVIDIA Jetson AGX Thor`: isolated realtime process, direct
SocketCAN, realtime priority, dedicated CPU cores and hardware safety independent of the software. Thor has two native
CAN controllers and NVIDIA provides a realtime kernel for Jetson Thor, but in the current documentation RT support is
listed as Developer Preview. So do not assume that Linux execution shared with AI, cameras and logging is
automatically deterministic.

A separate low-level computer is not mandatory for the first prototype and is present in the BOM as `OPZIONE qty0`.
It becomes advisable if the Thor-only tests show jitter, unacceptable latencies, bus saturation, dependence on
USB-CAN interfaces that are not robust enough, or if one wants to keep damping/watchdog and actuator management isolated from
crashes, reboots or updates of the AI software. Do not choose Raspberry Pi, MCU or SBC yet: first measure loop
frequency, latency and jitter with all 31 axes and define the number of buses, IMU, I/O and safety strategy.

"1 or 2 computers?" ISSUE RESOLVED 2026-06-14 (after ToddlerBot, Stanford CoRL 2025, arXiv 2502.00893). ToddlerBot is an
open-source 30 DoF humanoid with ONLY ONE computer (Jetson Orin NX, 2.5 TFLOPS) that runs locomotion AND manipulation/vision
with "concurrent policy inferences" on the same CUDA accelerator: NOT two computers. The low-level is done by the actuators
(Dynamixel smart-servos with the internal loop) just as in our case by the RobStride (internal FOC + CAN); on board there is only Orin NX + a
"comm board" (bus interface, NOT a second brain) + IMU/power. LESSON: the real axis is not "locomotion computer
vs manipulation computer" (loco-RL and manip-VLA are two networks that run together on 1 GPU), but high-level BRAIN
(perception + RL loco + VLA manip, 10-200 Hz) vs low-level real-time LOOP (~1 kHz joints + safety). That low-level can
sit on the SAME Thor as an isolated RT process, or on a small dedicated co-controller (= our OPTION qty0),
but it is NOT a second AI computer. "Maximum quality" DECISION: ONE single Thor as brain (runs loco+manip+vision with
huge margin: Thor >> Orin NX, and if a 2.5 TFLOPS Orin NX is enough for ToddlerBot, Thor fits with very ample room); NO
second computer for manipulation; the RT/safety co-controller remains an option to be activated only upon measurement on real HW.
Caveat: ToddlerBot is small/slow (3.4 kg, position servos) -> lighter RT requirements than a dynamic G1 clone,
so the jitter risk on the RT loop must be measured anyway. For the VIRTUAL PROTOTYPE it is irrelevant: in sim the on-board
compute does not matter, put in 1 Thor and do not let the CAD be conditioned by its size. (Supersedes the push by the other AI session to remove
the Thor: under "maximum quality" the single Thor is kept as the only brain and future on-board VLA.)

NVIDIA sources:

- CAN Jetson: <https://docs.nvidia.com/jetson/archives/r38.2.1/DeveloperGuide/HR/ControllerAreaNetworkCan.html>
- Thor layout and Micro-fit input: <https://docs.nvidia.com/jetson/agx-thor-devkit-4fed1671/user-guide/latest/hardware_layout.html>

## Changes made in this session

- Unified the motors on RobStride; removed Damiao and CubeMars from the selection.
- Corrected the G1 baseline by switching to the current official model `g1_29dof_mode_11`.
- Corrected the mechanical interpretation of the waist: RS04 vertical yaw + RS03 x2 on pushrods for pitch/roll.
- Restored waist gimbal (cardan), two M10 pushrods and shared pin on the torso side in the BOM.
- Restored the 7 DOF per arm of the G1 29 DOF variant.
- Chose RS05 x2 for neck pan/tilt using the official G1-Comp page as reference; neck torque to be validated.
- Differentiated the arm ladder to reduce distal mass: RS03 shoulder pitch/roll, RS06 shoulder yaw and elbow,
  RS02 wrist roll, RS05 wrist pitch/yaw. RS06 wrist roll remains a qty 0 alternative.
- Made all Excel motor rows uniform: dimensions, weight, RobStride rated/peak torque and G1 reference mandatory.
- Corrected the Excel formatting: the light grey applies only to rows with a numeric quantity of zero, not to the blue titles.
- Removed the premature assumptions `6001-2RS` and `6801-2RS` for the ankle joint: supports, retainers and pin lengths remain
  qty 0 until the CAD.
- Moved the safety chain to phase 1 bench.
- Removed CubeMars RUBIK LINK and external Thor transceivers; added RobStride USB-CAN debugger.
- Closed a purchasable electrical baseline: trunk `25 mm2`, main fuse BF1 `125 A`, safety control `2 A`,
  leg branches `70 A / 16 mm2`, waist-neck `40 A / 6 mm2`, arms `30 A / 6 mm2`, Thor services `10 A`; added
  specific 58 VDC fuse holders.
- Sized the precharge on the two KEMET capacitors: Vishay `100 ohm 50 W`, CIT 48 V relay, Eaton ON-delay timer
  set to about 10 s, Schneider key selector switch and coil TVS. Added manual battery disconnect switch ED250B-1.
- Eliminated generic 12 AWG cable and generic XT90: added Nautica Illiano cables by cross-section, Klauke cable lugs for the actual
  hole and K05 crimping tool. The ENERprof pluggable connector remains qty 0 until the manufacturer confirms the mating part.
- Eliminated the fake complete harnesses: added Seeed BCCA4011 cables, XT30UW-F connectors, JST GH housings/terminals,
  Belden CAN cable and YAGEO terminators; custom harness and J47 remain qty 0.
- Audited the selected links: corrected the old removed Seeed BCCA4009 cable, the withdrawn ENERprof charger and the
  unreachable CANable OpenLight. The new charger remains a qty 0 candidate until ENERprof approves the interface.
- Replaced the generic Danenergy battery with the direct link to the selected ENERprof pack; added alternative
  Dan-Tech Energy softpack qty 0 with mandatory note Smart BMS + AS150U.
- Removed the links to RS categories from the purchasable rows and made `umanoide` the active sheet when Excel opens.
- Reaffirmed that Unitree G1 is the only baseline: K-Bot remains only a secondary open hardware note for packaging and
  wiring, it must not be used to size geometries, ankle or motors.
- Clarified the ankle: the two orthogonal 12 mm diameter pins per ankle are exclusively rotation axes of the
  foot-shin joint; the transverse 8 mm diameter pin instead receives the two heads of the M8 pushrods. Six pushrods
  in total remain selected, four M8 at the ankles and two M10 at the waist.
- Added `qty 0` examples of standard SKF and igus Q2 plain bushings and three custom specimens printed in iglidur `i150`,
  `i190` and `J260-PF`; the final choice remains subject to CAD and tests on the real pin.
- Clarified the structure of the ankle supports: 12 mm diameter pin fixed in the lugs, radial support in the moving central
  piece, dedicated axial thrust washer adjusted per side, flanged metal insert fixed in the lugs as a
  replaceable counterface. Added `qty 0` alternatives igus `Q2FM`, `GTM`, SKF `HK`, `NKI`, `AXK`, `AS`, shim
  DIN 988 and Elesa+Ganter family `DIN 172`; do not activate any variant before the CAD dimensions.
- Documented the first clamping stack for the simple variant `NKI 12/16`: wide washers, integrated shoulders
  of the lugs that clamp only the inner ring, moving part excluded from the compression and RS PRO shoulder bolt
  `292-417` `12 x 60 mm` as preliminary `qty 0` reference. Recovered in the BOM the catalogues for pins and retainers.
- 2026-06-03: closed the ankle FINAL DECISION (see dedicated block in "Legs, phase 1"). Plain-bearing architecture, the
  simplest: ISO 7379 shoulder screw `Ø12-M10` as pin/race (integral with the lugs via axial clamping, not
  press fit), two igus `GFM-1214` flanged bushings pressed into the moving piece with the flange taking the axial load (eliminated
  separate thrust washers, sleeve/column and thrust bearing), M10 nut + wide washer. Flanged metal bush in the lug
  (`DIN 172-B12-20`) made OPTIONAL as an anti-wear upgrade if the igus flange wears the PA-CF. NKI 12/16 and
  sleeve/column archived as alternatives. Added multiple verified suppliers. PRIMARY bushing = PRINTED
  multi-material J260+PA-CF integral with the moving piece (filament already purchased), `GFM-1214` purchased as fallback;
  axial starting point with PA-CF shoulder of the lugs that slides on the printed igus flange. Aligned the ankle BOM
  rows (tags SCELTO/PRIMARIO/FALLBACK/ARCHIVIATO/OPZIONALE) and regenerated the Excel. Section drawings no longer maintained.
- 2026-06-04: waist yaw downgraded from RS04 to RS03 (user choice) -> BOM 8 RS04 + 7 RS03, total EUR 16.228,27, mass
  40,355 kg. Added "CAD 3D" column with the Seeed links (downloadable STEP) for each motor. Extracted and logged the exact
  positions of the 29 G1 joints from the URDF (`g1_joints.csv` + `g1_29dof_mode_11.urdf` in the workspace). Documented the RobStride vs Unitree
  torque density issue: leg motors (RS04 vs RS06) to be decided with the user depending on the ambition.
- 2026-06-05: added and then corrected the Onshape skeleton rule. The `G1 joints CAD` sheet contains `exact_*`, `cad_*`
  and `pose_down_*`: `cad_x` is brought to zero, `cad_y` is aligned in the vertical chains to `hip_roll` for the leg
  and `shoulder_yaw` for the arm, `cad_z` remains the G1 dimension. The rotation axes are not simplified. `pose_down_*`
  remains only a visual aid for arms along the body. The dash `-` means "same as the reference", not zero.
- 2026-06-05: the workbook was cleaned of useless tabs. The generator now intentionally deletes `ARTES4.0@Olbia_`,
  `Speso-Impegnato`, `pivot-finali`, `Acquisti` and `Budget`; `umanoide` is inserted after `ARTES4.0@Olbia_NoIVA` and
  `G1 joints CAD` right after `umanoide`.
- 2026-06-05 (AI): consolidation of the backlog of several rounds.
  (1) ARM MOTORS: wrist now 3 UNIFORM axes RS02 (was roll RS02 + pitch/yaw RS05; Unitree makes the wrist uniform).
  Shoulder yaw remains RS06 (lighter than the pitch/roll RS03, reduced distal mass). BOM = 8 RS04, 8 RS06, 7 RS03, 6 RS02,
  2 RS05 = 31 axes; total EUR 16.399,07; mass 41,211 kg. Grey reserves [SECONDA SCELTA qty0]: RS03 uniform shoulder-yaw,
  RS06 powerful wrist, RS05 light wrist pitch/yaw.
  (2) SIMPLIFIED AXES: added column `axis_cad_semplif` to the `G1 joints CAD` sheet (hip_roll->X, hip_yaw->Z,
  shoulder_pitch->Y, rest principal) at the user's request. CAD skeleton = `cad_*` positions + `axis_cad_semplif` axes
  (consistent, orthogonal). Supersedes the earlier AI note "axes not simplified".
  (3) G1 VERIFICATION (5-agent workflow): positions/axes/mass SOLID, triple-confirmed (<0,1 mm; total mass 33,340 kg;
  thigh 336,6 / shin 317,6 / leg 654,2 mm; hip cant 10,021 deg). Torques: they match the `mode_11` file but DIVERGE
  from the public URDF `unitree_rl_gym` on 3 joints: hip pitch/roll mode_11=139 vs rl_gym=88; ankle 35 vs 50; waist roll/pitch
  35 vs 50. Knee 139 in both. wrist pitch/yaw=5 confirmed (the "8" found by the user was wrong). To size the
  motors use the HIGHEST value (139 hip/knee, 50 ankle/waist) with margin. True bottleneck = KNEE (139,
  RS04 14% below). Ankle 2xRS06 confirmed correct (real ~50, not 35). The positions are identical between the two releases.
  (4) COMPUTE: recommended G1-style architecture = small real-time controller (uC or RT-Linux SBC) for policy + CAN loop
  + safety, PLUS AI computer (Orin NX class, NOT Thor) added LATER for vision. The RL policy for walking is tiny:
  Thor is not needed for the bring-up. Reconsider/remove Thor from the baseline; do not let the CAD be conditioned by its size.
  (5) POSE and LIMITS: draw and assemble with ARMS ALONG THE BODY (home); the pose is only the default config in sim, it is not
  engraved in the geometry (link lengths pose-independent). Joint limits = SOFTWARE, derived from one's own CAD
  (self-collision by rotating the joints in the assembly + cable wrap for the yaws), not copied from the G1. Physical stops only
  where critical for safety. Motor CAD: downloadable from the Seeed pages ("CAD 3D" column in the BOM) or AIFITLAB (STEP per model).
- 2026-06-05 (AI): leg hip yaw downgraded from RS04 to RS03 (user choice: in CAD the RS04 turn out to be too
  big/heavy). Pitch, roll and knee remain RS04 — roll is the axis of lateral balance (critical) and the robot
  at 41 kg is heavier than the G1 (33 kg), so it is not downgraded. BOM now: 6 RS04 + 9 RS03 + 8 RS06 + 6 RS02 + 2 RS05 = 31
  axes; total EUR 16.330,75; mass 40,131 kg (-1,08 kg). Hip yaw RS03 = 60 Nm peak vs G1 88: acceptable because yaw
  is the least loaded hip axis (does not fight gravity, low real demand).
- 2026-06-05 (AI): shoulder pitch/roll downgraded from RS03 to RS06 (shoulder now all uniform RS06), VERIFIED by calculation
  (not only G1): arm 3.26 kg, CoM 0.236 m -> static 7.5 Nm, peak on a fast gesture ~22 Nm. RS06 (36/11) covers with 1.6x
  on the peak and holds the outstretched arm continuously (7.5 < 11 nom); RS02 too weak (does not hold the outstretched arm, heats up); RS03 was
  2.7x = oversized. BOM now: 6 RS04 + 5 RS03 + 12 RS06 + 6 RS02 + 2 RS05 = 31 axes; total EUR 16.296,59; mass
  39,095 kg. WAIST instead NOT reduced (verified by calculation): it carries the whole upper body ~15-20 kg; pitch/roll ~32-64 Nm
  at the JOINT (gravity + dynamic, depending on torso inclination and battery position) and they pass through the 2 pushrods (motor torque
  != joint torque, lever geometry from the CAD is needed) -> remains RS03, not to be touched. Waist yaw ~9-31 Nm (inertial only): in
  theory RS06 but margin too thin (single motor, balance role) -> kept RS03, review after CAD + battery.
- 2026-06-05 (AI): shoulder yaw downgraded from RS06 to RS02, verified with the PAYLOAD in the real posture. User
  clarification: the load is held with the arm BENT (humerus vertical, forearm at 90 degrees), not outstretched. Consequences by
  calculation: (a) the shoulder yaw has the axis of the humerus vertical -> gravity 0, inertia only -> ~4-11 Nm even with 3 kg in hand ->
  RS02 (17 peak) is enough with margin; (b) shoulder pitch/roll and elbow hold the load at the lever of the FOREARM ~0.20 m
  (not 0.37 m of outstretched arm) -> RS06 holds ~4.3 kg with bent arm, so RS03 on the shoulder is NOT needed (remains RS06) and
  the elbow RS06 is fine as it is. The arm carries ~4 kg in load posture. BOM: 6 RS04 + 5 RS03 + 10 RS06 + 8 RS02 + 2 RS05
  = 31 axes; total EUR 16.137,99; mass 38,663 kg [snapshot 06-05, SUPERSEDED as of 2026-06-08, see below]. The reductions
  verified by calculation (shoulder pitch/roll, hip yaw, shoulder yaw) removed ~2,5 kg while staying above the real requirements.
- Set Thor-only as the initial baseline; the separate low-level computer remains a `qty 0` option to be activated only
  if measurements show jitter, insufficient buses or the need for isolation from crashes of the AI software.
- Consolidated the documentation into this single file; `STATO.md` deleted.
- 2026-06-08 (AI): complete motor review with the REAL RobStride specifications (table verified via Seeed/AIFITLAB/
  OpenELAB). Wrist 3 axes RS02->RS00 (dual encoder, 57 mm, 5 nom/14 peak, holds 2 kg in hand). Shoulder yaw RS02->RS00.
  Shoulder pitch/roll RS06->RS02 and elbow RS06->RS02 -- NOT RS01: found that RS01 has a SINGLE encoder (36V only, no IP),
  RS02 has DUAL encoder (output-side feedback, needed for RL/manipulation); RS01 discarded everywhere. Leg hip yaw RS03->RS06;
  waist yaw and waist pitch/roll RS03->RS06 (vertical axes / low dynamic demand, non-acrobatic robot, verif ~28 Nm <
  36 peak). Ankle remains 2x RS06: user correction -> ankle and waist pitch/roll are LINKAGES, the joint torque is
  fixed by the load but the motor torque depends on the crank ratio (in CAD); RS06 = safe ceiling. BOM now: 6 RS04 + 9 RS06
  + 6 RS02 + 8 RS00 + 2 RS05 = 31 axes (all RS03 and RS01 gone from the active ones). Total EUR 15.434,05; mass 35,312 kg
  (-3,35 kg on the motors vs 06-05). py source + MEMORY updated; Excel regenerated and CONFIRMED: complete 15.434,05,
  Phase1 10.519,00, Phase2 1.465,45, Phase3 3.449,60, mass 35,312 kg, 31 motors (RS00x8, RS02x6, RS04x6, RS05x2, RS06x9).
- 2026-06-08 (AI): complete TORQUE VERIFICATION post-downsizing (method + numbers in the dedicated section above). Outcome:
  no motor rejected for non-acrobatic use; RS04 legs (not downgraded) hold standing and walking. 3 recoverable
  WARNINGS: knee (no held deep squat, it is the max motor), waist pitch (low battery + linkage),
  elbow (<=1.5 kg comfortable / 2 kg only at moderate speed). 2 CAD checks: ankle and waist crank ratio >=1:1.
  Wrote the calculation METHOD (static g*Sum(m*b), dynamic I*alpha bang-bang, yaw=inertia only, linkages) + inputs
  (motor masses as lever arms, G1 joint positions, outstretched arm) so the other AI session can redo the calculations.
- 2026-06-09 (two AI sessions): cross-check by the other AI session on the SHOULDER -> the other AI session is right, the AI's number was optimistic. The AI's error:
  it had used hand 0,30 kg; in reality it is 0,50 kg with the CoM beyond the wrist (~0,48 m). Corrected: arm OUTSTRETCHED horizontal
  ~7,8-8,6 Nm > 6 rated -> RS02 does NOT hold the outstretched arm CONTINUOUSLY (ok only a few s below the 17 peak); 2 kg at
  full reach exceeds even the peak. With BENT elbow instead ok (~2,6 without payload / ~6,9 with 2 kg). The other AI session also
  raised the real MASS: it uses ~46 kg (PA-CF frame ~10 kg included), this AI session had verified at 35 (without frame). At 46 kg
  the RS04 LEGS (already the max) go ABOVE the rated value while walking (~45 vs 40) -> the lever is the MASS, not the motor.
  Conclusions: keep arms light (no shoulder upsize, it would make the legs worse) + CONTROL the mass (frame target
  ~6 kg, robot ~40 kg). Open decisions: role of the arm (bent only vs holding outstretched) and frame mass target.
- 2026-06-09 (user) [SUPERSEDED in part 2026-06-27: ankle and waist have new active hardware]: pushrod hardware swap. Ankle AND waist pushrods -> ALUMINIUM M8 rod-ends adjustable in various
  lengths (AliExpress 1005008935554718), on Ø8xM6 pins. BLACK AliExpress shoulder screws (set of all sizes,
  1005007481484485) used for EVERYTHING: Ø12xM10 for the rotation axes (ankle + waist gimbal), Ø8xM6 for the pins where
  the pushrods push (ankle + waist). RS PRO 292-417 demoted to alternative. Lengths at CAD. Regen: complete
  15.425,51 EUR, mass 35,012 kg.
- 2026-06-09 (user) [SUPERSEDED in part 2026-06-27: current = Ø8/M6 x45 ankle gimbal, KARM right qty2 + KALM left qty2, no waist gimbal]: defined the joint ASSEMBLY. ANKLE (pitch+roll) = cross-shaped 3D printed central piece with integral
  igus (cylindrical pitch hole at the top, perpendicular roll hole at the bottom), 2 Ø12xM10 shoulder screws as axes +
  black M10 nuts that clamp the lugs; central piece with slight play. igus fallback: separately printed flanged
  cylinders -> purchased flanged igus bushings. Foot PUSHROD PIN = transverse Ø8xM6 shoulder screw + 1 black M6 nut,
  2 rod-end heads of the pushrods + 3D printed central part. Black nylock nuts added to the BOM (Amazon B0C8ZCR6B1, set
  M3-M16): M6 (pushrod pins) and M10 (ankle+waist axes). CRITICAL NOTE (AI): the rod-ends must remain FREE to
  oscillate (the ankle does 2 DOF, roll requires the spherical joint) -> the Ø8 shoulder must BOTTOM OUT so that the nut
  preloads on metal and does NOT crush the balls; the printed central part acts only as a spacer (the shoulder carries the
  load, so it does not creep). Alu OD13 spacers discarded: OD too large, they would touch the rod-end body.
- 2026-06-09 (AI+user): parallel ankle KINEMATICS. G1 (from URDF): pitch -50/+30 = 80 deg, ROLL only +/-15 = 30
  deg. Rod-end: the PITCH (80 deg) uses the UNLIMITED rotation around the pin (pins along the pitch/transverse axis) ->
  zero misalignment; the ROLL (+/-15) uses the TILT of the ball, LIMITED. Required tilt ~ order of the roll angle
  but REDUCIBLE with geometry (LONG pushrods + attachment close to the plane of the roll axis). Cheap rod-ends ~+/-12-16 deg
  -> marginal at +/-15; use high-misalignment (+/-20-25) or verify the real tilt in CAD. LEVERS: roll = small motion,
  pushrod stays ~perpendicular -> ratio ~CONSTANT, design crank=foot for 1:1; pitch = large motion, sweep ->
  ratio VARIES (nonlinear ~1.5-2x), size for the worst case. CRANK/motor horn = MOST LOADED part
  (~1+ kN rod force at short lever): make it STOCKY or in METAL, not thin printed. Stacked motors (one up/one down) ->
  rods of different lengths + pitch/roll coupling (non-diagonal matrix); side-by-side same height = cleaner.
- 2026-06-09 (AI): WHAT IS IN THE URDF for the pushrod joints. The URDF is a serial TREE: the ankle is 2 VIRTUAL
  revolute joints (ankle_pitch + ankle_roll, effort 35 Nm each), the waist 3 (yaw 88, roll 35, pitch 35). There are NO
  motor positions, rods, cranks, nor mimic/transmission/loop (verified with grep). The sim does NOT simulate the transmission: it moves
  ideal joints, the RL commands torques at the virtual JOINTS; the motor masses are included in the inertia of the parent link
  (shin), not as separate bodies. The joint-torque -> motor-torque map (Jacobian of the linkage) lives in the
  robot CONTROLLER, NOT in the URDF. Consequence: the G1 lever arms CANNOT be derived from the URDF. Useful distinction:
  DIRECT joints (hip/knee/yaw/shoulders/elbow) -> URDF effort = MOTOR torque (usable directly); LINKAGE joints
  (ankle, waist roll/pitch) -> URDF effort = JOINT torque, the motor torque = joint/ratio, ratio = your choice.
  The linkage is sized to deliver the JOINT torque from one's own motors: ankle target ~46 Nm (robot 46 kg, more
  than the G1 33 kg which asks for 35!), 2x RS06 = 72 Nm at 1:1 -> covered with margin. Do NOT copy the 35 of the G1 (it is lighter).
- 2026-06-09 (user): BOM organization. (1) Row text color AUTOMATIC: BLACK if qty>0 or tag [SCELTO];
  GREY (A6A6A6) if alternative/catalog/archived at qty0. No bold. Logic in build_umanoide_tab.py
  (is_active = unita>0 or "[SCELTO" in nome). (2) ALL the mechanical hardware of the joints (pins, shoulder screws,
  nuts, rod-ends, bearings) lives in section "1 - PROTOTIPIA MECCANICA", including that of the WAIST (moved from 2b);
  the motor sections contain ONLY motors. The waist hardware keeps fase=Fase 3 (correct cost), only
  the visual position changes. Totals unchanged 15.425,51 EUR / 35,012 kg.
- 2026-06-11 (AI+user): STUDY of other robots + premium motors (budget potentially relaxed, "maximum quality",
  will make a virtual prototype). ARCHITECTURE: (a) WAIST -> [SUPERSEDED on 2026-06-14: the R1 in series was DISCARDED for
  geometry, we stay on the G1 PUSHRODS yaw+pitch+roll; see bullet 2026-06-14] the hypothesis was the UNITREE R1 scheme = yaw +
  roll (NO pitch), 2 direct motors. R1 confirmed yaw +-150 / roll +-30. Tesla: ~2 DOF torso, axes not public (the AI
  had gone out on a limb saying 'yaw only', retracted). Figure: no torso pitch (patent WO2025213141A1), it HAS
  leg-twist/hip-yaw canted low down (it does NOT remove the hip yaw). Asimov (35kg twin, github asimovinc/asimov-1): 6
  DOF/leg WITH hip yaw, waist yaw only.
  -> CONCLUSION: KEEP hip yaw (everyone has it), waist = direct SERIAL yaw+roll (see 2026-06-16, the waist pushrods SUPERSEDED), hip pitch OUTSIDE (G1/R1) not inside (Figure) because
  the big QDDs (Ø88-107) collide in the groin and block adduction. (b) Premium MOTORS: CubeMars AKE90-8 (170 Nm,
  1.4 kg, 9 arcmin, ~$484 bare) beats the G1 on the legs (goodbye to the 0.86x). BUT the WEIGHT is cut by ENCOS, not CubeMars:
  Encos EC-A4310-P2-36 = 36 Nm in 377 g vs RS06 621 g -> -244 g/motor. CubeMars more AVAILABLE (retail) and
  cheaper, Encos LIGHTER but by quotation (Foxtech). Specs: AKE80-8 30Nm/570g/Ø87x32/$340; AK10-9 53Nm/dual
  enc/$699; Encos A10020 150Nm/1.35kg/$2250, A13715 320Nm/$2250. Encos/CubeMars > RobStride in density but RobStride
  remains the lightest BELOW ~20 Nm (RS00 310g, RS05 191g) -> on the small ones RobStride is kept even in the premium option.
  Created 2nd Excel sheet "MOTORI premium" (optimal mix: AKE90-8 legs + Encos A4310 on the 36Nm + small RobStride):
  16.14 kg vs 18.21 RobStride = -2.07 kg (ALL from Encos), ~$8504 + 1824 EUR (30 axes, serial waist, RS00 arm).
  It sits alongside the RobStride BOM, it does not replace it.
- 2026-06-16 (AI+user): LOWER-BODY LOCKED for the CAD, after study of Tien Kung 2.0/3.0, Unitree H2, ToddlerBot.
  (a) WAIST = DIRECT SERIAL yaw(bottom) + roll(top above the yaw, X axis), NO pitch, NO pushrods. SUPERSEDES the
  pushrods of 2026-06-14. Reason: RL-FRIENDLY (Unitree itself moved from the G1 pushrods to serial Z-Y-X on the H2,
  "more RL-friendly"; we do RL in Isaac Lab; parallel mechanisms = closed chain + rod-end play = sim-to-real
  gap). 2 DOF stack ~130-150 mm accepted (Tien Kung 3.0 does it). Torso pitch is done by the HIPS. -1 RS06 ->
  30 motors. Totals (after RS02->RS00 point d AND ankle->RS00 point e): complete 14.594,69 EUR (Fase1 10.113,96 /
  Fase3 3.015,28), mass 32,227 kg, lineup RS00x18 / RS04x6 / RS05x2 / RS06x4 (RS06 only hip-yaw+waist; RS02 ELIMINATED).
  (b) HIP = orthogonal F-A-R (Flexion-Abduction-Rotation, like H2), pitch in the PELVIS towards the OUTSIDE (G1/R1), clean
  orthogonal axes, NO canting. User idea "60° star" (canting the leg pitches) evaluated in depth and discarded BUT
  with honesty: if you cant BOTH axes the two motors ADD UP on pure pitch (DIAMOND-shaped torque region: pure pitch
  up to 2*tau*cos(phi), e.g. 208 Nm at 30deg, > orthogonal; but the combined pitch+roll falls inside the diamond, worse than the
  orthogonal square). The sizing case = stance leg = pitch+roll TOGETHER -> orthogonal wins. And we
  are torque-starved (RS04 0.86x), we cannot gamble; the H2 cants because it has 360 Nm of surplus, we do not. To
  kill the bottleneck of the 139 the clean way = bigger motor (AKE90-8 170 Nm), not canting. TO BE
  VALIDATED in sim: log the torque trajectory (pitch,roll) at the hip; if the gaits turn out pitch-dominant, the
  canting question reopens. For now orthogonal CAD (reversible: only the orientation of the motor seats changes).
  (c) ANKLE = PARALLEL, motors IN THE SHIN. Motor = RS00 at reduction ~2:1 [UPDATED 2026-06-16, see point e:
  earlier the AI had put RS06 1:1 "for the power", but the REQUIREMENT is only WALKING + 1 kg/arm, NO jumps/running ->
  modest ankle power, RS00 is enough; the RS06 Ø88 stacked below the knee reached almost to the ground]. Strong
  precedent: RoboEra ~70 kg uses small motors with reduction ~2:1 roll / ~1.5:1 pitch and it JUMPS. At ~2:1 the 2 RS00 add up:
  2x14x2=56 Nm peak (ok 33-40 kg; at 46 kg ~2.5:1->70). RS06 1:1 remains alt qty0 IF dynamic gaits/jumps are needed. Motor
  axis along X (G1 style), user choice. Rod-end: with the SPHERICAL ones already chosen (igubal ±35°) it is enough to orient the pin so that the
  large PITCH = FREE rotation about the pin (unlimited) and the small ROLL (±15°) = tilt within ±35°. Do NOT make
  pure revolute-revolute heads (it binds = spatial overconstraint); safe recipe = RSU (Revolute-Spherical-Universal,
  like the IIT paper), keep at least one spherical/universal joint. Pushrod length locking: thin jam nut
  (half thickness M8 ~4 mm) + Loctite 243; if space is lacking, tune with the adjustable one then REPLACE it with a FIXED rod
  cut to length (stiffer, less play -> better sim-to-real). Hybrid "direct roll in the foot" = Plan B only if
  the sim-to-real of the parallel 2-DOF turns out to be a nightmare (and in that case roll with a light Encos 377 g motor).
  (d) RS02 ELIMINATED from the whole BOM (user choice 2026-06-16). User insight (CORRECT): in the RobStride range the RS02
  is DOMINATED. Dimensions: RS00 Ø57 / 5 rated-14 peak / 310 g; RS02 Ø78.5 / 6 rated-17 peak / 405 g; RS06 Ø88 / 11 rated-36
  peak / 621 g. From RS00->RS02 you pay +21.5 mm of Ø for only +3 Nm peak; from RS02->RS06 you pay only +9.5 mm for +19 Nm
  (2x). So RS02 is almost as big as RS06 but with half the torque: RULE = "if RS00 is enough use RS00 (much
  smaller), otherwise jump to RS06; never RS02". Applied: ARM all RS00 (shoulder pitch/roll + elbow downgraded from RS02;
  shoulder yaw + wrist already RS00). Tien Kung (70 kg) has motors ~Ø60 = the SIZE of an RS00 but they are DENSE ENCOS (~36 Nm), NOT
  an RS00 (14 Nm): size != torque. ANKLE: RS00 NO (POWER joint) -> stays RS06 at 1:1 (torque multiplies
  with the reduction, POWER does not: a small motor + reduction gives a lot of torque but at low speed, and at toe-off
  torque AND speed are needed together = power, which only a physically larger motor -RS06- or a dense one -Encos- has). For
  a compact AND powerful ankle = Encos A4310 premium (the Tien Kung way). Shoulder with RS00 OK: it is a SLOW joint, only
  the torque matters, and RS00 (14 peak) covers the dynamic ~12; the continuous horizontal hold was not achieved even by the RS02
  (6<6.8 rated). Elbow: RS00 ~1.2 kg continuous / 2 kg peak (slightly less than the RS02); RS06 only if 2 kg continuous is needed.
  Final lineup: see point (e).
  (e) ANKLE -> RS00 at ~2:1 + ENCOS CATALOG + MIXING (2026-06-16). REQUIREMENT confirmed by the user: normal walking
  + standing stably + 1 kg per arm, NO jumps/running. With this the ankle is NOT a high-power
  joint -> RS00 at reduction ~2:1 is enough (see point c). FINAL LINEUP: RS00x18 (arm 14 + ankle 4) / RS04x6
  (legs) / RS05x2 (neck) / RS06x4 (ONLY hip-yaw 2 + waist 2). 30 motors, 32,227 kg, 14.594,69 EUR.
  ENCOS CATALOG combed through (Foxtech): the smallest is the EC-A4310-P2-36 (36 Nm, 377 g, ~Ø60, frame Ø43). Below
  43 mm Encos has NOTHING -> for wrist/arm (5-14 Nm) no Encos: the A4310 would be overkill, heavier
  than the RS00 (377 vs 310 g) and ~6x the price. The other Encos are all BIGGER: A6408 (Ø64), A8112 (Ø81, ~94 Nm,
  830 g), A10020 (Ø100, ~150 Nm), A13715/A13720 (Ø137, ~320 Nm). So the ONLY useful Encos = A4310, and only where there is
  the RS06 (hip-yaw/waist) or for a DYNAMIC ankle. CASCADE: with "walking only" the ankle goes to RS00 (310 g,
  lighter AND cheaper than the A4310 377 g/$700) -> the Encos loses its best application (the distal mass of the
  ankle). What remains is hip-yaw+waist (4 motors): -244 g x4 = ~1 kg, but ~$2800 + 3rd brand. So for OUR use the
  Encos premium option is of little interest. MIXING Encos+RobStride: FEASIBLE (both CAN), but non-zero SOFTWARE cost =
  2 protocol drivers + 2 actuator models in sim + 2 calibrations + different connectors; ~FREE in sim (different
  parameters per joint are enough), it weighs only on the real HW. "All the same" is clearly simpler for build and
  sim-to-real (1 driver, 1 model, uniform spares). Conclusion: all RobStride (RS00/04/05/06) -> no mixing,
  problem avoided. Premium sheet: added DIMENSIONS column for all motors (user request).
- 2026-06-14 (AI+user) [SUPERSEDED on 2026-06-16: waist now direct SERIAL, NO longer pushrods - see bullet below]: WAIST - R1 in series EVALUATED and DISCARDED, we stay on the PUSHRODS (G1 scheme). Geometric
  reason (real numbers from the BOM): the waist roll is an RS06 Ø88; in series roll-below-yaw the Ø88 DIAMETER eats
  height -> torso/yaw base at ~190 mm above the hip axis = torso cut short for battery+compute. R1 can afford it only
  because it has tiny motors, we do not. Also discarded the Figure-style "bomb at the back" (it lowers the yaw but gives only
  ROLL, no pitch, and the cantilevered bracket carries the whole bending moment of the torso). PUSHRODS = right choice for
  large motors: same logic as the ankle (heavy motors LOW in the pelvis, transverse axis, zero vertical
  stack, mass down for CoM) and in addition the torso PITCH is regained (bending over/picking up from the ground; R1 does not
  have it). Cost: waist stays at 3 motors (yaw + 2 pushrods), 31 axes total, 35,012 kg. BOM and premium sheet already
  re-aligned to the pushrods. NB: also confirmed hip pitch in the pelvis towards the OUTSIDE (G1/R1 scheme, not Figure).
- 2026-06-10 (AI+user): ankle rod-end MISALIGNMENT BUDGET (from photos of X-Humanoid joints ~±45° and RobotEra ~±30°,
  which however use automotive BALL-STUDS, not rod-ends). Physics: the foot pin ROLLS with the foot -> the tilt required of the
  FOOT-SIDE eyes is ~1:1 with the roll (+~3 margin); the pitch costs 0 (rotation about the pin); the upper eyes
  (crank arm) ~0-2. CORRECTION: long pushrods remove only the out-of-plane part (~1-2 deg), not the main
  component. Cheap AliExpress rod-ends: typical tilt ±12-15 (MEASURE on arrival with an inclinometer). Plan: (1) start
  with roll limit ±12 in the end stops and in the URDF (flat walking uses ±5-10 -> enough); (2) almost free upgrade =
  high-misalignment conical spacers on the 2 foot-side eyes -> ±20-25, covers G1 target ±15 with margin, compatible with the
  M6 through bolt; (3) extreme upgrade = ball-stud (vertical tapered pin in the foot, local redesign) -> ±30-45, not now.
- 2026-06-10 (AI): SUPERSEDED point (3) above — found in the igus catalog the igubal **KBRM-08 CL** (2nd gen, hexagonal
  body + jam nut): **pivot ±35 degrees**, ball bore Ø8 E10, female thread M8, 8.6 g, loads 2.1 kN short-term /
  1.05 kN continuous (our rods ~0.6-1.2 kN short peak -> OK). TOTAL drop-in: same M8 aluminium rods + same pin
  (shoulder screw Ø8xM6), to be fitted only on the 2 FOOT-SIDE eyes (crank-arm side tilt ~0-2 -> stays standard). It matches the
  RobotEra ball-studs (±30) while staying catalog; KBLM-08 CL = left-hand thread. Note 2026-06-27: the current BOM instead uses
  **KARM-08 CL / KARM_08_CL_1 male M8 right-hand qty2 + KALM-08 CL male M8 left-hand qty2**; this old note remains
  only as history of the selection. The old qty0 path was: conical spacers M8->M6 (Competition Supplies/McGill, ±20-25)
  on the metal rod-ends. Side discovery: the
  industrial angle joints DIN 71802 only do 15-18 degrees, they are NOT the joints in the RobotEra/X-Humanoid photos.
  Ankle roll ladder: ±13 stock -> ±20-25 spacers -> ±35 igubal CL. igubal note: it is igumid G plastic, verify
  price from the configurator and no high temperatures.
- 2026-06-10 (AI+user): final PUSHROD ARCHITECTURE (questions: pin at 10? threaded rod as body?).
  (a) The PIN stays Ø8xM6: it is not the weak link (bending ~70-90 MPa vs >900 yield 12.9; the limit is the
  igubal plastic head). Going up to Ø10 does NOT strengthen the head and forces M10 threads -> heavier M10 rod body.
  Reserve: KARM-10 CL (2.5 kN short-term, ±35) only if the CAD keeps minimal foot lever arms and the worst case exceeds 1.2 kN.
  (b) NO threaded rod as the pushrod body: M8 threaded steel (core ~6.5) at 250 mm has Pcr ~2.7 kN -> SF
  ~2.3 on the peak 1.15 kN, BUT it is 4x less stiff in bending than the aluminium hex (EI 1.7e7 vs 7.1e7 Nmm2) = 'wobbly'
  (vibrates/flexes), thread = fatigue notch, similar weight. The RIGHT body is the ALUMINIUM hex of the AliExpress kit
  (female M8 RH+LH, Pcr ~10+ kN, SF ~9-18): we keep that one.
  (c) Foot-side head = igubal KARM-08 CL MALE M8 (±35, 1.7 kN short-term / 0.85 continuous, 6.2 g): it screws into the aluminium
  body in place of the stock metal head. Crank-arm side = stock head (tilt ~0-2), which also serves as the left-hand
  side for adjustment (KALM CL 'in preparation' in the catalog, availability to be verified). BOM updated
  2026-06-27: `2 x KARM-08 CL` male right-hand + `2 x KALM-08 CL` male left-hand, with `4 x` thin jam nuts DIN
  439 M8. KBRM/KBLM female remains only a historical/catalog variant and must not be used without changing the pushrod body.

## Open points to criticize before the purchases

1. Draw the ankle in CAD and compute the matrix between RS06 motor torques and virtual pitch/roll torques. If the margin
   is not enough try RS03; if instead the crank ratio gives reduction one can go down to RS02 (slower ankle, rod ~1
   kN). The ankle size comes out of the real crank ratio, not from the load (which only fixes the JOINT torque). Current baseline:
   printed ankle gimbal joint with two shoulder screws Ø8/M6 x 45 mm stacked in Z (pitch above, roll below) and
   four pushrod pivots Ø8/M6 x 16 mm; the active rod-ends are igus KARM-08 CL qty 2 right-hand + KALM-08 CL qty 2 left-hand.
   Keep volume open for a possible
   cleaner Cardan, but the CAD/sim must model the real offset as long as it exists. Separate in the CAD the two foot-shin axes
   from the pins on which the pushrods push. For each axis/pin dimension the width of the central part, axial space,
   volume swept by the lugs and by the rod-ends, seat outer diameter, shoulder length, fit, bushings, anti-rotation
   and retention; only then choose any bushings, metal inserts and final shims.
2. Draw the waist in CAD with roll below yaw: RS03 waist roll below, RS06 waist yaw above, no waist pitch and no
   waist pushrod/cardan in the current CAD. Verify vertical stack, cables, torso support and bending moment on the
   roll; the old 6002-2RS idle bearing and the pin Ø12/M10 are deactivated qty0 and must not be bought unless there is a CAD revision.
3. Find a reliable physical source or measure the G1-Comp neck motors. Until then RS05 x2 remains a provisional
   choice, not a verified G1 datum.
4. Wrist all RS00 (5 rated/14 peak, dual encoder): verify in CAD/use that it is enough on the roll (G1 25 Nm, but gravity ~0 and
   payload on the axis). Reserves qty0: RS02 (robust) and RS05 (ultralight pitch/yaw).
5. Rebuild the leg geometry from the joint origins and official G1 meshes `mode_11`, without confusing external meshes and internal
   CAD of the actuators.
6. Physically verify the RS04 envelope `120 x 120 x 56 mm` in the hips and at the knee: the power is close to the G1, but
   the packaging is not automatically equivalent.
7. Design harness and strain relief. K-Scale explicitly reports that the wiring is one of the least reliable parts.
8. Ask Bicycle Motor Works for confirmation of shipping to Italy, finished mass, connectors/charger, duration of the 100 A,
   short-circuit current, regenerative charge limit and BMS thresholds; in parallel ask Tõuksi Vabrik for a drawing of the
   EU fallback 60 A within 165 x 102 x 76 mm. Confirm that the main 70 A BF1 is coordinated with the BMS.
   Before walking measure currents and temperatures
   and size the bleeder energy/threshold on the real braking: the selected one is sufficient only for progressive
   bring-up as long as dynamic measurements do not exist.
9. Assess whether Thor is already owned or whether it must be kept in the cost: for bring-up alone it is oversized.
