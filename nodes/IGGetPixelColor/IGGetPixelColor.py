from IGParameter import *
from IGNode import *
from PIL import ImageOps
from IGParameterImage import *
from IGParameterCoords import *
from IGParameterColor import *

class IGGetPixelColor(IGNode):
    def __init__(self):
        super().__init__("Pixel Color")
        self.add_input_parameter("image", IGParameterImage.IGParameterImage())
        self.add_input_parameter("coords", IGParameterCoords.IGParameterCoords()) 
        self.add_output_parameter("pixel color", IGParameterColor.IGParameterColor()) 

    def process(self):
        source = self.inputs["image"].image
        coord_x = int(self.inputs["coords"].x)
        coord_y = int(self.inputs["coords"].y)
        r, g, b, a = source.getpixel((coord_x, coord_y))
        r = r/256.0
        g = g/256.0
        b = b/256.0
        a = a/256.0
        self.outputs["pixel color"].r = r
        self.outputs["pixel color"].g = g
        self.outputs["pixel color"].b = b
        self.outputs["pixel color"].a = a
        self.set_all_outputs_ready()
