import imgui # TODO remove this dependency

class IGGraph:
    def __init__(self):
        self.nodes = []
        self.links = []
        self.run_nodes = []
        self.error_nodes = {}
    
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
            for parameter in node.inputs:
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
        for parameter in node.inputs:
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
        return True

    def is_run(self, node):
        return node in self.run_nodes

    def is_error(self, node):
        return node in self.error_nodes