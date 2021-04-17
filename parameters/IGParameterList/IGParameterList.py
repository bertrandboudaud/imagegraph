from IGParameter import *
from PIL import Image
import copy

class IGParameterList(IGParameter):
    def __init__(self):
        super().__init__("List")
        self._value["list"] = []
    
    @property
    def list(self):
        return self._value["list"]

    @list.setter
    def list(self, list):
        self._value["list"] = list

