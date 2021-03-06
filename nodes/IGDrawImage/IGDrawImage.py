from IGParameter import *
from IGParameterImage import *
from IGParameterRectangle import *
from IGNode import *
from PIL import ImageOps

class IGDrawImage(IGNode):
    def __init__(self):
        super().__init__("Draw Image")
        self.add_input_parameter("source image", IGParameterImage.IGParameterImage()) 
        self.add_input_parameter("image to past", IGParameterImage.IGParameterImage())
        self.add_input_parameter("coordinates", IGParameterRectangle.IGParameterRectangle()) 
        self.add_output_parameter("composed image", IGParameterImage.IGParameterImage()) 

    def process(self):
        source = self.inputs["source image"].image.copy()
        to_past = self.inputs["image to past"].image
        coords = self.inputs["coordinates"].to_tuple()
        width = coords[2] - coords[0]
        height = coords[3] - coords[1]
        to_past = to_past.resize((int(width), int(height)))
        source.paste(to_past, (int(coords[0]), int(coords[1])))
        self.outputs["composed image"].image = source
        self.set_all_outputs_ready()
