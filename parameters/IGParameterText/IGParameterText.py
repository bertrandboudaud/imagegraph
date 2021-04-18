from IGParameter import *
from PIL import Image
import copy

class IGParameterText(IGParameter):
    def __init__(self):
        super().__init__("Text")
        self._value["text"] = 0

    @property
    def value(self):
        return self._value["text"]

    @value.setter
    def value(self, value):
        self._value["text"] = value

