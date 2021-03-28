from IGParameter import *
from IGNode import *
from PIL import ImageFilter
from PIL import ImageOps

class IGLoadImage(IGNode):
    def __init__(self):
        super().__init__("Load Image", imgui.Vec2(50,50))
        self.add_input_parameter("url", IGParameterURL()) 
        self.add_output_parameter("loaded image", IGParameterImage()) 
    
    def process(self):
        url = self.inputs["url"].url
        self.outputs["loaded image"].image = Image.open(url).transpose( Image.FLIP_TOP_BOTTOM );

