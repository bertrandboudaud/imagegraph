from flask import Flask, jsonify
app = Flask(__name__)
import sys
from os.path import dirname
import json
from flask_cors import CORS
from flask import request

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

sys.path.append(dirname(__file__) + "/..")

from IGNode import *
from IGGraph import *
from IGLibrary import *

@app.route('/')
def Welcome_page():
    return 'image_graph home page'

@app.route('/<graph_name>', methods = ['GET', 'POST'])
def load_graph(graph_name):
    # will show input of the graph
    fullname = "c:\\tmp\\" + graph_name + ".json" # TODO graph paths
    node_library = IGLibrary()
    iggraph = IGGraph(node_library)
    f=open(fullname)
    iggraph.from_json(json.load(f))
    f.close()
    if request.method == 'GET':
        input_nodes = iggraph.get_input_nodes()
        response = {}
        for input_node in input_nodes:
            key = input_node.inputs["parameter name"].text
            response[key] = input_node.to_json()
        return  jsonify({
            'status': 'success',
            'inputs': response
        })
    if request.method == 'POST':
        input_nodes = iggraph.get_input_nodes()
        inputs = {}
        for input_node in input_nodes:
            parameter_name = input_node.inputs["parameter name"].text
            inputs[parameter_name] = input_node.inputs["default value"].get_value()
        post_data = request.get_json()
        print(str(post_data))
        for parameter_name in post_data:
            arg_value = post_data[parameter_name]
            if isinstance(inputs[parameter_name]["value"], int):
                inputs[parameter_name]["value"] = int(arg_value)
            elif isinstance(inputs[parameter_name]["value"], float):
                inputs[parameter_name]["value"] = float(arg_value)
            else:
                inputs[parameter_name]["value"] = arg_value

        # run graph
        iggraph.run()

        # display outputs
        response = {}
        output_nodes = iggraph.get_output_nodes()
        for output_node in output_nodes:
            parameter_name = output_node.inputs["parameter name"].text
            output_parameter = output_node.outputs["output"]
            response[parameter_name] = {}
            for field in output_parameter.get_value():
                response[parameter_name][field] = str(output_parameter.get_value()[field])

        return  jsonify({
            'status': 'success',
            'inputs': response
        })        

if __name__ == '__main__':
    app.run(debug="True")