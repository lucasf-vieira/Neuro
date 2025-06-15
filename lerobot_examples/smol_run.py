import torch
from lerobot.common.utils.utils import (
    get_safe_torch_device,
)

from lerobot.common.policies.smolvla.modeling_smolvla import SmolVLAPolicy
from lerobot.common.robots.so101_follower import SO101FollowerConfig, SO101Follower


robot_config = SO101FollowerConfig(
    port="/dev/ttyACM0",
    id="movie",
)

robot = SO101Follower(robot_config)
robot.connect()

device = get_safe_torch_device("cuda")
policy = SmolVLAPolicy.from_pretrained("/home/fablab/lerobot/outputs/train/my_smolvla/checkpoints/last/pretrained_model/config.json")

done = True
while not done:
    observation = robot.get_observation()

    # Prepare observation for the policy running in Pytorch
    state = torch.from_numpy(observation["agent_pos"])
    image = torch.from_numpy(observation["pixels"])
    lang = torch.from_numpy(observation["lang"])

    # Convert to float32 with image from channel first in [0,255]
    # to channel last in [0,1]
    state = state.to(torch.float32)
    image = image.to(torch.float32) / 255
    image = image.permute(2, 0, 1)
    lang = lang.to(torch.long)

    # Send data tensors from CPU to GPU
    state = state.to(device, non_blocking=True)
    image = image.to(device, non_blocking=True)
    lang = lang.to(device, non_blocking=True)

    # Add extra (empty) batch dimension, required to forward the policy
    state = state.unsqueeze(0)
    image = image.unsqueeze(0)
    lang = lang.unsqueeze(0)

    # Create the policy input dictionary
    observation = {
        "observation.state": state,
        "observation.image": image,
        "observation.lang": lang
    }

    # Predict the next action with respect to the current observation
    with torch.inference_mode():
        action = policy.select_action(observation)

    # Prepare the action for the environment
    numpy_action = action.squeeze(0).to("cpu").numpy()

    # Send the action to the robot
    robot.send_action(numpy_action)

    # Check if the episode is done
    done = observation["done"]

robot.disconnect()