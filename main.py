#import evdev
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
from XboxGamepad import XboxGamepad

async def removetasks(loop):
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]

    for task in tasks:
        # skipping over shielded coro still does not help
        if task._coro.__name__ == "cant_stop_me":
            continue
        task.cancel()

    print("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def shutdown_signal(signal, loop):
    print(f"Received exit signal {signal.name}...")
    await removetasks(loop)

if __name__ == "__main__":
    devices = [InputDevice(path) for path in list_devices()]
    print('Connecting to xbox controller...')
    xbox_path = None
    remote_control = None
    for device in devices:
        if str.lower(device.name) == 'xbox wireless controller':
            xbox_path = str(device.path)
            remote_control = XboxGamepad(file = xbox_path)

    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown_signal(s, loop)))
    try:
        if(remote_control == None):
            print('Please connect an Xbox controller then restart the program!')
            sys.exit()
        tasks = [remote_control.read_gamepad_input()]
        try:
            loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))
        except asyncio.CancelledError:
            pass
        loop.run_until_complete(removetasks(loop))
    except Exception as e:
        print("Error occured " + str(e))
    finally:
        if remote_control != None:
            remote_control.power_on = False
        print("Closing async loop..")
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("Done..")
