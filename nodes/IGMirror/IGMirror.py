from IGParameter import *
from IGNode import *
from PIL import ImageOps

class IGMirror(IGNode):
    def __init__(self):
        super().__init__("Miror image")
        self.add_input_parameter("source image", IGParameterImage()) 
        self.add_output_parameter("mirrored image", IGParameterImage()) 

    def process(self):
        self.outputs["mirrored image"].image = ImageOps.flip(self.inputs["source image"].image)
        self.set_all_outputs_ready()
        
