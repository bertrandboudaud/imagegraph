import pytest

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from IGLibrary import *

def test_load_image_from_file():
    lib = IGLibrary()
    node = lib.create_node("Load Image") 
    assert node is not None, "Creation Failed"
    node.inputs["url"].url = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","high_map.png")
    node.process()
    width, height = node.outputs["loaded image"].image.size
    assert width == 512, "incorrect image width"
    assert height == 512, "incorrect image height"
