import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer
from PIL import Image
import numpy
#from testwindow import show_test_window

NODE_WINDOW_PADDING = imgui.Vec2(8.0, 8.0)

def add(vect1, vect2):
    res = imgui.Vec2(vect1.x + vect2.x, vect1.y + vect2.y)
    return res

class NodeInput:
    def __init__(self, ):
        self.name = "input"

class NodeOutput:
    def __init__(self, ):
        self.name = "output"

class NodeLink:
    def __init__(self, input_idx, input_slot, output_idx, output_slot):
        self.input_idx = input_idx
        self.input_slot = input_slot
        self.output_idx = output_idx
        self.output_slot = output_slot

class Node:
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

def load_image(image_name):
    image = Image.open(image_name).transpose( Image.FLIP_TOP_BOTTOM );
    textureData = numpy.array(list(image.getdata()), numpy.uint8)

    width = image.width
    height = image.height

    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA,
                    gl.GL_UNSIGNED_BYTE, textureData)

    return texture, width, height


def main():

    # states -------------------------
    nodes = []
    links = []
    scrolling = imgui.Vec2(0, 0)

    nodes.append(Node(0, "MainTex", imgui.Vec2(40, 50), 0.5, 1, 1))
    nodes.append(Node(1, "BumpMap", imgui.Vec2(40, 150), 0.42, 1, 1))
    nodes.append(Node(2, "Combine", imgui.Vec2(270, 80), 1.0, 2, 2))

    links.append(NodeLink(0,0,2,0))
    links.append(NodeLink(1,0,2,1))

    node_hovered_in_scene = -1
    node_selected = -1

    # states -------------------------

    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    io = imgui.get_io()

    image_texture, image_width, image_height = load_image("c:\\tmp\\Capture.PNG")

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()


        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()


        #------------------------------------------------------------
        imgui.begin("Output preview", True)
        imgui.text('An image:')
        imgui.image(image_texture, image_width, image_height)
        imgui.end()

        #------------------------------------------------------------
        imgui.begin("Example: Custom Node Graph", True)
        #imgui.begin_group()
        NODE_SLOT_RADIUS = 4.0

        # create our child canvas
        imgui.text("Hold middle mouse button to scroll")
        # imgui.same_line(imgui.get_window_width() - 100)
        imgui.push_style_var(imgui.STYLE_FRAME_PADDING, imgui.Vec2(1, 1))
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, imgui.Vec2(0, 0))
        imgui.begin_child("scrolling_region", 0, 0, True, imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE)
        imgui.pop_style_var()
        imgui.pop_style_var()
        imgui.push_item_width(120.0)

        offset = add(imgui.get_cursor_screen_pos(), scrolling)
        #print(scrolling)
        #print(imgui.get_cursor_screen_pos())
        #print(offset)
        draw_list = imgui.get_window_draw_list()

        # Display links
        draw_list.channels_split(2)
        draw_list.channels_set_current(0)
        for link in links:
            node_inp = nodes[link.input_idx]
            node_out = nodes[link.output_idx]
            p1 = add(offset, node_inp.get_intput_slot_pos(link.input_slot))
            p2 = add(offset, node_out.get_output_slot_pos(link.output_slot))
            #print(p1)
            #print(p2)
            draw_list.add_line(p1.x, p1.y, p2.x, p2.y, imgui.get_color_u32_rgba(1,1,0,1), 3)

        # Display nodes
        for node in nodes:
            imgui.push_id(str(node.id))
            node_rect_min = add(offset, node.pos)
            draw_list.channels_set_current(1) # foreground
            old_any_active = imgui.is_any_item_active()

            #display node content first
            # todo
            test = add(node_rect_min, NODE_WINDOW_PADDING)
            imgui.set_cursor_screen_position(add(node_rect_min, NODE_WINDOW_PADDING))
            imgui.begin_group()
            imgui.text("Hello")
            imgui.text(str(node_selected))
            imgui.end_group()

            # save size
            node_widgets_active = False # (not old_any_active and imgui.is_any_item_active())
            node.size = add( add( imgui.get_item_rect_size(), NODE_WINDOW_PADDING) , NODE_WINDOW_PADDING)
            node_rect_max = add(node.size, node_rect_min) 
            
            #display node box
            draw_list.channels_set_current(0) # background
            imgui.set_cursor_screen_position(node_rect_min)
            imgui.button("node", node.size.x, node.size.y) # TODO invisible_button
            if imgui.is_item_hovered():
                node_hovered_in_scene = node.id
                # open_context_menu |= ImGui::IsMouseClicked(1)

            node_moving_active = imgui.is_item_active()
            if node_widgets_active or node_moving_active:
                node_selected = node.id
            if (node_moving_active and imgui.is_mouse_dragging(0, 0.0) and node.id==node_selected):
               node.pos = add(node.pos, io.mouse_delta)

            draw_list.add_rect_filled(node_rect_min.x, node_rect_min.y, node_rect_max.x, node_rect_max.y, imgui.get_color_u32_rgba(1,0,0,0.5), 5)

            for node_input_index in range(len(node.inputs)):
                center = add(offset, node.get_intput_slot_pos(node_input_index))
                draw_list.add_circle_filled(center.x, center.y, 5, imgui.get_color_u32_rgba(0,1,0,1))

            for node_output_index in range(len(node.outputs)):
                center = add(offset, node.get_output_slot_pos(node_output_index))
                draw_list.add_circle_filled(center.x, center.y, 5, imgui.get_color_u32_rgba(0,1,1,1))

            imgui.pop_id()
        draw_list.channels_merge()

        imgui.pop_item_width()
        imgui.end_child()
        # to remove at the end
        imgui.end()

        gl.glClearColor(1., 1., 1., 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "minimal ImGui/GLFW3 example"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


if __name__ == "__main__":
    main()