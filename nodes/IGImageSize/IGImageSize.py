from IGParameter import *
from IGNode import *
from PIL import ImageOps
from IGParameterImage import *
from IGParameterCoords import *
from IGParameterColor import *
from IGParameterInteger import *

class IGImageSize(IGNode):
    def __init__(self):
        super().__init__("Image Size")
        self.add_input_parameter("image", IGParameterImage.IGParameterImage())
        self.add_output_parameter("size", IGParameterCoords.IGParameterCoords()) 

    def process(self):
        source = self.inputs["image"].image
        coord_x, coord_y = source.size
        self.outputs["size"].x = coord_x
        self.outputs["size"].y = coord_y
        self.set_all_outputs_ready()
