from IGParameter import *
from IGNode import *
from PIL import ImageFilter
from PIL import ImageOps
from IGParameterImage import *
from IGParameterURL import *

class IGLoadImage(IGNode):
    def __init__(self):
        super().__init__("Load Image")
        self.add_input_parameter("url", IGParameterURL.IGParameterURL()) 
        self.add_output_parameter("loaded image", IGParameterImage.IGParameterImage()) 
    
    def process(self):
        url = self.inputs["url"].url
        self.outputs["loaded image"].image = Image.open(url).convert("RGBA")
        self.set_all_outputs_ready()

