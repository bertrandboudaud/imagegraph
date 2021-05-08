from IGParameter import *
from PIL import Image
import copy

class IGParameterMutable(IGParameter):
    def __init__(self):
        super().__init__("Generic Output")
        self.user_parameter = None
        # used to be applied once the parameter is muted
        # loading phase
        self.user_parameter_json = None

    def on_connected_to(self, other_parameter):
        if self.user_parameter == None:
            self.mute_to(other_parameter)

    # TODO: disconnection
    # - unmute
    # - remove user_parameter_json

    def mute_to(self, other_parameter):
        if ("user_parameter" in other_parameter.__dict__):
            self.user_parameter = copy.copy(other_parameter.user_parameter)
        else:
            self.user_parameter = copy.copy(other_parameter)
        if self.user_parameter_json:
            self.__dict__['user_parameter'] = self.__dict__['user_parameter'].from_json(self.__dict__['user_parameter_json'])
        else:
            if ("user_parameter" in other_parameter.__dict__):
                self.set_value(other_parameter.user_parameter)
            else:
                self.set_value(other_parameter)

    def get_value(self):
        if self.user_parameter:
            return self.user_parameter.get_value()
        else:
            return None

    def set_value(self, other_parameter):
        if (self.user_parameter):
            self.user_parameter.set_value(other_parameter)

    def backup_value(self):
        if (self.user_parameter):
            self.user_parameter.backup_value()

    def restore_backup_value(self):
        if (self.user_parameter):
            self.user_parameter.restore_backup_value()

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

    def to_json(self):
        json = {}
        json["id"] = self.__dict__['id']
        json["type"] = self.__dict__['_type']
        json["user_parameter"] = self.__dict__['user_parameter'].to_json()
        return json

    def from_json(self, json):
        self.__dict__['id'] = json["id"]
        self.__dict__['type'] = json["type"]
        # will be applied later on the connection
        self.__dict__['user_parameter_json'] = json["user_parameter"]
        return json