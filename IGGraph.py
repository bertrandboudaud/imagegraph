import imgui # TODO remove this dependency

class IGGraph:
    def __init__(self):
        self.nodes = []
        self.links = []
    
    def find_input_parameter_links(self, input_parameter):
        # find output parameters linked to this input parameter
        found_parameter = []
        for link in self.links:
            if input_parameter == link.input_parameter:
                found_parameter.append(link.output_parameter)
        return found_parameter

    def find_starting_nodes(self):
        found_nodes = []
        for node in self.nodes:
            nb_linked_input = 0
            for parameter in node.inputs:
                linked = self.find_input_parameter_links(parameter)
                nb_linked_input = nb_linked_input + len(linked)
            if nb_linked_input == 0:
                found_nodes.append(node)
        return found_nodes

    def run(self):
        self.run_nodes = []
        while True:
            if not self.run_one_step():
                break
        
    def run_one_step(self):
        node_to_run = []
        if len(self.run_nodes) == 0:
            node_to_run = self.find_starting_nodes()
        else:
            return False
        for node in node_to_run:
            node.process()
            self.run_nodes.append(node)
        return True
