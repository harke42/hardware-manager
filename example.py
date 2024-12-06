import threading
import time

from visionrobot.visionrobot_manager import VisionRobotManager

robots = []
ALLOWED_IDS = ['visionrobot1']

def streamCallback(stream, device, *args, **kwargs):
    print(f"Received {stream} from {device}")

def read_input():
    print("mov robot_id dphi[rad] radius[mm] {time[s]}")
    print("Example: mov 2 3.141 300 5")

    while True:
        if robots != []:
            try:
                cmd = input("Enter command: ")
                cmd = cmd.split(sep=" ")
                if cmd[0] == "mov":
                    id = int(cmd[1])
                    dphi = float(cmd[2])
                    radius = float(cmd[3])
                    if len(cmd) == 4:
                        robots[id].device.command('add_movement', {'dphi': dphi, 'radius': radius, 'vtime': 0})
                    elif len(cmd) == 5:
                        vtime = float(cmd[4])
                        robots[id].device.command('add_movement', {'dphi': dphi, 'radius': radius, 'vtime': vtime})
                    else:
                        continue
            except Exception as e:
                print(e)
                print("Error occured in Input Task, Continuing")
        time.sleep(0.1)

def send_movements(robot, list):
    robot.device.command('add_movements', {'list': list})

def main():
    def robot_connected_callback(new_robot, *args, **kwargs):
        global robots
        if new_robot.device.information.device_id in ALLOWED_IDS:
            robots.append(new_robot)

    manager = VisionRobotManager()
    manager.start()

    manager.registerCallback('new_robot', robot_connected_callback)
    manager.registerCallback('stream', streamCallback)

    input_thread = threading.Thread(target=read_input)
    input_thread.daemon = True
    input_thread.start()

    while True:
        time.sleep(0.1)

if __name__ == '__main__':
    main()