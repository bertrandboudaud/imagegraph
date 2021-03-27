import imgui # TODO remove this dependency
from IGParameter import *
class NodeLink:
    def __init__(self, output_parameter, input_parameter):
        self.input_parameter = input_parameter
        self.output_parameter = output_parameter

class IGNode:
    def __init__(self, id, name, pos):
        self.id = id
        self.name = name
        self.pos = pos
        self.size = imgui.Vec2(0,0)
        self.inputs = []
        self.outputs = []

    def get_intput_slot_pos(self, parameter):
        slot_no = 0
        for input_parameter in self.inputs: # replace with map and name of the parameter
            if input_parameter == parameter:
                break
            slot_no = slot_no + 1 
        return imgui.Vec2(self.pos.x, self.pos.y + self.size.y*((slot_no+1) / (len(self.inputs)+1) ))

    def get_output_slot_pos(self, parameter):
        slot_no = 0
        for output_parameter in self.outputs: # replace with map and name of the parameter
            if output_parameter == parameter:
                break
            slot_no = slot_no + 1 
        return imgui.Vec2(self.pos.x + self.size.x, self.pos.y + self.size.y*((slot_no+1) / (len(self.outputs)+1) ))

class IGCreateImage(IGNode):
    def __init__(self, id):
        super().__init__(id, "Create Image", imgui.Vec2(50,50))
        self.created_image = IGParameterImage("created image", self) 
        self.outputs.append(self.created_image)
    
    def process(self):
        mode = 'RGBA'
        size = (128, 128)
        color = (73, 109, 137)
        self.created_image.image = Image.new(mode, size, color)

class IGFilterImage(IGNode):
    def __init__(self, id):
        super().__init__(id, "Filter Image", imgui.Vec2(200,100))
        self.inputs.append(IGParameterImage("source image", self))

    def process(self):
        print("IGFilterImage process")
