import imgui # TODO remove this dependency
from PIL import Image

class IGParameter:
    def __init__(self, id, type, output = True):
        self.id = id
        self.type = type
        self.output = output
    
class IGParameterImage(IGParameter):
    def __init__(self, id):
        super().__init__(id, "Image")
        mode = 'RGB'
        size = (128, 128)
        color = (73, 109, 137)
        self.image = Image.new(mode, size, color)