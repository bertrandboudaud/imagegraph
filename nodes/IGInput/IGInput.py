from IGParameter import *
from IGNode import *
from PIL import ImageFilter
from PIL import ImageOps
from IGParameterText import *
from IGParameterMutable import *

class IGInput(IGNode):
    def __init__(self):
        super().__init__("Input")
        self.add_input_parameter("parameter name", IGParameterText.IGParameterText())
        self.add_output_parameter("input", IGParameterMutable.IGParameterMutable()) 
        self.add_input_parameter("default value", IGParameterMutable.IGParameterMutable()) 
    
    def process(self):
        self.outputs["input"].set_value(self.inputs["default value"])
        self.set_all_outputs_ready()
    
    def on_output_connected_to(self, other_parameter):
        self.inputs["default value"].mute_to(other_parameter)
        if self.inputs["parameter name"].text == "":
            self.inputs["parameter name"].text = other_parameter.id
        

