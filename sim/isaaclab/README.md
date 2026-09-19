# Isaac Lab training code

Not in this folder yet. The walking policy (run "KneeHard", rough terrain, velocity tracking) was trained on the simulation workstation: the task configuration, rewards, actuator gains and checkpoints live there.

To add here:

- the Isaac Lab task package: environment, rewards, terminations, curriculum, actuator configuration for the RobStride motors
- the training runner configuration and the train / play commands
- the exported policy and its observation and action layout
- the run comparison notes: KneeDefault, KneeSoft, KneeHard, KneeTorque, Crouch, ArmsFwd

Until then, what is needed to rebuild it is in [docs/handoffs/isaac.md](../../docs/handoffs/isaac.md): import settings, gains, acceptance tests.
