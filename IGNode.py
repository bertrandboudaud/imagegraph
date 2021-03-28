import imgui # TODO remove this dependency
from IGParameter import *
from PIL import ImageFilter
from PIL import ImageOps

class NodeLink:
    def __init__(self, output_parameter, input_parameter):
        self.input_parameter = input_parameter
        self.output_parameter = output_parameter

class IGNode:
    def __init__(self, name, pos):
        self.id = None
        self.name = name
        self.pos = pos
        self.size = imgui.Vec2(0,0)
        self.inputs = {}
        self.outputs = {}
    
    def set_id(self, id):
        self.id = None
    
    def get_intput_slot_pos(self, parameter):
        slot_no = 0
        for input_parameter in self.inputs: # replace with map and name of the parameter
            if input_parameter == parameter.id:
                break
            slot_no = slot_no + 1 
        return imgui.Vec2(self.pos.x, self.pos.y + self.size.y*((slot_no+1) / (len(self.inputs)+1) ))

    def get_output_slot_pos(self, parameter):
        slot_no = 0
        for output_parameter in self.outputs: # replace with map and name of the parameter
            if output_parameter == parameter.id:
                break
            slot_no = slot_no + 1 
        return imgui.Vec2(self.pos.x + self.size.x, self.pos.y + self.size.y*((slot_no+1) / (len(self.outputs)+1) ))

    def add_input_parameter(self, id, parameter):
        parameter.id = id
        parameter.owner = self
        self.inputs[id] = parameter

    def add_output_parameter(self, id, parameter):
        parameter.id = id
        parameter.owner = self
        self.outputs[id] = parameter

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
