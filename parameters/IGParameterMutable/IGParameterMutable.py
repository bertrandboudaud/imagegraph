from IGParameter import *
from PIL import Image
import copy

class IGParameterMutable(IGParameter):
    def __init__(self):
        super().__init__("Generic Output")
        self.user_parameter = None

    def on_connected_to(self, other_parameter):
        self.mute_to(other_parameter)

    def mute_to(self, other_parameter):
        self.user_parameter = copy.copy(other_parameter)
        self.set_value(other_parameter)

    def get_value(self):
        if self.user_parameter:
            return self.user_parameter.get_value()
        else:
            return None

    def set_value(self, other_parameter):
        self.user_parameter.set_value(other_parameter)

    def backup_value(self):
        self._backup_value = copy.deepcopy(self.get_value())

    def restore_backup_value(self):
        self.user_parameter.set_value(_backup_value)

    @property
    def type(self):
        if self.user_parameter:
            return self.user_parameter.type
        else:
            return self._type
    
    def __getattr__(self, name):
        if self.user_parameter:
            return self.user_parameter.__getattribute__(name)
    
    def __setattr__(self, name, value):
        if not name in self.__dict__ and 'user_parameter' in self.__dict__ and self.__dict__['user_parameter']:
            return self.__dict__['user_parameter'].__setattr__(name, value)
        else:
            self.__dict__[name] = value
