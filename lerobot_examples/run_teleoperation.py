from lerobot.common.robots.so101_follower import SO101FollowerConfig, SO101Follower


def standby():

    robot_config = SO101FollowerConfig(
        port="/dev/ttyACM1",
        id="movie",
    )

    robot = SO101Follower(robot_config)
    robot.connect()

    try:
        while True:
            robot.send_action({'shoulder_pan.pos': 46.93274205469328, 'shoulder_lift.pos': 12.880366819508126, 'elbow_flex.pos': -9.432275368797491, 'wrist_flex.pos': 79.80535279805352, 'wrist_roll.pos': 9.614880796436992, 'gripper.pos': 1.1058451816745656})
    except KeyboardInterrupt:
        robot.disconnect()        

if __name__=="__main__":
    print("go to standby")
    standby()

