from IGParameter import *
from IGNode import *
from PIL import ImageOps
from IGParameterImage import *

class IGGrayscale(IGNode):
    def __init__(self):
        super().__init__("Gray Scale")
        self.add_input_parameter("source image", IGParameterImage.IGParameterImage()) 
        self.add_output_parameter("grayscale image", IGParameterImage.IGParameterImage()) 

    def process(self):
        self.outputs["grayscale image"].image = ImageOps.grayscale(self.inputs["source image"].image).convert('RGBA')
        self.set_all_outputs_ready()
        
