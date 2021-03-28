from IGParameter import *
from IGNode import *
from PIL import ImageOps

class IGMirror(IGNode):
    def __init__(self):
        super().__init__("Miror image", imgui.Vec2(200,100))
        self.add_input_parameter("source image", IGParameterImage()) 
        self.add_output_parameter("mirrored image", IGParameterImage()) 

    def process(self):
        self.outputs["mirrored image"].image = ImageOps.flip(self.inputs["source image"].image)
        
