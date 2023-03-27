import asyncio
from XboxGamepad import XboxGamepad
from SabertoothMotorController import SabertoothMotorController

class DriveManager:
    def __init__(self, gamepad: XboxGamepad, motor_controller: SabertoothMotorController):
        self.gamepad = gamepad
        self.motor_controller = motor_controller

    async def process_gamepad_input(self):
        while self.gamepad.power_on:
            await asyncio.sleep(0.1) # Yield control back to the event loop to avoid blocking
            if (self.gamepad.get_left_bumper() == True):
                self.motor_controller.turn_left(0.4)
            elif (self.gamepad.get_right_bumper() == True):
                self.motor_controller.turn_right(0.4)
            elif (self.gamepad.get_left_trigger() > 0):
                self.motor_controller.move_backward(self.gamepad.get_left_trigger() * 0.25) #multiply by a factor to reduce whiplash
            elif (self.gamepad.get_right_trigger() > 0):
                self.motor_controller.move_forward(self.gamepad.get_right_trigger())
            elif (self.gamepad.get_left_joystick_y() > 0 or self.gamepad.get_left_joystick_y() < 0 or self.gamepad.get_left_joystick_x() > 0 or self.gamepad.get_left_joystick_x() < 0):
                # Calculate the desired speed and direction for each motor
                y = -self.gamepad.get_left_joystick_y()
                x = self.gamepad.get_left_joystick_x()
                turn_factor = 0.5
                max_speed = 0.3
                left_speed = y + x
                right_speed = y - x

                # Scale the speeds to the maximum speed
                if abs(left_speed) > max_speed or abs(right_speed) > max_speed:
                    max_input = max(abs(left_speed), abs(right_speed))
                    left_speed /= max_input
                    right_speed /= max_input
                left_speed *= max_speed
                right_speed *= max_speed

                # # Adjust the motor speeds based on the turn factor
                # if x < 0:
                #     left_speed *= 1 + turn_factor * abs(x)
                # elif x > 0:
                #     right_speed *= 1 + turn_factor * x
                print("Left speed: " + str(left_speed) + ", Right speed: " + str(right_speed))
                self.motor_controller.smoothed_set_motor_speed(left_speed, right_speed)
                
            else:
                self.motor_controller.stop()

    async def stop(self):
        self.motor_controller.stop()