import os
import sys
from os.path import dirname
class IGLibrary:
    def __init__(self):
        self.nodes = {}
        self.parameters = {}
        sys.path.append(dirname(__file__) + "/parameters")
        parameter_names = os.listdir('./parameters')
        for parameter_name in parameter_names:
            parameter_module = __import__(parameter_name)
            parameter_instance = parameter_module.get()
            self.parameters[parameter_instance.type] = parameter_module
        sys.path.append(dirname(__file__) + "/nodes")
        node_names = os.listdir('./nodes')
        for node_name in node_names:
            node_module = __import__(node_name)
            node_instance = node_module.get()
            self.nodes[node_instance.name] = node_module
   
    def create_node(self, node_name):
        return self.nodes[node_name].get()

    def create_parameter(self, parameter_name):
        return self.parameters[parameter_name].get()
