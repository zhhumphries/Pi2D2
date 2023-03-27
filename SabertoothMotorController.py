import serial
import time
from abc import ABC, abstractmethod
from MotorControllerInterface import MotorControllerInterface

class SabertoothMotorController(MotorControllerInterface):
    def __init__(self, file = '/dev/ttyS0'):
        self.serial_port = serial.Serial(
            port=file,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.motor0_speed = 0
        self.motor1_speed = 0

    def __del__(self):
        self.serial_port.close()

    def calculate_checksum(self, address, command, data):
        return (address + command + data) & 0b01111111

    def send_sabertooth_command(self, command, data):
        address = 128 # Default address for Packetized Serial mode
        checksum = self.calculate_checksum(address, command, data)
        command_packet = bytearray([address, command, data, checksum])
        self.serial_port.write(command_packet)

    # The Sabertooth motor controller uses a different speed range for each motor
    # Motor 1: 0-127 (0 is stop and 127 is full speed forward)
    # Motor 2: 128-255 (128 is stop and 255 is full speed forward)
    # This function input is assumed to be a value between -1 and 1. It then
    # calculates the Sabertooth command and speed based on the input speed
    def set_motor_speed(self, motor_number, speed):
        print("Setting motor speed: " + str(speed) + " for motor " + str(motor_number))
        # Calculate the Sabertooth command and speed based on the input speed
        if speed >= 0:
            print("Speed is positive")
            command = 0 if motor_number == 0 else 4
            sabertooth_speed = int(speed * 127)
        else:
            print("Speed is negative")
            command = 1 if motor_number == 0 else 5
            sabertooth_speed = int(-speed * 127)
        print("Sabertooth command: " + str(command) + ", Sabertooth speed: " + str(sabertooth_speed))
        self.send_sabertooth_command(command, sabertooth_speed)

    def stop_motor(self, motor_number):
        # Determine the motor speed based on the motor_number
        if motor_number == 0:
            current_speed = self.motor0_speed
        elif motor_number == 1:
            current_speed = self.motor1_speed
        else:
            return

        # Gradually ramp down the motor speed
        ramp_increment = 0.5  # increment for each step
        if current_speed < 0:
            current_speed += ramp_increment
            if current_speed > 0:
                current_speed = 0
        elif current_speed > 0:
            current_speed -= ramp_increment
            if current_speed < 0:
                current_speed = 0
        
        if motor_number == 0:
            self.set_motor_speeds(current_speed, self.motor1_speed)
            self.motor0_speed = current_speed
        elif motor_number == 1:
            self.set_motor_speeds(self.motor0_speed, current_speed)
            self.motor1_speed = current_speed

    def stop_all_motors(self):
        self.stop_motor(0)
        self.stop_motor(1)

    def smoothed_set_motor_speed(self, speed_0, speed_1):
        # Limit the speed to a range of -0.7 to 0.7
        if (speed_0 > 0.7):
            speed_0 = 0.7
        elif (speed_0 < -0.7):
            speed_0 = -0.7

        if (speed_1 > 0.7):
            speed_1 = 0.7
        elif (speed_1 < -0.7):
            speed_1 = -0.7

        # Gradually ramp up the motor speed
        ramp_steps = 3  # number of steps to ramp up
        ramp_increment_0 = speed_0 / ramp_steps  # increment for each step
        ramp_increment_1 = speed_1 / ramp_steps  # increment for each step
        current_speed_0 = self.motor0_speed
        current_speed_1 = self.motor1_speed

        current_speed_0 += ramp_increment_0
        current_speed_1 += ramp_increment_1

        if (speed_0 > 0):
            if (current_speed_0 > speed_0):
                current_speed_0 = speed_0
        else:
            if (current_speed_0 < speed_0):
                current_speed_0 = speed_0

        if (speed_1 > 0):
            if (current_speed_1 > speed_1):
                current_speed_1 = speed_1
        else:
            if (current_speed_1 < speed_1):
                current_speed_1 = speed_1

        self.set_motor_speeds(current_speed_0, current_speed_1)
        self.motor0_speed = current_speed_0
        self.motor1_speed = current_speed_1

    def set_motor_speeds(self, motor_1_speed, motor_2_speed):
        print("Setting motor speeds: " + str(motor_1_speed) + ", " + str(motor_2_speed))
        self.set_motor_speed(0, motor_1_speed)
        self.set_motor_speed(1, motor_2_speed)

    def move_forward(self, speed):
        ramp_steps = 20  # number of steps to ramp up
        ramp_increment = speed / ramp_steps  # increment for each step
        current_speed = self.motor0_speed
        current_speed += ramp_increment
        if (current_speed > speed):
            current_speed = speed
        self.set_motor_speeds(current_speed, current_speed)
        self.motor0_speed = current_speed
        self.motor1_speed = current_speed

    def move_backward(self, speed):
        ramp_steps = 3  # number of steps to ramp up
        ramp_increment = speed / ramp_steps  # increment for each step
        current_speed = self.motor0_speed
        current_speed -= ramp_increment
        if (current_speed < -speed):
            current_speed = -speed
        self.set_motor_speeds(current_speed, current_speed)
        self.motor0_speed = current_speed
        self.motor1_speed = current_speed

    def turn_left(self, speed):
        print("Turning left at speed: " + str(speed))
        ramp_steps = 8  # number of steps to ramp up
        ramp_increment = speed / ramp_steps  # increment for each step
        current_speed = self.motor0_speed
        current_speed -= ramp_increment
        if (current_speed < -speed):
            current_speed = -speed
        self.set_motor_speeds(current_speed, -current_speed)
        self.motor0_speed = current_speed
        self.motor1_speed = -current_speed

    def turn_right(self, speed):
        print("Turning right at speed: " + str(speed))
        ramp_steps = 8  # number of steps to ramp up
        ramp_increment = speed / ramp_steps  # increment for each step
        current_speed = self.motor0_speed
        current_speed += ramp_increment
        if (current_speed > speed):
            current_speed = speed
        self.set_motor_speeds(current_speed, -current_speed)
        self.motor0_speed = current_speed
        self.motor1_speed = -current_speed

    def stop(self):
        self.stop_all_motors()

    def move_forward_left(self, speed):
        self.set_motor_speeds(0, speed)

    def move_forward_right(self, speed):
        self.set_motor_speeds(speed, 0)

    def move_backward_left(self, speed):
        self.set_motor_speeds(0, -speed)

    def move_backward_right(self, speed):
        self.set_motor_speeds(-speed, 0)
