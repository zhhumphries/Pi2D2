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

class gamepad():
    def __init__(self, file = '/dev/input/event3'):
        #self.event_value = 0
        self.power_on = True
        self.device_file = InputDevice(file)
        self.joystick_left_y = 0 # values are mapped to [-1 ... 1]
        self.joystick_left_x = 0 # values are mapped to [-1 ... 1]
        self.joystick_right_x = 0 # values are mapped to [-1 ... 1]
        self.joystick_right_y = 0 # values are mapped to [-1 ... 1]
        self.trigger_right = 0 # values are mapped to [0 ... 1]
        self.trigger_left = 0 # values are mapped to [0 ... 1]
        self.button_x = False
        self.button_y = False
        self.button_b = False
        self.button_a = False
        self.dpad_up = False
        self.dpad_down = False
        self.dpad_left = False
        self.dpad_right = False
        self.bump_left = False
        self.bump_right = False
        self.rumble_effect = 0
        self.effect1_id = 0 # light rumble, played continuously
        self.effect2_id = 0 # strong rumble, played once
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

    async def read_gamepad_input(self): # asyncronus read-out of events
        max_abs_joystick_left_x = 0xFFFF/2
        uncertainty_joystick_left_x = 2500
        max_abs_joystick_left_y = 0xFFFF/2
        uncertainty_joystick_left_y = 2500
        max_abs_joystick_right_x = 0xFFFF/2
        uncertainty_joystick_right_x = 2000
        max_abs_joystick_right_y = 0xFFFF/2
        uncertainty_joystick_right_y = 2000
        max_trigger = 1023

        async for event in self.device_file.async_read_loop():
            if not(self.power_on): #stop reading device when power_on = false
                break
            #print(str(event.type) + ' ' + str(event.code) + ' ' + str(event.value))
            if event.type == 3: # type is analog trigger or joystick
                if event.code == 1: # left joystick y-axis
                    if abs(event.value) > uncertainty_joystick_left_y:
                        #print('Left Y-axis ' + str(event.value))
                        self.joystick_left_y = (-event.value - uncertainty_joystick_left_y) / (max_abs_joystick_left_y - uncertainty_joystick_left_y + 1)
                    else:
                        self.joystick_left_y = 0
                elif event.code == 0: # left joystick x-axis
                    if abs(event.value) > uncertainty_joystick_left_x:
                        #print('Left X-axis ' + str(event.value))
                        self.joystick_left_x = (event.value - uncertainty_joystick_left_x) / (max_abs_joystick_left_x - uncertainty_joystick_left_x + 1)
                    else:
                        self.joystick_left_x = 0
                elif event.code == 3: # right joystick x-axis
                    if event.value > uncertainty_joystick_right_x:
                        self.joystick_right_x = (event.value - uncertainty_joystick_right_x) / (max_abs_joystick_right_x - uncertainty_joystick_right_x + 1)
                    elif event.value < -uncertainty_joystick_right_x:
                        self.joystick_right_x = (event.value + uncertainty_joystick_right_x) / (max_abs_joystick_right_x - uncertainty_joystick_right_x + 1)
                    else:
                        self.joystick_right_x = 0
                elif event.code == 4: # right joystick y-axis
                    if -event.value > uncertainty_joystick_right_y:
                        self.joystick_right_y = (-event.value - uncertainty_joystick_right_y) / (max_abs_joystick_right_y - uncertainty_joystick_right_y + 1)
                    elif -event.value < -uncertainty_joystick_left_y:
                        self.joystick_right_y = (-event.value + uncertainty_joystick_right_y) / (max_abs_joystick_right_y - uncertainty_joystick_right_y + 1)
                    else:
                        self.joystick_right_y = 0
                elif event.code == 9: # right trigger
                    self.send_motor1_command(int(128 * (event.value / max_trigger)), 0)
                    self.trigger_right = event.value / max_trigger
                elif event.code == 10: # left trigger
                    # Go reverse
                    self.send_motor1_command(int(128 * (event.value / max_trigger)), 1)
                    self.trigger_left = event.value / max_trigger
                elif event.code == 16: # right trigger
                    if(event.value == -1):
                        self.dpad_left = True
                        self.dpad_right = False
                    elif(event.value == 1):
                        self.dpad_left = False
                        self.dpad_right = True
                    else:
                        self.dpad_left = False
                        self.dpad_right = False
                elif event.code == 17: # left trigger
                    if(event.value == -1):
                        self.dpad_up = True
                        self.dpad_down = False
                    elif(event.value == 1):
                        self.dpad_up = False
                        self.dpad_down = True
                    else:
                        self.dpad_up = False
                        self.dpad_down = False
            if (event.type == 1): # type is button
                if event.code == 304: # button "A" pressed ?
                    self.button_a =  True
                if event.code == 307: # button "X" pressed ?
                    self.button_x = True
                if event.code == 308: # button "Y" pressed ?
                    self.button_y = True
                if event.code == 305: # button "B" pressed ?
                    self.button_b = True
                if event.code == 311: # bumper "right" pressed ?
                    self.bump_right = True if event.value == 1 else False
                if event.code == 310: # bumper "left" pressed ?
                    self.bump_left = True if event.value == 1 else False