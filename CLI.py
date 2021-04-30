import math 
import numpy
from IGNode import *
from IGGraph import *
import json
import argparse
import sys as _sys

def main():
    args = _sys.argv[1:]    
    # args for for the client
    main_args = []
    # args for the graph
    graph_args = []
    # split command line
    current_args = main_args
    for arg in args:
        if arg=="--":
            current_args = graph_args
        else:
            current_args.append(arg)

    main_args_parser = argparse.ArgumentParser(description='Process a graph.')
    main_args_parser.add_argument('graph', nargs=1, help='json graph to run')
    main_args = main_args_parser.parse_args(main_args)

    # load graph
    iggraph = IGGraph()
    f=open(main_args.graph[0])
    iggraph.from_json(json.load(f))
    f.close()

    # get inputs
    inputs = {}
    graph_args_parser = argparse.ArgumentParser(description='Graph inputs')
    input_nodes = iggraph.get_input_nodes()
    for input_node in input_nodes:
        parameter_name = input_node.inputs["parameter name"].text.replace(" ","_")
        for field in input_node.inputs["default value"].get_value():
            parameter_name_with_field = parameter_name + "." + field
            option_name = "--" + parameter_name_with_field
            graph_args_parser.add_argument(option_name, nargs='?', help='')
            inputs[parameter_name_with_field] = {"field": field, "value" : input_node.inputs["default value"].get_value() }
    graph_args = graph_args_parser.parse_args(graph_args)
    for parameter in inputs:
        arg_value = graph_args.__getattribute__(parameter)
        if arg_value is not None:
            param_bucket = inputs[parameter]
            field = param_bucket["field"]
            value = param_bucket["value"]
            if isinstance(value[field], int):
                value[field] = int(arg_value)
            elif isinstance(value[field], float):
                value[field] = float(arg_value)
            else:
                value[field] = arg_value

    # run graph
    iggraph.run()

    # display outputs
    output_nodes = iggraph.get_output_nodes()
    for output_node in output_nodes:
        parameter_name = output_node.inputs["parameter name"].text
        output_parameter = output_node.outputs["output"]
        if (output_parameter.type == "Image"): # todo handlers
            output_parameter.image.show()
        else:
            for field in output_parameter.get_value():
                print(parameter_name + ", " + field + ": " + str(output_parameter.get_value()[field]))

if __name__ == "__main__":
    main()