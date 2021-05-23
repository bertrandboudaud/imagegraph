from flask import Flask
app = Flask(__name__)
import sys
from os.path import dirname
import json

sys.path.append(dirname(__file__) + "/..")

from IGNode import *
from IGGraph import *
from IGLibrary import *

@app.route('/')
def Welcome_page():
    return 'image_graph home page'

@app.route('/<graph_name>')
def load_graph(graph_name):
    # will show input of the graph
    fullname = "c:\\tmp\\" + graph_name + ".json" # TODO graph paths
    node_library = IGLibrary()
    iggraph = IGGraph(node_library)
    f=open(fullname)
    iggraph.from_json(json.load(f))
    f.close()
    input_nodes = iggraph.get_input_nodes()
    response = {}
    for input_node in input_nodes:
         key = input_node.inputs["parameter name"].text
         response[key] = input_node.to_json()
    return response

if __name__ == '__main__':
    app.run(debug="True")