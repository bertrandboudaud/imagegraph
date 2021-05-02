from IGParameter import *
from IGNode import *
from PIL import ImageOps
from IGParameterList import *
from IGParameterMutable import *

class IGForEach2(IGNode):
    def __init__(self):
        super().__init__("For Each Loop 2")
        self.add_input_parameter("List to iterate", IGParameterList.IGParameterList()) 
        self.add_output_parameter("Element of the list", IGParameterMutable.IGParameterMutable())
        self.input_to_output = {}
        self.input_to_result = {}
        self.reset()
    
    def reset(self):
        super().reset()
        self.index = 0

    def process(self):
        list_parameter = self.inputs["List to iterate"]
        if (self.index < len(list_parameter.list)):
            current_element = list_parameter.list[self.index]
            self.outputs["Element of the list"].set_value(current_element)
            self.outputs["Element of the list"].set_ready()
            for input_name in self.input_to_output: 
                self.input_to_output[input_name].set_value(self.inputs["input_name"])
                self.input_to_output[input_name].set_ready()
        else:
            for input_name in self.input_to_result:
                self.input_to_result[input_name].set_value(self.inputs["input_name"])
                self.input_to_result[input_name].set_ready()
        self.index = self.index + 1

    def is_scoped_node(self):
        return True

    def handle_dynamic_parameters(self):
        return True

    def add_dynamic_parameter(self):
        id = 1
        while True:
            param_name = "param" + str(id)
            if not param_name in self.inputs:
                break
            id = id +1
        self.add_input_parameter(param_name, IGParameterMutable.IGParameterMutable())
        self.add_output_parameter(param_name, IGParameterMutable.IGParameterMutable())
        result_name = "result" + str(id)
        self.add_output_parameter(result_name, IGParameterMutable.IGParameterMutable())
        self.input_to_output[param_name] = self.outputs[param_name]
        self.input_to_result[param_name] = self.outputs[result_name]

    def on_input_connected_to(self, input_parameter, output_parameter):
        name = input_parameter.id
        self.outputs[name].mute_to(output_parameter)
        name = "result"+name.split("param")[1]
        self.outputs[name].mute_to(output_parameter)
