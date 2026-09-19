# Publishing texts

Same short text everywhere, lowercase name, no marketing.

## Published 2026-09-19

- GitHub https://github.com/AlessioPagliai/umanoide
- Printables https://www.printables.com/model/1846831-umanoide-open-source-humanoid-in-design
- Thingiverse https://www.thingiverse.com/thing:7411626
- MakerWorld https://makerworld.com/it/@RiverFamily — draft 9686078 complete and submitted, rejected by the automatic check ("no real photo detected"): add a photo of a printed part and resubmit from Modelli 3D › Fallito › Modifica, then swap in the model link
- YouTube https://youtu.be/bHGGjXYELUE
- riverfamily.art https://riverfamily.art/#umanoide
- Files https://storage.googleapis.com/riverfamily/umanoide/

## Name

`umanoide`

## One line (site, catalogue, video subtitle)

Open source humanoid, 3D printed, 30 RobStride actuators, Jetson Thor. In design.

## Printables · MakerWorld · Thingiverse

**Title:** umanoide — open source humanoid (in design)

**Description:**

Open source humanoid. 3D printed structure in PA-CF, 30 RobStride quasi-direct-drive actuators, NVIDIA Jetson AGX Thor, Unitree G1 kinematics as reference. Height ≈ 1.40 m, ≈ 45 kg.

Still in design, not built yet. Everything is shared to build it together: CAD, bill of materials with links, electrical scheme, simulation files and walking policies in Isaac Lab.

These are the first printed parts: the ankle offset gimbal and a leg test plate (femur, hip bracket, tibia). More parts follow as the design is frozen.

CAD: https://cad.onshape.com/documents/2a6d830c153f862229ff478f/w/82c50406ffe66995476ba0a1/e/6ac57dbaf03b523effa40409
Everything else: https://github.com/AlessioPagliai/umanoide
Video: https://youtu.be/bHGGjXYELUE

Print: ankle gimbal in Bambu PPA-CF, 0.2 mm, 0.4 nozzle, Bambu Lab H2C, 1 wall, 90 % grid infill; leg test plate in PLA on an H2S. Settings are in the 3MF.

Licence: CC0, public domain.

**Files:** `ankle-gimbal.3mf`, `leg-test-plate.3mf`, `electrical/scheme.png`, screenshots

**Category:** Robotics · **Tags:** humanoid, robot, open source, robstride, jetson thor, isaac lab, ppa-cf, bambu h2c

## YouTube

**Title:** umanoide — open source humanoid, walking in Isaac Lab

**Description:**

Open source humanoid in design: 3D printed, 30 RobStride actuators, Jetson AGX Thor. Walking policy trained in Isaac Lab on rough terrain. Not built yet — shared to build it together.

CAD https://cad.onshape.com/documents/2a6d830c153f862229ff478f/w/82c50406ffe66995476ba0a1/e/6ac57dbaf03b523effa40409
Files https://github.com/AlessioPagliai/umanoide
Printables https://www.printables.com/model/1846831-umanoide-open-source-humanoid-in-design
Thingiverse https://www.thingiverse.com/thing:7411626
https://riverfamily.art/

CC0

**Video:** `walk-kneehard.mp4` (20 s, 1280×720, 50 fps) — or both clips back to back, then the Onshape GIF.

## riverfamily.art — catalogue.json entry

```json
{
  "slug": "umanoide",
  "name": "umanoide",
  "category": "Robots",
  "description": "Open source humanoid, 3D printed, 30 RobStride actuators, Jetson Thor. In design.",
  "image": "https://riverfamily.art/static/images/umanoide.webp?v=20260919",
  "downloads": [
    {
      "url": "https://storage.googleapis.com/riverfamily/umanoide/umanoide-urdf.zip",
      "size": 11792994,
      "updated": "2026-09-19T08:46:05.000Z"
    }
  ],
  "source_files": [],
  "readmes": [],
  "links": {
    "github": "https://github.com/AlessioPagliai/umanoide",
    "onshape": "https://cad.onshape.com/documents/2a6d830c153f862229ff478f/w/82c50406ffe66995476ba0a1/e/6ac57dbaf03b523effa40409"
  }
}
```

(`links` is a new key: add it to the template or put the two URLs in the description.)

## RiverFamily README — new section before "About this catalogue"

```markdown
### Robots

<details id="umanoide">
<summary><strong>umanoide</strong> — Open source humanoid, 3D printed, 30 RobStride actuators, Jetson Thor. In design.</summary>

<img src="images/umanoide.webp" alt="umanoide by River Family" width="520">

**Files and published pages**

[GitHub](https://github.com/AlessioPagliai/umanoide) · [CAD on Onshape](https://cad.onshape.com/documents/2a6d830c153f862229ff478f/w/82c50406ffe66995476ba0a1/e/6ac57dbaf03b523effa40409) · [URDF package](https://storage.googleapis.com/riverfamily/umanoide/umanoide-urdf.zip) · 11.8 MB · [Printables](https://www.printables.com/model/1846831-umanoide-open-source-humanoid-in-design) · [Thingiverse](https://www.thingiverse.com/thing:7411626) · [MakerWorld](https://makerworld.com/it/@RiverFamily) · [YouTube](https://youtu.be/bHGGjXYELUE)

Not built yet. The GitHub repository has the bill of materials with every supplier link, the electrical scheme, the simulation pipeline and the design notes.

</details>
```

## Image list to produce (Onshape)

1. `hero` — full robot, front three-quarter, white background
2. `side` — full robot, side
3. `ankle` — shin with the two motors, pushrods and gimbal
4. `torso` — torso open with battery, Thor, converter, contactor
5. `gif` — a joint sweep or a full-body pose change, 5–8 s

Export at 1600 px wide or more, save as `images/<name>.webp` in the repo, `hero.webp` also in the RiverFamily `images/` folder.
