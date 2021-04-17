from IGParameter import *
from PIL import Image
import copy

class IGParameterRectangle(IGParameter):
    def __init__(self):
        super().__init__("Rectangle")
        self._value["left"] = 0
        self._value["top"] = 0
        self._value["right"] = 0
        self._value["bottom"] = 0

    @property
    def left(self):
        return self._value["left"]

    @left.setter
    def left(self, left):
        self._value["left"] = left
        
    @property
    def top(self):
        return self._value["top"]

    @top.setter
    def top(self, top):
        self._value["top"] = top
        
    @property
    def right(self):
        return self._value["right"]

    @right.setter
    def right(self, right):
        self._value["right"] = right
        
    @property
    def bottom(self):
        return self._value["bottom"]

    @bottom.setter
    def bottom(self, bottom):
        self._value["bottom"] = bottom
        
    def to_tuple(self):
        return (self._value["left"], self._value["top"], self._value["right"], self._value["bottom"])

