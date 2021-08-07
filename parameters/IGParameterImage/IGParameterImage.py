from IGParameter import *
import base64
from PIL import Image
import copy
import tempfile
import os
import json

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

    def to_json(self, running_parameter = False):
        json = {}
        json["id"]=self.id
        json["type"]=self.type
        if running_parameter:
            json["value"] = self.image_to_json(self._value['image'])
        else:
            json["value"] = self.image_to_json(self._backup_value['image'])
        return json

    def image_to_json(self, image):
        fd, path = tempfile.mkstemp()
        print("file created: " + path)
        data = ""
        try:
            image.save(path,"PNG")
            with open(path, mode='rb') as file:
                img = file.read()
            data = "data:image/png;base64,"+base64.b64encode(img).decode('utf-8')
        finally:
            pass
        #    os.remove(path)
        # base64.b64encode(self._value['image'])
        return data
