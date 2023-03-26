from abc import ABC, abstractmethod

class MotorControllerInterface(ABC):

    @abstractmethod
    def move_forward(self, speed):
        pass

    @abstractmethod
    def move_backward(self, speed):
        pass

    @abstractmethod
    def turn_left(self, speed):
        pass

    @abstractmethod
    def turn_right(self, speed):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def move_forward_left(self, speed):
        pass

    @abstractmethod
    def move_forward_right(self, speed):
        pass

    @abstractmethod
    def move_backward_left(self, speed):
        pass

    @abstractmethod
    def move_backward_right(self, speed):
        pass