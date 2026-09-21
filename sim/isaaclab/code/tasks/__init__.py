# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import gymnasium as gym

from . import agents

##
# Register Gym environments.
##

gym.register(
    id="Isaac-Velocity-Rough-Robstride-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:RobstrideRoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:RobstrideRoughPPORunnerCfg",
    },
)


gym.register(
    id="Isaac-Velocity-Rough-Robstride-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:RobstrideRoughEnvCfg_PLAY",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:RobstrideRoughPPORunnerCfg",
    },
)


gym.register(
    id="Isaac-Velocity-Flat-Robstride-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.flat_env_cfg:RobstrideFlatEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:RobstrideFlatPPORunnerCfg",
    },
)


gym.register(
    id="Isaac-Velocity-Flat-Robstride-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.flat_env_cfg:RobstrideFlatEnvCfg_PLAY",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:RobstrideFlatPPORunnerCfg",
    },
)


gym.register(
    id="Isaac-Velocity-Flat-Humanoid-G1WholeBody-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.g1_whole_body_env_cfg:HumanoidG1WholeBodyFlatEnvCfg",
        "rsl_rl_cfg_entry_point": (
            f"{agents.__name__}.rsl_rl_ppo_cfg:HumanoidG1WholeBodyFlatPPORunnerCfg"
        ),
    },
)


for _r5 in ("ArmsFwd", "KneeSoft", "KneeHard", "Crouch", "KneeDefault", "KneeTorque"):
    gym.register(
        id=f"Isaac-Velocity-R5-{_r5}-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.round5_env_cfg:Humanoid{_r5}EnvCfg",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Humanoid{_r5}PPORunnerCfg",
        },
    )
    gym.register(
        id=f"Isaac-Velocity-R5-{_r5}-Play-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.round5_env_cfg:Humanoid{_r5}PlayEnvCfg",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Humanoid{_r5}PPORunnerCfg",
        },
    )


for _r4 in ("PendBase", "PendShort", "PendLow", "PendSlow", "ImpactShort", "PendTrack"):
    gym.register(
        id=f"Isaac-Velocity-R4-{_r4}-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.round4_env_cfg:Humanoid{_r4}EnvCfg",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Humanoid{_r4}PPORunnerCfg",
        },
    )
    gym.register(
        id=f"Isaac-Velocity-R4-{_r4}-Play-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.round4_env_cfg:Humanoid{_r4}PlayEnvCfg",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Humanoid{_r4}PPORunnerCfg",
        },
    )


for _r3 in ("WalkG1", "WalkH1", "WalkTiny", "RunPend", "RunImpact", "RunG1"):
    gym.register(
        id=f"Isaac-Velocity-R3-{_r3}-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.round3_env_cfg:Humanoid{_r3}EnvCfg",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Humanoid{_r3}PPORunnerCfg",
        },
    )
    gym.register(
        id=f"Isaac-Velocity-R3-{_r3}-Play-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.round3_env_cfg:Humanoid{_r3}PlayEnvCfg",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Humanoid{_r3}PPORunnerCfg",
        },
    )


for _soft in ("Soft", "SoftImpact", "SoftSlow", "SoftTiny", "SoftClock", "SoftPend"):
    gym.register(
        id=f"Isaac-Velocity-Soft-{_soft}-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.soft_ways_env_cfg:Humanoid{_soft}EnvCfg",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Humanoid{_soft}PPORunnerCfg",
        },
    )
    gym.register(
        id=f"Isaac-Velocity-Soft-{_soft}-Play-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.soft_ways_env_cfg:Humanoid{_soft}PlayEnvCfg",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Humanoid{_soft}PPORunnerCfg",
        },
    )


for _way in ("G1", "TienKung", "Digit", "H1", "Cassie", "Hybrid"):
    gym.register(
        id=f"Isaac-Velocity-Way-{_way}-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.six_ways_env_cfg:Humanoid{_way}WayEnvCfg",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Humanoid{_way}WayPPORunnerCfg",
        },
    )
    gym.register(
        id=f"Isaac-Velocity-Way-{_way}-Play-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.six_ways_env_cfg:Humanoid{_way}WayPlayEnvCfg",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Humanoid{_way}WayPPORunnerCfg",
        },
    )


for _name, _cfg, _runner in (
    ("G1Corrected", "HumanoidG1CorrectedEnvCfg", "HumanoidG1CorrectedPPORunnerCfg"),
    ("TienKungCorrected", "HumanoidTienKungCorrectedEnvCfg", "HumanoidTienKungCorrectedPPORunnerCfg"),
):
    gym.register(
        id=f"Isaac-Velocity-Rough-Humanoid-{_name}-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.legs_only_env_cfg:{_cfg}",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:{_runner}",
        },
    )
    gym.register(
        id=f"Isaac-Velocity-Rough-Humanoid-{_name}-Play-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": f"{__name__}.legs_only_env_cfg:{_cfg}_PLAY",
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:{_runner}",
        },
    )


gym.register(
    id="Isaac-Velocity-Rough-Humanoid-Symmetry-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        # same env as Isaac-Velocity-Rough-Robstride-v0; only the PPO runner differs
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:RobstrideRoughEnvCfg",
        "rsl_rl_cfg_entry_point": (
            f"{agents.__name__}.rsl_rl_ppo_cfg:HumanoidSymmetryRoughPPORunnerCfg"
        ),
    },
)


gym.register(
    id="Isaac-Velocity-Rough-Humanoid-Symmetry-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:RobstrideRoughEnvCfg_PLAY",
        "rsl_rl_cfg_entry_point": (
            f"{agents.__name__}.rsl_rl_ppo_cfg:HumanoidSymmetryRoughPPORunnerCfg"
        ),
    },
)


gym.register(
    id="Isaac-Velocity-Rough-Humanoid-DigitStyle-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.digit_style_env_cfg:HumanoidDigitStyleRoughEnvCfg",
        "rsl_rl_cfg_entry_point": (
            f"{agents.__name__}.rsl_rl_ppo_cfg:HumanoidDigitStyleRoughPPORunnerCfg"
        ),
    },
)


gym.register(
    id="Isaac-Velocity-Rough-Humanoid-DigitStyle-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.digit_style_env_cfg:HumanoidDigitStyleRoughEnvCfg_PLAY",
        "rsl_rl_cfg_entry_point": (
            f"{agents.__name__}.rsl_rl_ppo_cfg:HumanoidDigitStyleRoughPPORunnerCfg"
        ),
    },
)


gym.register(
    id="Isaac-Velocity-Rough-Humanoid-G1WholeBody-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            f"{__name__}.g1_whole_body_rough_env_cfg:HumanoidG1WholeBodyRoughEnvCfg"
        ),
        "rsl_rl_cfg_entry_point": (
            f"{agents.__name__}.rsl_rl_ppo_cfg:HumanoidG1WholeBodyRoughPPORunnerCfg"
        ),
    },
)


gym.register(
    id="Isaac-Velocity-Rough-Humanoid-G1WholeBody-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            f"{__name__}.g1_whole_body_rough_env_cfg:HumanoidG1WholeBodyRoughEnvCfg_PLAY"
        ),
        "rsl_rl_cfg_entry_point": (
            f"{agents.__name__}.rsl_rl_ppo_cfg:HumanoidG1WholeBodyRoughPPORunnerCfg"
        ),
    },
)


gym.register(
    id="Isaac-Velocity-Flat-Humanoid-G1WholeBody-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            f"{__name__}.g1_whole_body_env_cfg:HumanoidG1WholeBodyFlatEnvCfg_PLAY"
        ),
        "rsl_rl_cfg_entry_point": (
            f"{agents.__name__}.rsl_rl_ppo_cfg:HumanoidG1WholeBodyFlatPPORunnerCfg"
        ),
    },
)


gym.register(
    id="Isaac-Velocity-Flat-Humanoid-TienKungPeriodic-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            f"{__name__}.tienkung_whole_body_env_cfg:HumanoidTienKungPeriodicFlatEnvCfg"
        ),
        "rsl_rl_cfg_entry_point": (
            f"{agents.__name__}.rsl_rl_ppo_cfg:HumanoidTienKungPeriodicFlatPPORunnerCfg"
        ),
    },
)


gym.register(
    id="Isaac-Velocity-Flat-Humanoid-TienKungPeriodic-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            f"{__name__}.tienkung_whole_body_env_cfg:HumanoidTienKungPeriodicFlatEnvCfg_PLAY"
        ),
        "rsl_rl_cfg_entry_point": (
            f"{agents.__name__}.rsl_rl_ppo_cfg:HumanoidTienKungPeriodicFlatPPORunnerCfg"
        ),
    },
)
