from IGNode import *

class IGLibrary:
    def __init__(self):
        self.nodes = {} # TODO use it later
   
    def create_node(self, node_name):
        # TODO discovery of nodes
        if (node_name == "Load Image"):
            return IGLoadImage()
        elif (node_name == "Invert Color"):
            return IGFilterImage()
        else:
            raise Exception("Unknown node " + node_name)
        