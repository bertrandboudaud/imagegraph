from IGParameter import *
from PIL import Image
import copy

class IGParameterImage(IGParameter):
    def __init__(self):
        super().__init__("Image")
        self._value["image"] = None
    
    @property
    def image(self):
        return self._value["image"]

    @image.setter
    def image(self, image):
        self._value["image"] = image


