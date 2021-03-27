import imgui # TODO remove this dependency
from IGParameter import *
from PIL import ImageFilter
from PIL import ImageOps

class NodeLink:
    def __init__(self, output_parameter, input_parameter):
        self.input_parameter = input_parameter
        self.output_parameter = output_parameter

class IGNode:
    def __init__(self, id, name, pos):
        self.id = id
        self.name = name
        self.pos = pos
        self.size = imgui.Vec2(0,0)
        self.inputs = []
        self.outputs = []

    def get_intput_slot_pos(self, parameter):
        slot_no = 0
        for input_parameter in self.inputs: # replace with map and name of the parameter
            if input_parameter == parameter:
                break
            slot_no = slot_no + 1 
        return imgui.Vec2(self.pos.x, self.pos.y + self.size.y*((slot_no+1) / (len(self.inputs)+1) ))

    def get_output_slot_pos(self, parameter):
        slot_no = 0
        for output_parameter in self.outputs: # replace with map and name of the parameter
            if output_parameter == parameter:
                break
            slot_no = slot_no + 1 
        return imgui.Vec2(self.pos.x + self.size.x, self.pos.y + self.size.y*((slot_no+1) / (len(self.outputs)+1) ))

class IGCreateImage(IGNode):
    def __init__(self, id):
        super().__init__(id, "Create Image", imgui.Vec2(50,50))
        self.created_image = IGParameterImage("created image", self) 
        self.outputs.append(self.created_image)
    
    def process(self):
        mode = 'RGBA'
        size = (128, 128)
        color = (73, 109, 137)
        self.created_image.image = Image.new(mode, size, color)

class IGLoadImage(IGNode):
    def __init__(self, id):
        super().__init__(id, "Load Image", imgui.Vec2(50,50))
        self.loaded_image = IGParameterImage("loaded image", self) 
        self.outputs.append(self.loaded_image)
    
    def process(self):
        self.url = "c:\\tmp\\Capture.PNG"
        self.loaded_image.image = Image.open(self.url).transpose( Image.FLIP_TOP_BOTTOM );

class IGFilterImage(IGNode):
    def __init__(self, id):
        super().__init__(id, "Filter Image", imgui.Vec2(200,100))
        self.source_image = IGParameterImage("source image", self) 
        self.inputs.append(self.source_image)
        self.filter_image = IGParameterImage("filtered image", self)
        self.outputs.append(self.filter_image)

    def process(self):
        if self.source_image.image.mode == 'RGBA':
            r,g,b,a = self.source_image.image.split()
            rgb_image = Image.merge('RGB', (r,g,b))
            inverted_image = ImageOps.invert(rgb_image)
            r2,g2,b2 = inverted_image.split()
            final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
            self.filter_image.image = final_transparent_image
        
