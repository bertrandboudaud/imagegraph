import imgui # TODO remove this dependency
from PIL import Image

class IGParameter:
    def __init__(self, type):
        self.id = ""
        self.type = type
        self.owner = None
        self.timestamp = 0
        self.is_ready = False
        self._value = {}
    
    def set_ready(self, ready=True):
        self.is_ready = ready
        self.timestamp = self.timestamp + 1

    def set_value(self, other_parameter):
        self._value = other_parameter._value.copy()

class IGParameterImage(IGParameter):
    def __init__(self):
        super().__init__("Image")
        self._value["image"] = None
    
    @property
    def image(self):
        return self._value["image"]

    @image.setter
    def image(self, image):
        self._value["image"] = image

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
class IGParameterURL(IGParameter):
    def __init__(self):
        super().__init__("URL")
        self._value["url"] = "c:\\tmp\Capture.PNG"

    @property
    def url(self):
        return self._value["url"]

    @url.setter
    def url(self, url):
        self._value["url"] = list

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

    @x.setter
    def y(self, y):
        self._value["y"] = y

    def to_tuple(self):
        return (self._value["x"], self._value["y"])

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

