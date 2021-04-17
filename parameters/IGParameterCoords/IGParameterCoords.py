from IGParameter import *
from PIL import Image
import copy


class IGParameterCoords(IGParameter):
    def __init__(self):
        super().__init__("Coordinates")
        self._value["x"] = 0
        self._value["y"] = 0

    @property
    def x(self):
        return self._value["x"]

    @x.setter
    def x(self, x):
        self._value["x"] = x

    @property
    def y(self):
        return self._value["y"]

    @y.setter
    def y(self, y):
        self._value["y"] = y

    def to_tuple(self):
        return (self._value["x"], self._value["y"])

