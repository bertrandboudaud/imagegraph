from IGNode import *
from IGGraph import *
import json

class IGScriptNode(IGNode):
    def __init__(self, name, json_file, library):
        super().__init__(name)
        self.iggraph = IGGraph(library)
        f=open(json_file)
        self.iggraph.from_json(json.load(f))
        f.close()
        for input_node in self.iggraph.get_input_nodes():
            self.add_input_parameter(input_node.inputs["parameter name"].text, 
                                     library.create_parameter(input_node.inputs["default value"].type)) 
        for output_node in self.iggraph.get_output_nodes():
            self.add_output_parameter(output_node.inputs["parameter name"].text, 
                                     library.create_parameter(output_node.outputs["output"].type)) 

    def process(self):
        self.iggraph.run()
        self.set_all_outputs_ready()
