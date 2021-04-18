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
        self.input_value = None
    
    def process(self):
        self.outputs["input"].value = self.input_value
        self.set_all_outputs_ready()
    
    def connect_to(self, other_parameter):
        print("connect to other parameter TODO")

