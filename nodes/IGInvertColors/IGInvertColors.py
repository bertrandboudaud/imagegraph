from IGParameter import *
from IGNode import *
from PIL import ImageFilter
from PIL import ImageOps

class IGInvertColors(IGNode):
    def __init__(self):
        super().__init__("Invert colors", imgui.Vec2(200,100))
        self.add_input_parameter("source image", IGParameterImage()) 
        self.add_output_parameter("filtered image", IGParameterImage()) 

    def process(self):
        if self.inputs["source image"].image.mode == 'RGBA':
            r,g,b,a = self.inputs["source image"].image.split()
            rgb_image = Image.merge('RGB', (r,g,b))
            inverted_image = ImageOps.invert(rgb_image)
            r2,g2,b2 = inverted_image.split()
            final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
            self.outputs["filtered image"].image = final_transparent_image
        
