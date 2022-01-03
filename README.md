# retropie-pcsx2-wrapper
This is a wrapper for PCSX2 for Retropie, it uses a simple python wrapper to intercept a key combination to exit the emulator on keypress

Generic python script to kill some application using a gamepad.

The specific usecase in mind: Some emulators do not allow to be exited with a gamepad, but only with a keyboard.


## Installation
Copy (or better symlink) everything but the README to /opt/retropie/configs/all.
Note: The config file must be present in the directory of the original python script, not the symlink.

This Python script requires ```evdev```, ```psutil``` and ```json``` which can both be installed using pip

`pip install evdev`

`pip install psutil`

Make the scripts executable

`chmod +x runcommand-onstart.sh`

`chmod +x runcommand-onend.sh`

`chmod +x gamepad_wrapper.py`

## Configuration
Find the json file in the directory of the python script.
In there, you must configure your gamepad device name, the buttons which need to be pressed and the application which shall be killed.
See the following commented example (this will not be usable, since comments are not supported in json):
```
{
	# With the dev_config entry the controller names and buttons are configured
	# Run the python script manually with the argument "test" to see the connected controllers and button presses
	"dev_config": {
		"Xbox Wireless Controller": {  # All controllers with this name will be allowed to kill the application
			"buttons": [158, 315]  # Arbitrary number of buttons, which must be hold down at the same time. However, the first one is acting as a hotkey enable and must be pressed first.
		}
	},
	# With proc_names the platforms of retropie are mapped to the application paths.
	# Upper/lowercase is not regarded
	"proc_names": {
		"ps2": "/usr/games/PCSX2"
	},
	# Change mode to "debug" to see additional output of the python script
	# Change mode to "test" to be in dummy mode (no application will be killed). Can be useful for configuration. Just pass any argument.
	"mode": "normal"
}
```

### runcommand-onstart.sh
This bash script is executed by RetroArch when any ROM is loaded. This executes the gamepad_wrapper.py script and passes the platform as argument.

### gamepad_wrapper.py
This Python script requires ```evdev``` and ```psutil``` and ```json``` which can both be installed using pip

This will start a Python listener using evdev that upon the specified key press will kill the specified app

You may need to edit the following line 

```gamepad = InputDevice('/dev/input/event19')```

And edit /dev/input/event19 with whichever one your controller is recognized as

When the specified key combo is pressed, it will kill the PCSX2 process, then RetroArch will run the runcommand-onend.sh script

### runcommand-onend.sh
This Script is executed by RetroArch when the emulator exits and is only here to cleanup the Python wrapper process

## Usage
There should be nothing additional needed as these scripts should execute each time that RetroArch uses runcommand to launch an emulator

