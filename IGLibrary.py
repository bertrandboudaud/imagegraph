import os
import sys
from os.path import dirname
class IGLibrary:
    def __init__(self):
        self.nodes = {}
        sys.path.append(dirname(__file__) + "/nodes")
        node_names = os.listdir('./nodes')
        for node_name in node_names:
            node_module = __import__(node_name)
            node_instance = node_module.get()
            self.nodes[node_instance.name] = node_module
   
    def create_node(self, node_name):
        return self.nodes[node_name].get()

