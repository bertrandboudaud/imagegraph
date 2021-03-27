import imgui # TODO remove this dependency
from PIL import Image

class IGParameter:
    def __init__(self, type):
        self.id = ""
        self.type = type
        self.owner = None
    
class IGParameterImage(IGParameter):
    def __init__(self):
        super().__init__("Image")
        self.image = None