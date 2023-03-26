from abc import ABC, abstractmethod

class GamepadInterface(ABC):

    # This method is called by the main thread to read the left joystick
    # x-axis value. The value is mapped to [-1 ... 1].
    @abstractmethod
    def get_left_joystick_x(self):
        pass

    # This method is called by the main thread to read the left joystick
    # y-axis value. The value is mapped to [-1 ... 1].
    @abstractmethod
    def get_left_joystick_y(self):
        pass

    # This method is called by the main thread to read the right joystick
    # x-axis value. The value is mapped to [-1 ... 1].
    @abstractmethod
    def get_right_joystick_x(self):
        pass

    # This method is called by the main thread to read the right joystick
    # y-axis value. The value is mapped to [-1 ... 1].
    @abstractmethod
    def get_right_joystick_y(self):
        pass

    # This method is called by the main thread to read the left trigger
    # value. The value is mapped to [0 ... 1].
    @abstractmethod
    def get_left_trigger(self):
        pass

    # This method is called by the main thread to read the right trigger
    # value. The value is mapped to [0 ... 1].
    @abstractmethod
    def get_right_trigger(self):
        pass

    # This method is called by the main thread to read the left bumper
    # value. The value is either true or false.
    @abstractmethod
    def get_left_bumper(self):
        pass

    # This method is called by the main thread to read the right bumper
    # value. The value is either true or false.
    @abstractmethod
    def get_right_bumper(self):
        pass

    # This method is called by the main thread to read the south button
    # value. The value is either true or false.
    @abstractmethod
    def get_button_south(self):
        pass

    # This method is called by the main thread to read the east button
    # value. The value is either true or false.
    @abstractmethod
    def get_button_east(self):
        pass

    # This method is called by the main thread to read the west button
    # value. The value is either true or false.
    @abstractmethod
    def get_button_west(self):
        pass

    # This method is called by the main thread to read the north button
    # value. The value is either true or false.
    @abstractmethod
    def get_button_north(self):
        pass

    # This method is called by the main thread to read the dpad up button
    # value. The value is either true or false.
    @abstractmethod
    def get_dpad_up(self):
        pass

    # This method is called by the main thread to read the dpad down button
    # value. The value is either true or false.
    @abstractmethod
    def get_dpad_down(self):
        pass

    # This method is called by the main thread to read the dpad left button
    # value. The value is either true or false.
    @abstractmethod
    def get_dpad_left(self):
        pass

    # This method is called by the main thread to read the dpad right button
    # value. The value is either true or false.
    @abstractmethod
    def get_dpad_right(self):
        pass

    # This method is called by the main thread to read the back button
    # value. The value is either true or false.
    @abstractmethod
    def get_button_back(self):
        pass

    # This method is called by the main thread to read the start button
    # value. The value is either true or false.
    @abstractmethod
    def get_button_start(self):
        pass