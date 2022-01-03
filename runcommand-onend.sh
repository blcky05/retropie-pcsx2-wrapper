#!/bin/bash
#kill python wrapper script if found
PROCS=$(ps aux | grep gamepad_wrapper.py | awk '{ print $2 }')
for PROC in ${PROCS[@]}
do
	kill "$PROC"
done