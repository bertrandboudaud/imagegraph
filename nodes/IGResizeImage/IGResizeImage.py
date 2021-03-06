from IGParameter import *
from IGNode import *
from PIL import ImageOps
from IGParameterImage import *
from IGParameterCoords import *

class IGResizeImage(IGNode):
    def __init__(self):
        super().__init__("Resize Image")
        self.add_input_parameter("source image", IGParameterImage.IGParameterImage()) 
        self.add_input_parameter("size", IGParameterCoords.IGParameterCoords()) 
        self.add_output_parameter("resized image", IGParameterImage.IGParameterImage()) 

    def process(self):
        source = self.inputs["source image"].image
        coords = self.inputs["size"].to_tuple()
        self.outputs["resized image"].image = source.resize((int(coords[0]), int(coords[1])))
        self.set_all_outputs_ready()
