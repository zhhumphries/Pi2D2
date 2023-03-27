from evdev import InputDevice, categorize, ecodes, list_devices
import asyncio
import math
import os
import serial
import signal
import subprocess
import sys
import threading
import time
from DriveManager import DriveManager
from SabertoothMotorController import SabertoothMotorController
from XboxGamepad import XboxGamepad

# Function to cancel all outstanding tasks and stop the event loop
async def removetasks(loop):
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]
    for task in tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    loop.stop()

# Function to handle shutdown signals
async def shutdown_signal(signal, loop):
    print(f"Received exit signal {signal.name}...")
    await removetasks(loop)

def main():
    # Get a list of connected input devices
    devices = [InputDevice(path) for path in list_devices()]
    print('Connecting to xbox controller...')
    xbox_path = None
    remote_control = None
    motor_controller = None
    driver_manager = None
    # Look for an Xbox wireless controller and create an instance of XboxGamepad if found
    for device in devices:
        if str.lower(device.name) == 'xbox wireless controller':
            xbox_path = str(device.path)
            remote_control = XboxGamepad(file = xbox_path)

    motor_controller = SabertoothMotorController()
    
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    # Register signal handlers to cleanly shutdown the program
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown_signal(s, loop)))
    try:
        # If no Xbox controller is found, exit the program
        if(remote_control == None):
            print('Please connect an Xbox controller then restart the program!')
            sys.exit()
        if (motor_controller == None):
            print('Please connect a Sabertooth motor controller then restart the program!')
            sys.exit()
        driver_manager = DriveManager(remote_control, motor_controller)
        if (driver_manager == None):
            print('Error creating DriveManager')
            sys.exit()

        # Run the gamepad input task until it completes or is cancelled
        tasks = [remote_control.read_gamepad_input(), driver_manager.process_gamepad_input()]
        try:
            loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))
        except asyncio.CancelledError:
            pass
        # Stop all outstanding tasks and close the event loop
        loop.run_until_complete(removetasks(loop))
    except Exception as e:
        print("Error occurred " + str(e))
    finally:
        if remote_control != None:
            remote_control.power_on = False
        print("Closing async loop..")
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("Done..")

if __name__ == "__main__":
    main()