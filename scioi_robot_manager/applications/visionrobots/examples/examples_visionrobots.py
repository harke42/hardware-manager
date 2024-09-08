import math
import threading
import time


from applications.visionrobots.visionrobot_manager import VisionRobotManager

robot = None
joystick = None


def streamCallback(stream, device, *args, **kwargs):
    ...
    #print(f"New Stream {stream}")


def handControl():
    was_set = False
    while True:
        if robot is not None and joystick is not None:
            val1 = joystick.axis[1]
            val2 = joystick.axis[0]
            speed_left = -0.5 * val1 + 0.5 * val2
            speed_right = -0.5 * val1 - 0.5 * val2
            if speed_left != 0 or speed_right != 0:
                robot.device.command('setSpeed', {'speed': [speed_left, speed_right]})
                was_set = True
            else:
                if was_set:
                    robot.device.command('setSpeed', {'speed': [0.0, 0.0]})

        time.sleep(0.1)

def send_goTo(cmd):
    for i in range(1, len(cmd)):
        try:
            tmp = cmd[i].split(sep="|")
            x = float(tmp[0])
            y = float(tmp[1])
            robot.device.command('goTo', {'x': x, 'y': y})
            time.sleep(0.1)
        except:
            print("Error in send_goTo")
            pass
def readInput():
    print("Options: ")
    print("turn $psi")
    print("goTo 1.3|2.4 3.5|4.6 ...")
    while True:
        if robot is not None:
            cmd = input("Enter: ")
            cmd = cmd.split(sep=" ")
            if cmd[0] == "turn":
                phi = float(cmd[1])
                robot.device.command('turn', {'phi': phi})
            elif cmd[0] == "goTo":
                send_goTo(cmd)
        time.sleep(0.1)


def example_1():
    def robot_connected_callback(new_robot, *args, **kwargs):
        global robot
        if new_robot.device.information.device_id == 'visionrobot1':
            robot = new_robot

    def joystick_connected_callback(new_joystick, *args, **kwargs):
        global joystick
        joystick = new_joystick

    def turn(robot):
        robot.device.command('turn', {'phi': [math.pi]})

    manager = VisionRobotManager()
    manager.init()
    manager.start()

    manager.registerCallback('new_robot', robot_connected_callback)
    manager.registerCallback('new_joystick', joystick_connected_callback)
    manager.registerCallback('stream', streamCallback)

    hand_control_thread = threading.Thread(target=handControl)
    input_thread = threading.Thread(target=readInput)

    hand_control_thread.daemon = True
    input_thread.daemon = True

    hand_control_thread.start()
    input_thread.start()

    while True:
        time.sleep(0.1)


if __name__ == '__main__':
    example_1()

#goTo 1|2 4|3 5|6 8|7
