import imgui # TODO remove this dependency
from IGLibrary import *
from IGNode import *
from enum import Enum

class IGGraph:

    STATE_IDLE = 1
    STATE_RUNNING = 2

    def __init__(self, node_library):
        self.nodes = []
        self.links = []
        self.run_nodes = []
        self.error_nodes = {}
        self.id_generator = 1
        self.node_library = node_library
        self.timestamp = 1
        self.parameter_run_timestamp = {}
        self.catch_exceptions = True
        self.state = self.STATE_IDLE
    
    def to_json(self):
        json = {}
        nodes = []
        for node in self.nodes:
            nodes.append(node.to_json())
        json["nodes"] = nodes
        links = []
        for link in self.links:
            links.append(link.to_json())
        json["links"] = links
        return json

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def from_json(self, json):
        json_nodes = json["nodes"]
        for json_node in json_nodes:
            node = self.node_library.create_node(json_node["name"])
            node.from_json(json_node)
            self.nodes.append(node)
        json_links = json["links"]
        for json_link in json_links:
            json_output_parameter = json_link["output_parameter"]
            output_node = self.get_node_from_id(json_output_parameter["node_id"])
            output_parameter = output_node.outputs[json_output_parameter["parameter_id"]]
            json_input_parameter = json_link["input_parameter"]
            input_node = self.get_node_from_id(json_input_parameter["node_id"])
            input_parameter = input_node.inputs[json_input_parameter["parameter_id"]]
            self.add_link(output_parameter, input_parameter)

    def get_node_from_id(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return None

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

    def get_input_nodes(self):
        input_nodes = []
        for node in self.nodes:
            if node.name == "Input":
                input_nodes.append(node)
        return input_nodes

    def get_output_nodes(self):
        output_nodes = []
        for node in self.nodes:
            if node.name == "Output":
                output_nodes.append(node)
        return output_nodes

    def run(self):
        self.run_nodes = []
        self.error_nodes = {}
        while True:
            if not self.run_one_step():
                break
        
    def run_one_step(self):
        # print("-- run one step")
        nodes_to_run = self.find_nodes_to_run()
        if len(nodes_to_run) == 0:
            return False
        for node in nodes_to_run:
            # print("run " + node.name)
            self.set_inputs(node)
            try:
                node.process()
            except Exception as e:
                self.error_nodes[node] = repr(e)
                if not self.catch_exceptions:
                    raise(e)
            self.run_nodes.append(node)
            self.update_timestamps(node)
        return True

    def is_run(self, node):
        return node in self.run_nodes

    def is_error(self, node):
        return node in self.error_nodes
    
    def generate_id(self):
        id_exists = True
        while id_exists:
            self.id_generator = self.id_generator +1
            id_exists = False
            for node in self.nodes:
                if node.id == self.id_generator:
                    id_exists = True
                    break
        return self.id_generator

    def create_node(self, node_name, pos = imgui.Vec2(0,0)):
        new_node = self.node_library.create_node(node_name)
        new_node.id = self.generate_id()
        new_node.pos = pos
        self.nodes.append(new_node)
        return new_node

    def remove_node(self, node):
        # first remove links
        links_to_remove = []
        for link in self.links:
            if (link.input_parameter.owner == node) or (link.output_parameter.owner == node):
                links_to_remove.append(link)
        for link in links_to_remove:
            self.links.remove(link)
        self.nodes.remove(node)

    def update_timestamps(self, node):
        for parameter_name in node.inputs:
            parameter = node.inputs[parameter_name]
            linked_outputs = self.find_input_parameter_links(parameter)
            for output_parameter in linked_outputs:
                if output_parameter.is_ready:
                    self.parameter_run_timestamp[(output_parameter, node)] = output_parameter.timestamp

    def reset(self):
        for node in self.nodes:
            node.reset()
        self.run_nodes = []
        self.error_nodes = {}
        self.parameter_run_timestamp = {}

    def add_link(self, output_parameter, input_parameter):
        # TODO remove notification on parameter. go through the node to be notified only
        output_parameter.on_connected_to(input_parameter)
        output_parameter.owner.on_output_connected_to(input_parameter)
        input_parameter.on_connected_to(output_parameter)
        input_parameter.owner.on_input_connected_to(output_parameter)
        self.links.append(NodeLink(output_parameter, input_parameter))

    def prepare_to_run(self):
        for node in self.nodes:
            node.preapre_to_process()
