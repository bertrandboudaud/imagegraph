import imgui # TODO remove this dependency
from PIL import Image

class IGParameter:
    def __init__(self, type):
        self.id = ""
        self.type = type
        self.owner = None
        self.timestamp = 0
    
class IGParameterImage(IGParameter):
    def __init__(self):
        super().__init__("Image")
        self.image = None
class IGParameterRectangle(IGParameter):
    def __init__(self):
        super().__init__("Rectangle")
        self.top = 10
        self.left = 10
        self.right = 100
        self.bottom = 100

class IGParameterColor(IGParameter):
    def __init__(self):
        super().__init__("Color")
        self.r = 1.0
        self.g = 1.0
        self.b = 1.0
        self.a = 1.0

    def color256(self):
        return [self.r*255 , self.g*255, self.b*255, self.a*255]
class IGParameterURL(IGParameter):
    def __init__(self):
        super().__init__("URL")
        self.url = "c:\\tmp\Capture.PNG"
