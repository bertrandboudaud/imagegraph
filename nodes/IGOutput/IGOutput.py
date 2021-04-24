from IGParameter import *
from IGNode import *
from PIL import ImageFilter
from PIL import ImageOps
from IGParameterText import *
from IGParameterMutable import *

class IGOutput(IGNode):
    def __init__(self):
        super().__init__("Output")
        self.add_input_parameter("parameter name", IGParameterText.IGParameterText())
        self.add_output_parameter("output", IGParameterMutable.IGParameterMutable()) 
        self.add_input_parameter("output", IGParameterMutable.IGParameterMutable()) 
    
    def process(self):
        self.outputs["output"].set_value(self.inputs["output"])
        self.set_all_outputs_ready()
    
    # TODO add parameter input !!
    def on_input_connected_to(self, other_parameter):
        self.outputs["output"].mute_to(other_parameter)
        if self.inputs["parameter name"].text == "":
            self.inputs["parameter name"].text = other_parameter.id
        

