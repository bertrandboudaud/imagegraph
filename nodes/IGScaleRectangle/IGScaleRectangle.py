from IGParameter import *
from IGNode import *
from PIL import ImageOps
from IGParameterRectangle import *
from IGParameterCoords import *
from IGParameterInteger import *

class IGScaleRectangle(IGNode):
    def __init__(self):
        super().__init__("Scale Rectangle")
        self.add_input_parameter("rectangle", IGParameterRectangle.IGParameterRectangle())
        self.add_input_parameter("scale", IGParameterInteger.IGParameterInteger())
        self.add_input_parameter("pivot point", IGParameterCoords.IGParameterCoords()) 
        self.add_output_parameter("scaled rectangle", IGParameterRectangle.IGParameterRectangle())
        # default pivot point is middle
        self.inputs["pivot point"].x = 0.5
        self.inputs["pivot point"].y = 0.5
        self.inputs["scale"].value = 1.0

    def process(self):
        left = self.inputs["rectangle"].left
        top = self.inputs["rectangle"].top
        right = self.inputs["rectangle"].right
        bottom = self.inputs["rectangle"].bottom
        pivot_coord_x = self.inputs["pivot point"].x
        pivot_coord_y = self.inputs["pivot point"].y
        scale = self.inputs["scale"].value
        width = (right-left)*scale
        height = (bottom-top)*scale
        # to do use pivot point
        self.outputs["scaled rectangle"].left = left
        self.outputs["scaled rectangle"].top = top
        self.outputs["scaled rectangle"].right = left + width
        self.outputs["scaled rectangle"].bottom = top + height
        self.set_all_outputs_ready()
