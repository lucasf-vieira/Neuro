from lerobot.common.cameras.configs import ColorMode, Cv2Rotation
from lerobot.common.cameras.opencv.camera_opencv import OpenCVCamera
from lerobot.common.cameras.opencv.configuration_opencv import OpenCVCameraConfig
import torch
from lerobot.common.utils.utils import (
    get_safe_torch_device,
)


from lerobot.common.policies.smolvla.modeling_smolvla import SmolVLAPolicy
from lerobot.common.robots.so101_follower import SO101FollowerConfig, SO101Follower
from pathlib import Path


camera_config = OpenCVCameraConfig(
    index_or_path=4,
    fps=30,
    width=640,
    height=480,
    color_mode=ColorMode.RGB,
    rotation=Cv2Rotation.NO_ROTATION
)

robot_config = SO101FollowerConfig(
    port="/dev/ttyACM0",
    cameras={"camera": camera_config},
    id="movie",
    calibration_dir=Path("/home/lucasfv/Workspaces/hackathon_lerobot/Neuro/calibration")
)

robot = SO101Follower(robot_config)
robot.connect()
print(robot.cameras)
# observation = robot.get_observation()
# print(observation)

# device = get_safe_torch_device("cuda")
# policy = SmolVLAPolicy.from_pretrained("/home/fablab/lerobot/outputs/train/my_smolvla/checkpoints/last/pretrained_model/config.json", repo_type="local", device="cpu")

robot.disconnect()
