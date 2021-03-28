from IGParameter import *
from IGNode import *
from PIL import ImageOps

class IGCrop(IGNode):
    def __init__(self):
        super().__init__("Crop image", imgui.Vec2(200,100))
        self.add_input_parameter("source image", IGParameterImage()) 
        self.add_input_parameter("crop rectangle", IGParameterRectangle()) 
        self.add_output_parameter("cropped image", IGParameterImage())

    def process(self):
        crop_rect = self.inputs["crop rectangle"]
        self.outputs["cropped image"].image = self.inputs["source image"].image.crop((crop_rect.left, crop_rect.top, crop_rect.right, crop_rect.bottom))
        
