from IGParameter import *
from PIL import Image
import copy

class IGParameterInteger(IGParameter):
    def __init__(self):
        super().__init__("Integer")
        self._value["value"] = 0

    @property
    def value(self):
        return self._value["value"]

    @value.setter
    def value(self, value):
        self._value["value"] = value

