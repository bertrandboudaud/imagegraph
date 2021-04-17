from IGParameter import *
from PIL import Image
import copy

class IGParameterColor(IGParameter):
    def __init__(self):
        super().__init__("Color")
        self._value["r"] = 1.0
        self._value["g"] = 1.0
        self._value["b"] = 1.0
        self._value["a"] = 1.0

    def color256(self):
        return [self.r*255 , self.g*255, self.b*255, self.a*255]

    @property
    def r(self):
        return self._value["r"]

    @r.setter
    def r(self, r):
        self._value["r"] = r

    @property
    def g(self):
        return self._value["g"]
    
    @g.setter
    def g(self, g):
        self._value["g"] = g

    @property
    def b(self):
        return self._value["b"]

    @b.setter
    def b(self, b):
        self._value["b"] = b
        
    @property
    def a(self):
        return self._value["a"]

    @a.setter
    def a(self, a):
        self._value["a"] = a
