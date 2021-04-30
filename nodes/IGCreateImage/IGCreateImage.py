from IGParameter import *
from IGNode import *
from PIL import Image
from IGParameterInteger import *
from IGParameterImage import *
from IGParameterColor import *

class IGCreateImage(IGNode):
    def __init__(self):
        super().__init__("Create Image")
        self.add_input_parameter("width", IGParameterInteger.IGParameterInteger())
        self.add_input_parameter("height", IGParameterInteger.IGParameterInteger())
        self.add_input_parameter("background color", IGParameterColor.IGParameterColor()) 
        self.add_output_parameter("created image", IGParameterImage.IGParameterImage()) 
    
    def process(self):
        width = self.inputs["width"].value
        height = self.inputs["height"].value
        color = self.inputs["background color"].color256_tuple()
        self.outputs["created image"].image = Image.new('RGBA', (width, height), color = color)
        self.set_all_outputs_ready()

