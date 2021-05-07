import os
import sys
from os.path import dirname
from IGScriptNode import *
class IGLibrary:
    def __init__(self):
        self.nodes = []
        self.native_nodes = {}
        self.script_nodes = {}
        self.parameters = {}
        # native nodes
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
            self.native_nodes[node_instance.name] = node_module
            self.nodes.append(node_instance.name)
        # scripts nodes
        script_dirs = ["c:\\tmp\\lib"]
        for script_dir in script_dirs:
            for file in os.listdir(script_dir):
                if file.endswith(".json"):
                    # todo check content
                    node_name = os.path.splitext(file)[0]
                    self.script_nodes[node_name] = os.path.join(script_dir, file)
                    self.nodes.append(node_name)
   
    def create_node(self, node_name):
        if node_name in self.script_nodes:
            return IGScriptNode(node_name, self.script_nodes[node_name], self)
        else:
            return self.native_nodes[node_name].get()

    def create_parameter(self, parameter_name):
        return self.parameters[parameter_name].get()
