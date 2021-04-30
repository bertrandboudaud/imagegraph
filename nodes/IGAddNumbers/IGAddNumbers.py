from IGParameter import *
from IGNode import *
from PIL import ImageOps
from IGParameterRectangle import *
from IGParameterCoords import *
from IGParameterInteger import *

class IGAddNumbers(IGNode):
    def __init__(self):
        super().__init__("Add Numbers")
        self.add_input_parameter("a", IGParameterInteger.IGParameterInteger())
        self.add_input_parameter("b", IGParameterInteger.IGParameterInteger())
        self.add_output_parameter("addition result", IGParameterInteger.IGParameterInteger())

    def process(self):
        a = self.inputs["a"].value
        b = self.inputs["b"].value
        self.outputs["addition result"].value = a+b
        self.set_all_outputs_ready()
