from evdev import InputDevice, categorize, ecodes, list_devices
import psutil


############# Configuration ##############

mode = "normal"  # change to debug for additional output

#button code variables (change to suit your device)
# More information from https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html
# Change mode to debug to see your button presses (run script manually)
button1 = 314
button2 = 315

# Process to look for to kill when BOTH keys are pressed
procName = '/usr/games/PCSX2'


############# Functionality ##############

devices = [InputDevice(path) for path in list_devices()]
devicePath = ""
if mode == "debug":
    print("Available devices:")
for device in devices:
    if mode == "debug":
        print(device.name)
    if device.name == "Xbox Wireless Controller":
        devicePath = device.path

if mode == "debug":
    print("Chosen device path: ", devicePath)
if devicePath == "":
    print("Specified device not found. Exiting...")
    exit()

gamepad = InputDevice(devicePath)

#loop and filter by event code and print the mapped label
counter = 0
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            # Button pressed
            if mode == "debug":
                print("Button Pressed")
                print(event.code)
                if event.code in ecodes.KEY:
                    print(ecodes.KEY[event.code])
            if event.code == button1 or event.code == button2:
                counter += 1
        if event.value == 0:
            # Button released
            if mode == "debug":
                print("Button Released")
                print(event.code)
                if event.code in ecodes.KEY:
                    print(ecodes.KEY[event.code])
            if event.code == button1 or event.code == button2:
                counter -= 1
    if counter <= 0:
        counter = 0
    elif counter >= 2:
        if mode == "debug":
            print("PS Button and Start Pressed")
        for process in psutil.process_iter():
            if procName in process.cmdline():
                if mode == "debug":
                    print('Process found. Terminating it.')
                process.terminate()
                print('Process terminated due to button event')
                exit()
                break
