from IGParameter import *
from IGNode import *
from PIL import ImageOps

class IGFlip(IGNode):
    def __init__(self):
        super().__init__("Flip image")
        self.add_input_parameter("source image", IGParameterImage()) 
        self.add_output_parameter("flipped image", IGParameterImage()) 

    def process(self):
        self.outputs["flipped image"].image = ImageOps.flip(self.inputs["source image"].image)
        self.set_all_outputs_ready()
        
