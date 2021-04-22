from PIL import Image
import copy

class IGParameter:
    def __init__(self, type):
        self.id = ""
        self._type = type
        self.owner = None
        self.timestamp = 0
        self.is_ready = False
        self._value = {}
        self._backup_value = {}
    
    def set_ready(self, ready=True):
        self.is_ready = ready
        self.timestamp = self.timestamp + 1

    def set_value(self, other_parameter):
        self._value = copy.deepcopy(other_parameter.get_value())

    def backup_value(self):
        self._backup_value = copy.deepcopy(self.get_value())

    def restore_backup_value(self):
        self._value = copy.deepcopy(self.get_value())

    def get_value(self):
        return self._value

    def to_json(self):
        json = {}
        json["id"]=self.id
        json["type"]=self.type
        json["value"] = self._backup_value
        return json

    def from_json(self, json):
        self.id = json["id"]
        self.type = json["type"]
        self._value = json["value"].copy()
        self._backup_value = json["value"].copy()
        return json

    # override to handle connection to another parameter
    def on_connected_to(self, other_parameter):
        pass

    @property
    def type(self):
        return self._type

    def __copy__(self):
        cpy = object.__new__(type(self))
        cpy.id = self.id
        cpy._type = self._type
        cpy.owner = None
        cpy.timestamp = self.timestamp
        cpy.is_ready = self.is_ready
        cpy._value = self._value.copy()
        cpy._backup_value = self._backup_value.copy()
        return cpy
