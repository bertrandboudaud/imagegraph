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
        self.parameter_run_timestamp = {}
    
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
            all_inputs_are_ready = True
            one_input_has_changed = False
            node_linked_outputs = []
            for parameter_name in node.inputs:
                parameter = node.inputs[parameter_name]
                parameter_linked_outputs = self.find_input_parameter_links(parameter)
                node_linked_outputs = node_linked_outputs + parameter_linked_outputs
                input_is_ready = (len(parameter_linked_outputs) == 0)
                for output_parameter in parameter_linked_outputs:
                    if output_parameter.is_ready:
                        input_is_ready = True
                        if (output_parameter, node) in self.parameter_run_timestamp:
                            if self.parameter_run_timestamp[(output_parameter, node)] != output_parameter.timestamp:
                                one_input_has_changed = True
                        else:
                            one_input_has_changed = True
                all_inputs_are_ready = all_inputs_are_ready & input_is_ready
            starting_node = (len(node_linked_outputs) == 0)
            add_node = (starting_node or all_inputs_are_ready) and ((not node in self.run_nodes) or one_input_has_changed)
            if add_node:
               found_nodes.append(node) 
        return found_nodes
    
    def set_inputs(self, node):
        for parameter_name in node.inputs:
            parameter = node.inputs[parameter_name]
            linked_outputs = self.find_input_parameter_links(parameter)
            for output_parameter in linked_outputs:
                if output_parameter.is_ready:
                    parameter.set_value(output_parameter)
                # TODO handle the case (error?) where several outputs are ready

    def run(self):
        self.run_nodes = []
        self.error_nodes = {}
        while True:
            if not self.run_one_step():
                break
        
    def run_one_step(self):
        print("-- run one step")
        node_to_run = self.find_nodes_to_run()
        if len(node_to_run) == 0:
            return False
        for node in node_to_run:
            print("run " + node.name)
            self.set_inputs(node)
            try:
                node.process()
            except Exception as e:
                self.error_nodes[node] = str(e)
                raise(e)
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
        #for parameter_name in node.inputs:
        #    parameter = node.inputs[parameter_name]
        #    parameter.timestamp = self.timestamp
        #for parameter_name in node.outputs:
        #    parameter = node.outputs[parameter_name]
        #    parameter.timestamp = self.timestamp
        #self.timestamp = self.timestamp + 1
        for parameter_name in node.inputs:
            parameter = node.inputs[parameter_name]
            linked_outputs = self.find_input_parameter_links(parameter)
            for output_parameter in linked_outputs:
                if output_parameter.is_ready:
                    self.parameter_run_timestamp[(output_parameter, node)] = output_parameter.timestamp
