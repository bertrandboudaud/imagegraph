import imgui # TODO remove this dependency

class IGParameter:
    def __init__(self, id, type, output = True):
        self.id = id
        self.type = type
        self.output = output
    
class IGParameterImage
    def __init__(self, id, type):
        super().__init__(id, "Image")