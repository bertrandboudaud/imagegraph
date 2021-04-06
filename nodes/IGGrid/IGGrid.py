from IGParameter import *
from IGNode import *
from PIL import ImageOps

class IGGrid(IGNode):
    def __init__(self):
        super().__init__("Grid Rectangles")
        self.add_input_parameter("source image", IGParameterImage()) 
        self.add_input_parameter("number of horizontal cells", IGParameterInteger())
        self.add_input_parameter("number of vertical cells", IGParameterInteger())
        self.add_output_parameter("cells", IGParameterList()) 

    def process(self):
        source = self.inputs["source image"].image
        width = source.width
        height = source.height
        nb_cells_x = self.inputs["number of horizontal cells"].value
        nb_cells_y = self.inputs["number of vertical cells"].value
        cell_width = source.width / nb_cells_x
        cell_height = source.height / nb_cells_y
        for y in range(nb_cells_y):
            for x in range(nb_cells_x):
                new_rectangle = IGParameterRectangle()
                new_rectangle.left = x * cell_width
                new_rectangle.top = y * cell_height
                new_rectangle.right = new_rectangle.left + cell_width
                new_rectangle.bottom = new_rectangle.top + cell_height
                self.outputs["cells"].list.append(new_rectangle)
        self.set_all_outputs_ready()
