from evdev import InputDevice, categorize, ecodes, list_devices
import psutil
from subprocess import Popen

#creates object 'gamepad' to store the data
#you can call it whatever you like
# you will need to check /dev/input for your specific device name like eventXX


devices = [InputDevice(path) for path in list_devices()]
for device in devices:
   if device.name == "Microntek              USB Joystick          ":
      devicePath = device.path

gamepad = InputDevice(devicePath)

#button code variables (change to suit your device)
# More information from https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html
button1 = 316
button2 = 315

# Process to look for to kill when BOTH keys are pressed
procName = '/usr/games/PCSX2'

#loop and filter by event code and print the mapped label
counter = 0
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            # Button pressed
            print("pressed")
            print(event.code)
            if event.code == button1 or event.code == button2:
                counter += 1
        if event.value == 0:
            # Button released
            print("released")
            print(event.code)
            if event.code == button1 or event.code == button2:
                counter -= 1
    if counter <= 0:
        counter = 0
    elif counter >= 2:
        print("PS Button and Start Pressed")
        for process in psutil.process_iter():
            if procName in process.cmdline():
                print('Process found. Terminating it.')
                process.terminate()
                exit()
                break
