import glfw
import OpenGL.GL as gl
import tkinter as tk
from tkinter import filedialog
import imgui
from imgui.integrations.glfw import GlfwRenderer
from PIL import Image
from PIL import ImageOps
import numpy
from IGNode import *
from IGGraph import *

NODE_WINDOW_PADDING = imgui.Vec2(8.0, 8.0)

class ImageToTexture:
    def __init__(self):
        self.image = None
        self.timestamp = 0
        self.gl_texture = 0
        self.gl_widh =0
        self.gl_height = 0
        self.last_used = 0

image_to_texture_last_used = 0
image_to_textures = []

def add(vect1, vect2):
    res = imgui.Vec2(vect1.x + vect2.x, vect1.y + vect2.y)
    return res

def get_gl_texture(image, timestamp):
    global image_to_texture_last_used
    image_to_texture_last_used = image_to_texture_last_used + 1
    for image_to_texture in image_to_textures:
        if image_to_texture.image == image and image_to_texture.timestamp == timestamp:
            image_to_texture.last_used = image_to_texture_last_used
            return image_to_texture
        if image_to_texture.image == image and image_to_texture.timestamp != timestamp:
            width, height = set_texture(image_to_texture.image, image_to_texture.gl_texture)
            image_to_texture.gl_widh = width
            image_to_texture.gl_height = height
            image_to_texture.last_used = image_to_texture_last_used
            image_to_texture.timestamp = timestamp
            return image_to_texture
    minimum_last_used = image_to_textures[0]
    for image_to_texture in image_to_textures:
        if image_to_texture.last_used < minimum_last_used.last_used:
            minimum_last_used = image_to_texture
    width, height = set_texture(image, minimum_last_used.gl_texture)
    minimum_last_used.image = image
    minimum_last_used.gl_widh = width
    minimum_last_used.gl_height = height
    minimum_last_used.last_used = image_to_texture_last_used
    minimum_last_used.timestamp = timestamp
    return minimum_last_used

def init_textures():
    for i in range(16):
        image_to_texture = ImageToTexture()
        image_to_texture.gl_texture = gl.glGenTextures(1)
        image_to_textures.append(image_to_texture)

def set_texture(image, texture):
    max_width = 256
    max_height = 256

    # maybe for later ... resized_image = ImageOps.fit(image, (max_width, max_height))
    resized_image = image
    textureData = numpy.array(list(resized_image.getdata()), numpy.uint8)

    width = resized_image.width
    height = resized_image.height

    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA,
                    gl.GL_UNSIGNED_BYTE, textureData)

    return width, height

# draw link between 2 params
def draw_link_param_to_param(draw_list, offset, output_parameter, input_parameter):
    node_inp = input_parameter.owner
    node_out = output_parameter.owner
    p1 = add(offset, node_inp.get_intput_slot_pos(input_parameter))
    p2 = add(offset, node_out.get_output_slot_pos(output_parameter))
    draw_link(draw_list, p1.x, p1.y, p2.x, p2.y, output_parameter)

# draw link between 1 param, 1 point
def draw_link_param_to_point(draw_list, offset, parameter, p2_x, p2_y):
    node_out = parameter.owner
    p1 = add(offset, node_out.get_output_slot_pos(parameter))
    draw_link(draw_list, p1.x, p1.y, p2_x, p2_y, parameter)

# draw link between 2 points
def draw_link(draw_list, p1_x, p1_y, p2_x, p2_y, parameter):
    draw_list.add_line(p1_x, p1_y, p2_x, p2_y,  get_parameter_color(parameter), 3)

def get_parameter_color(parameter):
    if (parameter.type == "Image"):
        return imgui.get_color_u32_rgba(1,0,0,0.7)
    if (parameter.type == "Rectangle"):
        return imgui.get_color_u32_rgba(0,1,0,0.7)
    if (parameter.type == "Color"):
        return imgui.get_color_u32_rgba(1,1,0,0.7)
    if (parameter.type == "URL"):
        return imgui.get_color_u32_rgba(0,1,1,0.7)
    else:
        # unknown
        return imgui.get_color_u32_rgba(1,1,1,0.2)

def get_node_color(node, iggraph, hovered):
    node_color = imgui.get_color_u32_rgba(0,0.5,1,0.5)
    if iggraph.is_error(node):
        if hovered:
            node_color = imgui.get_color_u32_rgba(1,0,0,0.7)
        else:
            node_color = imgui.get_color_u32_rgba(1,0,0,0.5)
    elif iggraph.is_run(node):
        if hovered:
            node_color = imgui.get_color_u32_rgba(0,1,0,0.7)
        else:
            node_color = imgui.get_color_u32_rgba(0,1,0,0.5)
    elif hovered:
        node_color = imgui.get_color_u32_rgba(0,0.5,1,0.7)
    return node_color

def display_parameter(parameter):
    if imgui.tree_node(parameter.id):
        if parameter.type == "Image":
            if parameter.image:
                image_to_texture = get_gl_texture(parameter.image, parameter.timestamp)
                # imgui.image(image_texture, image_width, image_height)
                window_width = 256 # imgui.get_window_width()
                display_width = 0
                display_height = 0
                image_width = image_to_texture.gl_widh
                image_height = image_to_texture.gl_height
                if image_width >= image_height:
                    display_width = window_width
                    display_height = image_height / (image_width/float(display_width))
                else:
                    display_height = window_width
                    display_width = image_width / (image_height/float(display_height))
                imgui.image(image_to_texture.gl_texture, display_width, display_height)
                imgui.text("width: " + str(image_width))
                imgui.text("height: " + str(image_height))
            else:
                imgui.text("No image available - run workflow or connect an image source")
        elif parameter.type == "Rectangle":
            imgui.text("Left: " + str(parameter.left))
            imgui.text("Top: " + str(parameter.top))
            imgui.text("Right: " + str(parameter.right))
            imgui.text("Bottom: " + str(parameter.bottom))
        elif parameter.type == "Color":
            changed, color = imgui.color_edit4(parameter.id, parameter.r, parameter.g, parameter.b, parameter.a)
            if changed:
                parameter.r = color[0]
                parameter.g = color[1]
                parameter.b = color[2]
                parameter.a = color[3]
        elif parameter.type == "URL":
            changed, textval = imgui.input_text(parameter.id, parameter.url, 1024)
            if changed:
                parameter.url = textval
            if imgui.button("browse..."):
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename()
                if file_path:
                    parameter.url = file_path
        imgui.tree_pop()

def main():

    # states -------------------------
    
    scrolling = imgui.Vec2(0, 0)

    iggraph = IGGraph()
    iggraph.create_node("Load Image")

    node_hovered_in_scene = -1
    node_selected = None
    parameter_link_start = None
    selected_parameter = None

    io_anchors_width = 10
    
    image_width = 0
    image_height = 0
    image_texture = None

    # states -------------------------

    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    io = imgui.get_io()

    init_textures()

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
        imgui.begin("Library", True)
        for node_name in iggraph.node_library.nodes:
            if imgui.button(node_name):
                iggraph.create_node(node_name)
        imgui.end()

        #------------------------------------------------------------
        imgui.begin("Node View", True)
        if node_selected:
            if imgui.tree_node("Inputs"):
                for parameter_name in node_selected.inputs:
                    parameter = node_selected.inputs[parameter_name]
                    display_parameter(parameter)
                imgui.tree_pop()
            if imgui.tree_node("Output"):
                for parameter_name in node_selected.outputs:
                    parameter = node_selected.outputs[parameter_name]
                    display_parameter(parameter)
                imgui.tree_pop()

        imgui.end()

        #------------------------------------------------------------
        imgui.begin("Example: Custom Node Graph", True)
        #imgui.begin_group()
        NODE_SLOT_RADIUS = 4.0

        # create our child canvas
        if imgui.button("run"):
            iggraph.run()
        imgui.same_line()
        if imgui.button("run one step"):
            iggraph.run_one_step()
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
        for link in iggraph.links:
            draw_link_param_to_param(draw_list, offset, link.output_parameter, link.input_parameter)

        # Display nodes
        for node in iggraph.nodes:
            imgui.push_id(str(node.id))
            node_rect_min = add(offset, node.pos)
            draw_list.channels_set_current(1) # foreground
            old_any_active = imgui.is_any_item_active()

            #display node content first
            # todo
            test = add(node_rect_min, NODE_WINDOW_PADDING)
            imgui.set_cursor_screen_position(add(node_rect_min, NODE_WINDOW_PADDING))
            imgui.begin_group()
            imgui.text("")
            imgui.text(node.name)
            imgui.text("")
            imgui.end_group()

            # save size
            node_widgets_active = False # (not old_any_active and imgui.is_any_item_active())
            node.size = add( add( imgui.get_item_rect_size(), NODE_WINDOW_PADDING) , NODE_WINDOW_PADDING)
            node_rect_max = add(node.size, node_rect_min) 
            
            #display node box
            draw_list.channels_set_current(0) # background
            imgui.set_cursor_screen_position(node_rect_min)
            imgui.invisible_button("", node.size.x, node.size.y)
            if imgui.is_item_hovered():
                node_hovered_in_scene = node.id
            else:
                node_hovered_in_scene = None
            node_moving_active = imgui.is_item_active()
            draw_list.add_rect_filled(node_rect_min.x, node_rect_min.y, node_rect_max.x, node_rect_max.y, get_node_color(node, iggraph, node_hovered_in_scene), 5)
            if node_hovered_in_scene and iggraph.is_error(node):
                imgui.begin_tooltip()
                imgui.text(iggraph.error_nodes[node])
                imgui.end_tooltip()

            # input parameters
            for parameter_name in node.inputs:
                parameter = node.inputs[parameter_name]
                center = node.get_intput_slot_pos(parameter)
                center_with_offset = add(offset, center)
                imgui.set_cursor_pos(imgui.Vec2(center.x-io_anchors_width/2, center.y-io_anchors_width/2))
                imgui.push_id(str(str(node.id) + "input" + parameter.id))
                if (imgui.invisible_button("input", io_anchors_width, io_anchors_width)):
                    selected_parameter = parameter
                if imgui.is_item_hovered():
                    if parameter_link_start:
                        iggraph.links.append(NodeLink(parameter_link_start, parameter))
                        # todo forbid 2 node links
                imgui.pop_id()
                draw_list.add_circle_filled(center_with_offset.x, center_with_offset.y, io_anchors_width/2, get_parameter_color(parameter))

            # output parameters
            for parameter_name in node.outputs:
                parameter = node.outputs[parameter_name]
                center = node.get_output_slot_pos(parameter)
                center_with_offset = add(offset, center)
                imgui.set_cursor_pos(imgui.Vec2(center.x-io_anchors_width/2, center.y-io_anchors_width/2))
                if (imgui.invisible_button("output", io_anchors_width, io_anchors_width)):
                    selected_parameter = parameter
                creating_link_active = imgui.is_item_active()
                draw_list.add_circle_filled(center_with_offset.x, center_with_offset.y, io_anchors_width/2, get_parameter_color(parameter))
                if creating_link_active:
                    parameter_link_start = parameter

            if node_widgets_active or node_moving_active:
                node_selected = node
            if (node_moving_active and imgui.is_mouse_dragging(0, 0.0) and node.id==node_selected.id):
               node.pos = add(node.pos, io.mouse_delta)

            imgui.pop_id()
        draw_list.channels_merge()

        if parameter_link_start and imgui.is_mouse_dragging(0, 0.0):
            draw_link_param_to_point(draw_list, offset, parameter_link_start, io.mouse_pos.x, io.mouse_pos.y)
        elif parameter_link_start and not imgui.is_mouse_dragging(0, 0.0):
            parameter_link_start = False

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