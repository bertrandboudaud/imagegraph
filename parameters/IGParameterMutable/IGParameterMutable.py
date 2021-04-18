from IGParameter import *
from PIL import Image
import copy

class IGParameterMutable(IGParameter):
    def __init__(self):
        super().__init__("Generic Output")
        self._value = None
        self.user_parameter = None

    @property
    def value(self):
        return self._value["value"]

    @value.setter
    def value(self, value):
        self._value["value"] = value

    def notify_connected_to(self, other_parameter):
        print("connect_to")
        self.user_parameter = copy.copy(other_parameter)

    @property
    def type(self):
        if self.user_parameter:
            return self.user_parameter.type
        else:
            return self._type
    
    def __getattr__( self, name):
        if self.user_parameter:
            return self.user_parameter.__getattribute__(name)