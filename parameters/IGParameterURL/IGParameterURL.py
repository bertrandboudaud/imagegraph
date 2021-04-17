from IGParameter import *
from PIL import Image
import copy

class IGParameterURL(IGParameter):
    def __init__(self):
        super().__init__("URL")
        self._value["url"] = "c:\\tmp\Capture.PNG"

    @property
    def url(self):
        return self._value["url"]

    @url.setter
    def url(self, url):
        self._value["url"] = url

