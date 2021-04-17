from IGParameter import *
from IGNode import *
from IGParameterImage import *
from IGParameterColor import *
from PIL import ImageOps

class IGColorize(IGNode):
    def __init__(self):
        super().__init__("Colorize Image")
        self.add_input_parameter("source image", IGParameterImage.IGParameterImage()) 
        self.add_input_parameter("black", IGParameterColor.IGParameterColor()) 
        self.add_input_parameter("white", IGParameterColor.IGParameterColor()) 
        self.add_output_parameter("colorized image", IGParameterImage.IGParameterImage()) 

    def process(self):
        black = self.inputs["black"].color256()
        white = self.inputs["white"].color256()
        image = self.inputs["source image"].image
        image = image.convert("L")
        # mid is also available
        self.outputs["colorized image"].image = ImageOps.colorize(image, black, white).convert("RGBA")
        self.set_all_outputs_ready()
        
