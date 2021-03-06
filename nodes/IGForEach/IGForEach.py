from IGParameter import *
from IGNode import *
from PIL import ImageOps
from IGParameterImage import *
from IGParameterRectangle import *
from IGParameterList import *

class IGForEach(IGNode):
    def __init__(self):
        super().__init__("For Each Loop")
        self.add_input_parameter("List to iterate", IGParameterList.IGParameterList()) 
        self.add_input_parameter("Input1", IGParameterImage.IGParameterImage())
        self.add_output_parameter("Element", IGParameterRectangle.IGParameterRectangle()) 
        self.add_output_parameter("Output1", IGParameterImage.IGParameterImage())
        self.add_output_parameter("Result1", IGParameterImage.IGParameterImage())
        self.reset()
    
    def reset(self):
        super().reset()
        self.index = 0

    def process(self):
        list_parameter = self.inputs["List to iterate"]
        if (self.index < len(list_parameter.list)):
            current_element = list_parameter.list[self.index]
            self.outputs["Element"].set_value(current_element)
            self.outputs["Element"].set_ready()
            self.outputs["Output1"].set_value(self.inputs["Input1"])
            self.outputs["Output1"].set_ready()
        else:
            self.outputs["Result1"].set_value(self.inputs["Input1"])
            self.outputs["Result1"].set_ready()
        self.index = self.index + 1

    def is_scoped_node(self):
        return True
