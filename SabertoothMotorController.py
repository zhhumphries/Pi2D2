import serial
import time
from abc import ABC, abstractmethod
import MotorControllerInterface

class SabertoothMotorContoller(MotorControllerInterface):
    def __init__(self, file = '/dev/ttyS0'):
        self.serial_port = serial.Serial(
            port=file,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
    def __del__(self):
        self.serial_port.close()

    def calculate_checksum(self, address, command, data):
        return (address + command + data) & 0b01111111

    def send_sabertooth_command(self, motor_number, command, speed):
        address = 128 # Default address for Packetized Serial mode
        data = speed if motor_number == 0 else speed + 128
        checksum = self.calculate_checksum(address, command, data)
        command_packet = bytearray([address, command, data, checksum])
        self.serial_port.write(command_packet)

    # The Sabertooth motor controller uses a different speed range for each motor
    # Motor 1: 0-127 (0 is stop and 127 is full speed forward)
    # Motor 2: 128-255 (128 is stop and 255 is full speed forward)
    # This function normalizes the input speed (of -100 to 100) to a value between
    # -1 and 1 and then calculates the Sabertooth command and speed based on the
    # input speed
    def set_motor_speed(self, motor_number, speed):
        # Normalize the input speed to a value between -1 and 1
        normalized_speed = speed / 100

        # Calculate the Sabertooth command and speed based on the input speed
        if normalized_speed >= 0:
            command = 0
            if motor_number == 0:
                sabertooth_speed = int(normalized_speed * 127)
            else:
                sabertooth_speed = int(normalized_speed * (255 - 128)) + 128
        else:
            command = 1
            if motor_number == 0:
                sabertooth_speed = int(-normalized_speed * 127)
            else:
                sabertooth_speed = int(-normalized_speed * (255 - 128)) + 128

        self.send_sabertooth_command(motor_number, command, sabertooth_speed)

    def stop_motor(self, motor_number):
        speed = 0 if motor_number == 0 else 128
        self.send_sabertooth_command(motor_number, 0, speed)

    def stop_all_motors(self):
        self.stop_motor(0)
        self.stop_motor(1)

    def set_motor_speeds(self, motor_1_speed, motor_2_speed):
        self.set_motor_speed(0, motor_1_speed)
        self.set_motor_speed(1, motor_2_speed)

    def move_forward(self, speed):
        self.set_motor_speeds(speed, speed)

    def move_backward(self, speed):
        self.set_motor_speeds(-speed, -speed)

    def turn_left(self, speed):
        self.set_motor_speeds(-speed, speed)

    def turn_right(self, speed):
        self.set_motor_speeds(speed, -speed)

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
