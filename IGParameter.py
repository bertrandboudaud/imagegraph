from PIL import Image
import copy

class IGParameter:
    def __init__(self, type):
        self.id = ""
        self.type = type
        self.owner = None
        self.timestamp = 0
        self.is_ready = False
        self._value = {}
        self._backup_value = {}
    
    def set_ready(self, ready=True):
        self.is_ready = ready
        self.timestamp = self.timestamp + 1

    def set_value(self, other_parameter):
        self._value = copy.deepcopy(other_parameter._value)

    def backup_value(self):
        self._backup_value = copy.deepcopy(self._value)

    def restore_backup_value(self):
        self._value = copy.deepcopy(self._backup_value)

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
