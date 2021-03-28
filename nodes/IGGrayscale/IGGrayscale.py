from IGParameter import *
from IGNode import *
from PIL import ImageOps

class IGGrayscale(IGNode):
    def __init__(self):
        super().__init__("Gray Scale", imgui.Vec2(200,100))
        self.add_input_parameter("source image", IGParameterImage()) 
        self.add_output_parameter("grayscale image", IGParameterImage()) 

    def process(self):
        self.outputs["grayscale image"].image = ImageOps.grayscale(self.inputs["source image"].image).convert('RGBA')
        
