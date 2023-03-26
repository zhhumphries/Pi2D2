from evdev import InputDevice, categorize, ecodes

from GamepadInterface import GamepadInterface

class XboxGamepad(GamepadInterface):

    def __init__(self, file = '/dev/input/event3'):
        self.power_on = True
        self.device_file = InputDevice(file)
        self.joystick_left_y = 0 # values are mapped to [-1 ... 1]
        self.joystick_left_x = 0 # values are mapped to [-1 ... 1]
        self.joystick_right_x = 0 # values are mapped to [-1 ... 1]
        self.joystick_right_y = 0 # values are mapped to [-1 ... 1]
        self.trigger_right = 0 # values are mapped to [0 ... 1]
        self.trigger_left = 0 # values are mapped to [0 ... 1]
        self.button_x = False # values are mapped to true or false
        self.button_y = False # values are mapped to true or false
        self.button_b = False # values are mapped to true or false
        self.button_a = False # values are mapped to true or false
        self.dpad_up = False # values are mapped to true or false
        self.dpad_down = False # values are mapped to true or false
        self.dpad_left = False # values are mapped to true or false
        self.dpad_right = False # values are mapped to true or false
        self.bump_left = False # values are mapped to true or false
        self.bump_right = False # values are mapped to true or false
        self.stick_left = False # values are mapped to true or false
        self.stick_right = False # values are mapped to true or false
        self.button_back = False # values are mapped to true or false
        self.button_start = False # values are mapped to true or false
        self.button_guide = False # values are mapped to true or false
        self.button_record = False # values are mapped to true or false
        self.rumble_effect = 0 # values are mapped to 0, 1, or 2??
        self.effect1_id = 0 # light rumble, played continuously
        self.effect2_id = 0 # strong rumble, played once

    # --------------------------------------------
    # GamepadInterface methods
    # --------------------------------------------
    # This method is called by the main thread to read the left joystick
    # x-axis value. The value is mapped to [-1 ... 1].
    def get_left_joystick_x(self):
        return self.joystick_left_x

    # This method is called by the main thread to read the left joystick
    # y-axis value. The value is mapped to [-1 ... 1].
    def get_left_joystick_y(self):
        return self.joystick_left_y

    # This method is called by the main thread to read the right joystick
    # x-axis value. The value is mapped to [-1 ... 1].
    def get_right_joystick_x(self):
        return self.joystick_right_x

    # This method is called by the main thread to read the right joystick
    # y-axis value. The value is mapped to [-1 ... 1].
    def get_right_joystick_y(self):
        return self.joystick_right_y

    # This method is called by the main thread to read the left trigger
    # value. The value is mapped to [0 ... 1].
    def get_left_trigger(self):
        return self.trigger_left

    # This method is called by the main thread to read the right trigger
    # value. The value is mapped to [0 ... 1].
    def get_right_trigger(self):
        return self.trigger_right

    # This method is called by the main thread to read the left bumper
    # value. The value is either true or false.
    def get_left_bumper(self):
        return self.bump_left

    # This method is called by the main thread to read the right bumper
    # value. The value is either true or false.
    def get_right_bumper(self):
        return self.bump_right

    # This method is called by the main thread to read the south button
    # value. The value is either true or false.
    def get_button_south(self):
        return self.button_a

    # This method is called by the main thread to read the east button
    # value. The value is either true or false.
    def get_button_east(self):
        return self.button_b

    # This method is called by the main thread to read the west button
    # value. The value is either true or false.
    def get_button_west(self):
        return self.button_x

    # This method is called by the main thread to read the north button
    # value. The value is either true or false.
    def get_button_north(self):
        return self.button_y

    # This method is called by the main thread to read the dpad up button
    # value. The value is either true or false.
    def get_dpad_up(self):
        return self.dpad_up

    # This method is called by the main thread to read the dpad down button
    # value. The value is either true or false.
    def get_dpad_down(self):
        return self.dpad_down

    # This method is called by the main thread to read the dpad left button
    # value. The value is either true or false.
    def get_dpad_left(self):
        return self.dpad_left

    # This method is called by the main thread to read the dpad right button
    # value. The value is either true or false.
    def get_dpad_right(self):
        return self.dpad_right

    # This method is called by the main thread to read the back button
    # value. The value is either true or false.
    def get_button_back(self):
        return self.button_back

    # This method is called by the main thread to read the start button
    # value. The value is either true or false.
    def get_button_start(self):
        return self.button_start

    # This method is called by the main thread to set the light rumble
    # value. The value is mapped to [0 ... 1].
    def set_light_rumble(self, value):
        self.effect1_id = value
        self.rumble_effect = value

    # This method is called by the main thread to set the strong rumble
    # value. The value is mapped to [0 ... 1].
    def set_heavy_rumble(self, value):
        self.effect2_id = value
        self.rumble_effect = value
    # --------------------------------------------
    # End of GamepadInterface methods
    # --------------------------------------------

    # --------------------------------------------
    # XboxGamepad methods
    # --------------------------------------------
    
    # This method is called by the main thread to set the power_on value
    # value. The value is mapped to true or false.
    def set_power_on(self, value):
        self.power_on = value
    
    # This method is called by the main thread to read the stick_left value
    # value. The value is mapped to true or false.
    def get_stick_left(self):
        return self.stick_left
    
    # This method is called by the main thread to read the stick_right value
    # value. The value is mapped to true or false.
    def get_stick_right(self):
        return self.stick_right

    # This method is called by the main thread to read the button_record value
    # value. The value is mapped to true or false.
    def get_button_record(self):
        return self.button_record

    # This method is called by the main thread to read the button_guide value
    # value. The value is mapped to true or false.
    def get_button_guide(self):
        return self.button_guide
    
    async def read_gamepad_input(self): # asyncronus read-out of events
        max_abs_joystick_left_x = 0x7FFF
        uncertainty_joystick_left_x = 2500
        max_abs_joystick_left_y = 0x7FFF
        uncertainty_joystick_left_y = 2500
        max_abs_joystick_right_x = 0x7FFF
        uncertainty_joystick_right_x = 2500
        max_abs_joystick_right_y = 0x7FFF
        uncertainty_joystick_right_y = 2500
        max_trigger = 1023

        def constrain(value, min_value, max_value):
            if value < min_value:
                return min_value
            elif value > max_value:
                return max_value
            else:
                return value

        async for event in self.device_file.async_read_loop():
            if not(self.power_on): #stop reading device when power_on = false
                break
            print(str(event) + ' ' + str(categorize(event)))
            if (event.type == ecodes.EV_KEY): # type is button
                if (event.code == 167): # code is button record
                    self.button_record = event.value
                elif (event.code == 304): # code is button A
                    self.button_a = event.value
                elif (event.code == 305): # code is button B
                    self.button_b = event.value
                elif (event.code == 307): # code is button X
                    self.button_x = event.value
                elif (event.code == 308): # code is button Y
                    self.button_y = event.value
                elif (event.code == 310): # code is button left bumper
                    self.bump_left = event.value
                elif (event.code == 311): # code is button right bumper
                    self.bump_right = event.value
                elif (event.code == 314): # code is button back
                    self.button_back = event.value
                elif (event.code == 315): # code is button start
                    self.button_start = event.value
                elif (event.code == 317): # code is button left stick
                    self.stick_left = event.value
                elif (event.code == 318): # code is button right stick
                    self.stick_right = event.value
                elif (event.code == 316): # code is button guide
                    self.button_guide = event.value
            elif (event.type == ecodes.EV_ABS): # type is axis
                if (event.code == 0): # code is left joystick x-axis
                    if (abs(abs(event.value) - max_abs_joystick_left_x) > uncertainty_joystick_left_x):
                        self.joystick_left_x = constrain((event.value / max_abs_joystick_left_x) - 1, -1, 1)
                    else:
                        self.joystick_left_x = 0
                elif (event.code == 1): # code is left joystick y-axis
                    if (abs(abs(event.value) - max_abs_joystick_left_y) > uncertainty_joystick_left_y):
                        self.joystick_left_y = constrain((event.value / max_abs_joystick_left_y) - 1, -1, 1)
                    else:
                        self.joystick_left_y = 0
                elif (event.code == 2): # code is right joystick x-axis
                    if (abs(abs(event.value) - max_abs_joystick_right_x) > uncertainty_joystick_right_x):
                        self.joystick_right_x = constrain((event.value / max_abs_joystick_right_x) - 1, -1, 1)
                    else:
                        self.joystick_right_x = 0
                elif (event.code == 5): # code is right joystick y-axis
                    if (abs(abs(event.value) - max_abs_joystick_right_y) > uncertainty_joystick_right_y):
                        self.joystick_right_y = constrain((event.value / max_abs_joystick_right_y) - 1, -1, 1)
                    else:
                        self.joystick_right_y = 0
                elif (event.code == 9): # code is right trigger
                    self.trigger_right = event.value / max_trigger
                elif (event.code == 10): # code is left trigger
                    self.trigger_left = event.value / max_trigger
                elif (event.code == 16): # code is dpad left/right
                    if (event.value == -1):
                        self.dpad_left = True
                    elif (event.value == 1):
                        self.dpad_right = True
                    else:
                        self.dpad_left = False
                        self.dpad_right = False
                elif (event.code == 17): # code is dpad up/down
                    if (event.value == -1):
                        self.dpad_up = True
                    elif (event.value == 1):
                        self.dpad_down = True
                    else:
                        self.dpad_up = False
                        self.dpad_down = False
    # --------------------------------------------
    # End of XboxGamepad methods
    # --------------------------------------------    