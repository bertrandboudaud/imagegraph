from IGParameter import *
from IGNode import *
from PIL import ImageOps
from IGParameterImage import *
from IGParameterCoords import *
from IGParameterColor import *
from IGParameterInteger import *

class IGHighMap(IGNode):
    def __init__(self):
        super().__init__("High Map")
        self.add_input_parameter("image", IGParameterImage.IGParameterImage())
        self.add_input_parameter("coords", IGParameterCoords.IGParameterCoords()) 
        self.add_output_parameter("high", IGParameterInteger.IGParameterInteger()) 

    def process(self):
        source = self.inputs["image"].image
        coord_x = int(self.inputs["coords"].x)
        coord_y = int(self.inputs["coords"].y)
        r, g, b, a = source.getpixel((coord_x, coord_y))
        r = r/256.0
        g = g/256.0
        b = b/256.0
        a = a/256.0
        self.outputs["high"].value = r
        self.set_all_outputs_ready()
