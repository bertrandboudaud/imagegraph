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
        self.image = None