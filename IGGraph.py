import imgui # TODO remove this dependency
from IGLibrary import *

class IGGraph:
    def __init__(self):
        self.nodes = []
        self.links = []
        self.run_nodes = []
        self.error_nodes = {}
        self.id_generator = 1
        self.node_library = IGLibrary()
        self.timestamp = 1
    
    def find_input_parameter_links(self, input_parameter):
        # find output parameters linked to this input parameter
        found_parameter = []
        for link in self.links:
            if input_parameter == link.input_parameter:
                found_parameter.append(link.output_parameter)
        return found_parameter

    def find_nodes_to_run(self):
        found_nodes = []
        for node in self.nodes:
            linked_outputs = [] # outputs linked to all inputs of the node
            for parameter_name in node.inputs:
                parameter = node.inputs[parameter_name]
                linked_outputs = linked_outputs + self.find_input_parameter_links(parameter)
            add_node = not node in self.run_nodes
            for output in linked_outputs:
                if not output.owner in self.run_nodes:
                    add_node = False
                    break
            if add_node:
               found_nodes.append(node) 
        return found_nodes
    
    def set_inputs(self, node):
        for parameter_name in node.inputs:
            parameter = node.inputs[parameter_name]
            linked_outputs = self.find_input_parameter_links(parameter)
            for output in linked_outputs:
                parameter.image = output.image ## todo other types of parameters

    def run(self):
        self.run_nodes = []
        self.error_nodes = {}
        while True:
            if not self.run_one_step():
                break
        
    def run_one_step(self):
        node_to_run = self.find_nodes_to_run()
        if len(node_to_run) == 0:
            return False
        for node in node_to_run:
            self.set_inputs(node)
            try:
                node.process()
            except Exception as e:
                self.error_nodes[node] = str(e)
            self.run_nodes.append(node)
            self.update_timestamps(node)
        return True

    def is_run(self, node):
        return node in self.run_nodes

    def is_error(self, node):
        return node in self.error_nodes
    
    def create_node(self, node_name, pos = imgui.Vec2(0,0)):
        new_node = self.node_library.create_node(node_name)
        new_node.id = self.id_generator
        new_node.pos = pos
        self.id_generator = self.id_generator +1
        self.nodes.append(new_node)
        return new_node

    def update_timestamps(self, node):
        for parameter_name in node.inputs:
            parameter = node.inputs[parameter_name]
            parameter.timestamp = self.timestamp
        for parameter_name in node.outputs:
            parameter = node.outputs[parameter_name]
            parameter.timestamp = self.timestamp
        self.timestamp = self.timestamp + 1