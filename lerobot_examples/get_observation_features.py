import torch
from lerobot.common.utils.utils import (
    get_safe_torch_device,
)

from lerobot.common.policies.smolvla.modeling_smolvla import SmolVLAPolicy
from lerobot.common.robots.so101_follower import SO101FollowerConfig, SO101Follower


# robot_config = SO101FollowerConfig(
#     port="/dev/ttyACM0",
#     id="movie",
# )

# robot = SO101Follower(robot_config)
# robot.connect()
# observation = robot.get_observation()
# print(observation)

# device = get_safe_torch_device("cuda")
policy = SmolVLAPolicy.from_pretrained("/home/fablab/lerobot/outputs/train/my_smolvla/checkpoints/last/pretrained_model/config.json", repo_type="local", device="cpu")

# robot.disconnect()
