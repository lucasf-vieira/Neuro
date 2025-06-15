from enum import auto, Enum
import time

import numpy as np
from custom.gemini import VoiceIA
from lerobot.common.robots.so101_follower import SO101FollowerConfig, SO101Follower

from yolo.yolo import YOLOModel

class RobotStates(Enum):
    STANDBY = auto()
    STORE_OBJECT = auto()
    RETRIEVE_OBJECT = auto()
    GOTO_STORAGE = auto()
    WAIT_VOICE_RELEASE = auto()
    GOTO_STANDBY = auto()


class StateRunner:
    def __init__(self):
        self.running = False

    def run_states(self):
        self._prepare_systems()
        self.set_state(RobotStates.STANDBY)

        self.running = True
        while self.running:
            print(f"Current state: {self.state.name.title()}")
            run_state = getattr(self, self.state.name.lower())
            run_state()
            time.sleep(0.5)
        print("Robot stopped")

    def _prepare_systems(self):
        self.robot = self._prepare_robot()
        self.yolo = self._prepare_yolo()
        self.voice = self._prepare_voice()

    def _prepare_robot(self):
        print("Preparing robot")
        print("Robot ready")
        # robot_config = SO101FollowerConfig(
        #     port="/dev/ttyACM0",
        #     id="movie",
        # )

        # robot = SO101Follower(robot_config)
        # self.robot.connect()
        # return robot

    def _prepare_yolo(self):
        print("Preparing YOLO")
        yolo = YOLOModel("model.pt")
        print("YOLO ready")
        return yolo

    def _prepare_voice(self):
        print("Preparing voice")
        voiceIA = VoiceIA()
        voiceIA.listen()
        print("Voice ready")
        return voiceIA

    #
    #   Robot States
    #

    def set_state(self, state: RobotStates):
        if not isinstance(state, RobotStates):
            raise ValueError(f"Invalid state: {state}")
        self.state = state
        self._prepare_voice()

    def _prepare_voice(self):
        if self.state in (
            RobotStates.STANDBY,
            RobotStates.WAIT_VOICE_RELEASE
        ):
            self.voice.listen()
        elif self.state in (
            RobotStates.RETRIEVE_OBJECT,
            RobotStates.STORE_OBJECT,
            RobotStates.GOTO_STANDBY
        ):
            self.voice.stop()

    def standby(self):
        # Aguarda presenca de pecas da pessoa
        # image = self.robot.get_image()
        # class = self.yolo.predict_best_class(image)
        # if class != "none":
        #     # Move to next state
        #     self.detected_class = class
        #     self.set_state(RobotStates.STORE_OBJECT)

        # Aguarda comando de voz
        if self.voice.request_is_ready():
            self.request=self.voice.read_request()
            self.voice.stop()

            # Move to next state
            self.set_state(RobotStates.RETRIEVE_OBJECT)

    def store_object(self):
        # Store object
        # self.detected_class
        # self.robot.send_action()

        # Move to next state
        self.set_state(RobotStates.GOTO_STANDBY)

    def retrieve_object(self):
        # Vai para o ponto antes de pegar objetos
        # self.request
        # self.robot.send_action()

        # Move to next state
        self.set_state(RobotStates.WAIT_VOICE_RELEASE)

    def wait_voice_release(self):
        # Aguarda comando de voz para soltar
        # self.voice.request
        # self.robot.send_action()

        # Move to next state
        self.set_state(RobotStates.GOTO_STANDBY)

    def goto_standby(self):
        """Utiliza ângulos fixos dos motores para ir para a posicao de standby"""
        # Move to standby position
        # robot.send_action({'shoulder_pan.pos': 46.93274205469328, 'shoulder_lift.pos': 12.880366819508126, 'elbow_flex.pos': -9.432275368797491, 'wrist_flex.pos': 79.80535279805352, 'wrist_roll.pos': 9.614880796436992, 'gripper.pos': 1.1058451816745656})
        self.voice.listen()

        # Move to next state
        self.set_state(RobotStates.STANDBY)

    #
    #   Helper functions
    #

    def _release_grip(self):
        # Open the robot's grip
        # robot.send_action()
        ...

    def _close_grip(self):
        # Close the robot's grip
        # robot.send_action()
        ...

def main():
    bot = StateRunner()
    try:
        bot.run_states()
    except KeyboardInterrupt:
        print("Program stopped")

if __name__ == "__main__":
    main()