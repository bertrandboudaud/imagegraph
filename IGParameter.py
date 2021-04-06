import imgui # TODO remove this dependency
from PIL import Image

# TODO: 'value' should be used for the generic value, to avoid the set_value method
class IGParameter:
    def __init__(self, type):
        self.id = ""
        self.type = type
        self.owner = None
        self.timestamp = 0
        self.is_ready = False
    
    def set_ready(self, ready=True):
        self.is_ready = ready
        self.timestamp = self.timestamp + 1
    
class IGParameterImage(IGParameter):
    def __init__(self):
        super().__init__("Image")
        self.image = None
    
    def set_value(self, other_parameter):
        self.image = other_parameter.image
class IGParameterRectangle(IGParameter):
    def __init__(self):
        super().__init__("Rectangle")
        self.top = 0
        self.left = 0
        self.right = 0
        self.bottom = 0

    def set_value(self, other_parameter):
        self.top = other_parameter.top
        self.left = other_parameter.left
        self.right = other_parameter.right
        self.bottom = other_parameter.bottom

    def to_tuple(self):
        return (self.left, self.top, self.right, self.bottom)

class IGParameterColor(IGParameter):
    def __init__(self):
        super().__init__("Color")
        self.r = 1.0
        self.g = 1.0
        self.b = 1.0
        self.a = 1.0

    def color256(self):
        return [self.r*255 , self.g*255, self.b*255, self.a*255]

    def set_value(self, other_parameter):
        self.r = other_parameter.r
        self.g = other_parameter.g
        self.b = other_parameter.b
        self.a = other_parameter.a
class IGParameterURL(IGParameter):
    def __init__(self):
        super().__init__("URL")
        self.url = "c:\\tmp\Capture.PNG"

    def set_value(self, other_parameter):
        self.url = other_parameter.url
class IGParameterInteger(IGParameter):
    def __init__(self):
        super().__init__("Integer")
        self.value = 0
    
    def set_value(self, other_parameter):
        self.value = other_parameter.value
class IGParameterList(IGParameter):
    def __init__(self):
        super().__init__("List")
        self.list = []
    
    def set_value(self, other_parameter):
        self.list = other_parameter.list
