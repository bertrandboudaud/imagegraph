import imgui # TODO remove this dependency
from IGParameter import *
from PIL import ImageFilter
from PIL import ImageOps

class NodeLink:
    def __init__(self, output_parameter, input_parameter):
        self.input_parameter = input_parameter
        self.output_parameter = output_parameter

    def to_json(self):
        json = {}
        json_parameter = {}
        json_parameter["node_id"] = self.input_parameter.owner.id
        json_parameter["parameter_id"] = self.input_parameter.id
        json["input_parameter"] = json_parameter
        json_parameter = {}
        json_parameter["node_id"] = self.output_parameter.owner.id
        json_parameter["parameter_id"] = self.output_parameter.id
        json["output_parameter"] = json_parameter
        return json

class IGNode:
    def __init__(self, name, pos = imgui.Vec2(0,0)):
        self.id = None
        self.name = name
        self.pos = pos
        self.size = imgui.Vec2(0,0)
        self.inputs = {}
        self.outputs = {}

    def to_json(self):
        json = {}
        json["name"] = self.name
        inputs = {}
        for input_name in self.inputs:
            inputs[input_name] = self.inputs[input_name].to_json()
        json["inputs"] = inputs
        outputs = {}
        for output_name in self.outputs:
            outputs[output_name] = self.outputs[output_name].to_json()
        json["outputs"] = outputs
        pos = {}
        pos["x"] = self.pos.x
        pos["y"] = self.pos.x
        json["pos"] = pos
        size = {}
        size["x"] = self.size.x
        size["y"] = self.size.x
        json["size"] = size
        json["id"] = self.id
        return json

    def set_all_outputs_ready(self):
        for output_parameter_name in self.outputs:
            self.outputs[output_parameter_name].set_ready()
    
    def set_id(self, id):
        self.id = None
    
    def get_intput_slot_pos(self, parameter):
        slot_no = 0
        for input_parameter in self.inputs:
            if input_parameter == parameter.id:
                break
            slot_no = slot_no + 1 
        return imgui.Vec2(self.pos.x, self.pos.y + self.size.y*((slot_no+1) / (len(self.inputs)+1) ))

    def get_output_slot_pos(self, parameter):
        slot_no = 0
        for output_parameter in self.outputs:
            if output_parameter == parameter.id:
                break
            slot_no = slot_no + 1 
        return imgui.Vec2(self.pos.x + self.size.x, self.pos.y + self.size.y*((slot_no+1) / (len(self.outputs)+1) ))

    def add_input_parameter(self, id, parameter):
        parameter.id = id
        parameter.owner = self
        self.inputs[id] = parameter
        self.preapre_to_process()

    def add_output_parameter(self, id, parameter):
        parameter.id = id
        parameter.owner = self
        self.outputs[id] = parameter
        self.preapre_to_process()

    def preapre_to_process(self):
        # save default values
        for input_parameter_name in self.inputs:
            parameter = self.inputs[input_parameter_name]
            parameter.backup_value()
        for output_parameter_name in self.outputs:
            parameter = self.outputs[output_parameter_name]
            parameter.backup_value()

    def reset(self):
        for input_parameter_name in self.inputs:
            parameter = self.inputs[input_parameter_name]
            parameter.restore_backup_value()
            parameter.is_ready = False
        for output_parameter_name in self.outputs:
            parameter = self.outputs[output_parameter_name]
            parameter.restore_backup_value()
            parameter.is_ready = False

class IGCreateImage(IGNode):
    def __init__(self, id):
        super().__init__(id, "Create Image")
        self.created_image = IGParameterImage("created image", self) 
        self.outputs.append(self.created_image)
    
    def process(self):
        mode = 'RGBA'
        size = (128, 128)
        color = (73, 109, 137)
        self.created_image.image = Image.new(mode, size, color)
