import imgui # TODO remove this dependency
from PIL import Image

class IGParameter:
    def __init__(self, id, type, owner, output = True):
        self.id = id
        self.type = type
        self.output = output
        self.owner = owner
    
class IGParameterImage(IGParameter):
    def __init__(self, id, owner):
        super().__init__(id, "Image", owner)
        mode = 'RGB'
        size = (128, 128)
        color = (73, 109, 137)
        self.image = Image.new(mode, size, color)