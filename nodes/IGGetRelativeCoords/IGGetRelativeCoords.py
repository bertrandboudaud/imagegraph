from IGParameter import *
from IGNode import *
from PIL import ImageOps

class IGGetRelativeCoords(IGNode):
    def __init__(self):
        super().__init__("Relative Coords")
        self.add_input_parameter("rectangle", IGParameterRectangle())
        self.add_input_parameter("relative coords", IGParameterCoords()) 
        self.add_output_parameter("coords", IGParameterCoords())
        # default is middle
        self.inputs["relative coords"].x = 0.5
        self.inputs["relative coords"].y = 0.5

    def process(self):
        left = self.inputs["rectangle"].left
        top = self.inputs["rectangle"].top
        right = self.inputs["rectangle"].right
        bottom = self.inputs["rectangle"].bottom
        relative_coord_x = self.inputs["relative coords"].x
        relative_coord_y = self.inputs["relative coords"].y
        self.outputs["coords"].x = ((right-left)*relative_coord_x) + left
        self.outputs["coords"].y = ((bottom-top)*relative_coord_y) + top
        self.set_all_outputs_ready()
