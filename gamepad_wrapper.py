#!/usr/bin/python3

from evdev import InputDevice, categorize, ecodes, list_devices
import psutil
from select import select
import json
import os.path
from sys import argv

############# Configuration ##############

if len(argv) <= 1:
    print("No application specified! Exiting.")
    exit()

mode = "normal"  # change to debug for additional output

# More information from https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html
dev_config = dict()
# Set an entry for the controller with its name
# Change script mode to debug to see the connected controller names and paths
dev_config["Xbox Wireless Controller"] = dict()
# Configure the buttons to be pressed simultaneously to terminate the emulator
# The first button acts as hotkey enable and must be pressed before the other buttons
# You can set up as many buttons as you like
# Change script mode to debug to see your button presses (run script manually)
dev_config["Xbox Wireless Controller"]["buttons"] = [158, 315]

# Process to look for to kill when all keys are pressed
procName = '/usr/games/PCSX2'

config_file = "gamepad_wrapper.json"
config_file = os.path.dirname(os.path.abspath(__file__)) + "/" + config_file
if os.path.isfile(config_file):
    with open(config_file, 'r') as json_config:
        json_data = json.load(json_config)
        if "dev_config" in json_data:
            valid = True
            for entry in json_data["dev_config"].values():
                if not "buttons" in entry:
                    valid = False
            if valid:
                dev_config = json_data["dev_config"]
            else:
                print("Error parsing dev_config")
        if "proc_names" in json_data:
            if argv[1] not in json_data["proc_names"].keys():
                print("Specified application not configured. Exiting.")
                exit()
            procName = json_data["proc_names"][argv[1]]
        if "mode" in json_data:
            mode = json_data["mode"]
else:
    print("No config file found! Using default values.")


############# Functionality ##############

available_devices = [InputDevice(path) for path in list_devices()]
gamepads = {}
buttons_pressed = []

if mode == "debug":
    print("Available devices:")
for device in available_devices:
    if mode == "debug":
        print(device.name, device.path)
    if device.name in dev_config.keys():
        gamepads[device.fd] = {
            "device": device,
            "buttons": dev_config[device.name]["buttons"],
            "buttons_pressed": [False for element in range(len(dev_config[device.name]["buttons"]))]
        }

if len(gamepads.keys()) == 0:
    print("Specified device not found. Exiting...")
    exit()
if mode == "debug":
    print("Chosen device paths: ", *(gamepads[dev]["device"].path for dev in gamepads.keys()), sep='\n')

active = True
while active:
    try:
        r, w, x = select(gamepads, [], [])  # efficiently wait for input of any gamepad
        for fd in r:
            for event in gamepads[fd]["device"].read():
                if event.type == ecodes.EV_KEY:
                    if event.value == 1:  # Button pressed
                        if mode == "debug":
                            print("Button pressed for device ", gamepads[fd]["device"].path)
                            print(event.code)
                            if event.code in ecodes.KEY:
                                print(ecodes.KEY[event.code])
                        # if the first defined button (acting as hotkey enable) is pressed
                        # or already has been pressed, update the respective buttons_pressed values
                        if event.code == gamepads[fd]["buttons"][0] \
                                or gamepads[fd]["buttons_pressed"][0]:
                            if event.code in gamepads[fd]["buttons"]:
                                index = gamepads[fd]["buttons"].index(event.code)
                                gamepads[fd]["buttons_pressed"][index] = True
                    elif event.value == 0:  # Button released
                        if mode == "debug":
                            print("Button released for device ", gamepads[fd]["device"].path)
                            print(event.code)
                            if event.code in ecodes.KEY:
                                print(ecodes.KEY[event.code])
                        # if the hotkey enable button is released, we reset all buttons
                        if event.code == gamepads[fd]["buttons"][0]:
                            gamepads[fd]["buttons_pressed"] = [False for element in range(len(gamepads[fd]["buttons"]))]
                        elif event.code in gamepads[fd]["buttons"]:
                            index = gamepads[fd]["buttons"].index(event.code)
                            gamepads[fd]["buttons_pressed"][index] = False

                    # if all values are true, i.e. all buttons are pressed, terminate the application
                    if len([button for button in gamepads[fd]["buttons_pressed"] if button]) == len(
                            gamepads[fd]["buttons"]):
                        if mode == "debug":
                            print("PS button and terminate buttons pressed")
                        for process in psutil.process_iter():
                            if procName.lower() in [line.lower() for line in process.cmdline()]:
                                if mode == "debug":
                                    print('Process found. Terminating it.')
                                process.terminate()
                                print('Process terminated due to button event')
                                active = False
                                exit()
                                break
    except Exception as e:
        print(e)
        active = False
