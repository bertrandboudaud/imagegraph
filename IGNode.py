import imgui # TODO remove this dependency

class NodeInput:
    def __init__(self):
        self.name = "input"

class NodeOutput:
    def __init__(self):
        self.name = "output"

class NodeLink:
    def __init__(self, input_idx, input_slot, output_idx, output_slot):
        self.input_idx = input_idx
        self.input_slot = input_slot
        self.output_idx = output_idx
        self.output_slot = output_slot

class IGNode:
    def __init__(self, id, name, pos, value, input_count, output_count):
        self.id = id
        self.name = name
        self.pos = pos
        self.value = value
        self.size = imgui.Vec2(0,0)
        self.inputs = [NodeInput() for _ in range(input_count)]
        self.outputs = [NodeOutput() for _ in range(output_count)]

    def get_intput_slot_pos(self, slot_no):
        return imgui.Vec2(self.pos.x, self.pos.y + self.size.y*((slot_no+1) / (len(self.inputs)+1) ))

    def get_output_slot_pos(self, slot_no):
        return imgui.Vec2(self.pos.x + self.size.x, self.pos.y + self.size.y*((slot_no+1) / (len(self.outputs)+1) ))

class IGCreateImage(IGNode):
    def __init__(self, id):
        super().__init__(id, "Create Image", imgui.Vec2(0,0), 0, 1, 1)
