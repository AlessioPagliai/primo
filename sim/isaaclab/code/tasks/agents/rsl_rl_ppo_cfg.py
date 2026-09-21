# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from isaaclab.utils import configclass

from isaaclab_rl.rsl_rl import (
    RslRlOnPolicyRunnerCfg,
    RslRlPpoActorCriticCfg,
    RslRlPpoAlgorithmCfg,
    RslRlSymmetryCfg,
)

from isaaclab_tasks.manager_based.locomotion.velocity.mdp.symmetry import humanoid_biped


@configclass
class RobstrideRoughPPORunnerCfg(RslRlOnPolicyRunnerCfg):
    num_steps_per_env = 24
    max_iterations = 3000
    save_interval = 50
    experiment_name = "robstride_rough"
    policy = RslRlPpoActorCriticCfg(
        init_noise_std=1.0,
        actor_obs_normalization=False,
        critic_obs_normalization=False,
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
    )
    algorithm = RslRlPpoAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.008,
        num_learning_epochs=5,
        num_mini_batches=4,
        learning_rate=1.0e-3,
        schedule="adaptive",
        gamma=0.99,
        lam=0.95,
        desired_kl=0.01,
        max_grad_norm=1.0,
    )


@configclass
class RobstrideFlatPPORunnerCfg(RobstrideRoughPPORunnerCfg):
    def __post_init__(self):
        super().__post_init__()

        self.max_iterations = 1500
        self.experiment_name = "robstride_flat"
        self.policy.actor_hidden_dims = [256, 128, 128]
        self.policy.critic_hidden_dims = [256, 128, 128]


@configclass
class HumanoidG1WholeBodyFlatPPORunnerCfg(RobstrideFlatPPORunnerCfg):
    """Separate log namespace for the fair 28-DOF G1-style rerun."""

    def __post_init__(self):
        super().__post_init__()
        self.experiment_name = "humanoid_flat_g1_whole_body"


@configclass
class HumanoidSymmetryRoughPPORunnerCfg(RobstrideRoughPPORunnerCfg):
    """Identical to the plain rough runner except for left-right symmetry augmentation.

    Every sampled state is also trained in mirror image, so an asymmetric (lame) gait cannot
    remain a stable optimum. This is the only variable that differs from the ``robstride_rough``
    baseline, so the two runs are a clean A/B.
    """

    def __post_init__(self):
        super().__post_init__()
        self.experiment_name = "humanoid_rough_symmetry"
        self.max_iterations = 3000
        self.algorithm.symmetry_cfg = RslRlSymmetryCfg(
            use_data_augmentation=True,
            data_augmentation_func=humanoid_biped.compute_symmetric_states,
        )


def _make_way_runner(name: str):
    """One runner per reward recipe; separate log namespace, symmetry inherited."""

    @configclass
    class _Runner(HumanoidSymmetryRoughPPORunnerCfg):
        def __post_init__(self):
            super().__post_init__()
            self.experiment_name = f"way_{name.lower()}"
            self.max_iterations = 3000

    _Runner.__name__ = f"Humanoid{name}WayPPORunnerCfg"
    return _Runner


for _n in ("G1", "TienKung", "Digit", "H1", "Cassie", "Hybrid"):
    globals()[f"Humanoid{_n}WayPPORunnerCfg"] = _make_way_runner(_n)


def _make_soft_runner(name: str):
    @configclass
    class _Runner(HumanoidSymmetryRoughPPORunnerCfg):
        def __post_init__(self):
            super().__post_init__()
            self.experiment_name = f"soft_{name.lower()}"
            self.max_iterations = 3000

    _Runner.__name__ = f"Humanoid{name}PPORunnerCfg"
    return _Runner


for _n in ("Soft", "SoftImpact", "SoftSlow", "SoftTiny", "SoftClock", "SoftPend"):
    globals()[f"Humanoid{_n}PPORunnerCfg"] = _make_soft_runner(_n)


def _make_round3_runner(name: str):
    @configclass
    class _Runner(HumanoidSymmetryRoughPPORunnerCfg):
        def __post_init__(self):
            super().__post_init__()
            self.experiment_name = f"r3_{name.lower()}"
            self.max_iterations = 3000

    _Runner.__name__ = f"Humanoid{name}PPORunnerCfg"
    return _Runner


for _n in ("WalkG1", "WalkH1", "WalkTiny", "RunPend", "RunImpact", "RunG1"):
    globals()[f"Humanoid{_n}PPORunnerCfg"] = _make_round3_runner(_n)


def _make_round4_runner(name: str):
    @configclass
    class _Runner(HumanoidSymmetryRoughPPORunnerCfg):
        def __post_init__(self):
            super().__post_init__()
            self.experiment_name = f"r4_{name.lower()}"
            self.max_iterations = 3000

    _Runner.__name__ = f"Humanoid{name}PPORunnerCfg"
    return _Runner


for _n in ("PendBase", "PendShort", "PendLow", "PendSlow", "ImpactShort", "PendTrack"):
    globals()[f"Humanoid{_n}PPORunnerCfg"] = _make_round4_runner(_n)


def _make_round5_runner(name: str):
    @configclass
    class _Runner(HumanoidSymmetryRoughPPORunnerCfg):
        def __post_init__(self):
            super().__post_init__()
            self.experiment_name = f"r5_{name.lower()}"
            self.max_iterations = 3000

    _Runner.__name__ = f"Humanoid{name}PPORunnerCfg"
    return _Runner


for _n in ("ArmsFwd", "KneeSoft", "KneeHard", "Crouch", "KneeDefault", "KneeTorque"):
    globals()[f"Humanoid{_n}PPORunnerCfg"] = _make_round5_runner(_n)


@configclass
class HumanoidG1CorrectedPPORunnerCfg(HumanoidSymmetryRoughPPORunnerCfg):
    """G1 rewards + gait corrections + symmetry."""

    def __post_init__(self):
        super().__post_init__()
        self.experiment_name = "humanoid_g1_corrected_sym"


@configclass
class HumanoidTienKungCorrectedPPORunnerCfg(HumanoidSymmetryRoughPPORunnerCfg):
    """TienKung periodic gait + gait corrections + symmetry."""

    def __post_init__(self):
        super().__post_init__()
        self.experiment_name = "humanoid_tienkung_corrected_sym"


@configclass
class HumanoidDigitStyleRoughPPORunnerCfg(RobstrideRoughPPORunnerCfg):
    """Digit-style rough run. Digit itself uses the shared rough runner settings."""

    def __post_init__(self):
        super().__post_init__()
        self.experiment_name = "humanoid_digit_style_rough"
        self.max_iterations = 3000


@configclass
class HumanoidG1WholeBodyRoughPPORunnerCfg(RobstrideFlatPPORunnerCfg):
    """Rough-terrain fine-tune of the flat G1-whole-body policy.

    Same network shape as the flat runner so the flat checkpoint loads. Lower LR because
    this continues an already-trained policy rather than starting from scratch.
    """

    def __post_init__(self):
        super().__post_init__()
        self.experiment_name = "humanoid_rough_g1_whole_body_finetune"
        self.max_iterations = 1500
        self.algorithm.learning_rate = 3.0e-4


@configclass
class HumanoidTienKungPeriodicFlatPPORunnerCfg(RobstrideFlatPPORunnerCfg):
    """Separate logs for the controlled TienKung-periodic comparison."""

    def __post_init__(self):
        super().__post_init__()
        self.experiment_name = "humanoid_flat_tienkung_periodic"
