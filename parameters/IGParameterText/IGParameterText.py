from IGParameter import *
from PIL import Image
import copy

class IGParameterText(IGParameter):
    def __init__(self):
        super().__init__("Text")
        self._value["text"] = ""
  
    @property
    def text(self):
        return self._value["text"]

    @text.setter
    def text(self, text):
        self._value["text"] = text

