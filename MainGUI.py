import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer
from PIL import Image
import numpy
from IGNode import *
from IGGraph import *

NODE_WINDOW_PADDING = imgui.Vec2(8.0, 8.0)

def add(vect1, vect2):
    res = imgui.Vec2(vect1.x + vect2.x, vect1.y + vect2.y)
    return res

def init_texture():
    image_texture = gl.glGenTextures(1)
    return image_texture

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

def set_texture(image, texture):
    textureData = numpy.array(list(image.getdata()), numpy.uint8)

    width = image.width
    height = image.height

    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA,
                    gl.GL_UNSIGNED_BYTE, textureData)

    return texture, width, height

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

def main():

    # states -------------------------
    
    scrolling = imgui.Vec2(0, 0)

    iggraph = IGGraph()
    iggraph.create_node("Load Image")
#    image_load = IGLoadImage(3)
#    image_filter = IGFilterImage(4)
#    iggraph.nodes.append(image_load)
#    iggraph.nodes.append(image_filter)

    node_hovered_in_scene = -1
    node_selected = -1
    parameter_selected = None

    io_anchors_width = 10
    
    image_width = 0
    image_height = 0
    image_texture = None

    mouse_just_release = False  # workaround for creating the link
    # states -------------------------

    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    io = imgui.get_io()

    # image_texture, image_width, image_height = load_image("c:\\tmp\\Capture.PNG")
    image_texture = init_texture()

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
        imgui.begin("Output preview", True)
        if image_texture is not None and image_width>0 and image_height>0:
            # imgui.image(image_texture, image_width, image_height)
            window_width = imgui.get_window_width()
            display_width = 0
            display_height = 0
            if image_width >= image_height:
                display_width = window_width
                display_height = image_height / (image_width/float(display_width))
            else:
                display_height = window_width
                display_width = image_width / (image_height/float(display_height))
            imgui.image(image_texture, display_width, display_height)
            imgui.text("width: " + str(image_width))
            imgui.text("height: " + str(image_height))
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
                imgui.invisible_button("input", io_anchors_width, io_anchors_width)
                if imgui.is_item_hovered():
                    if parameter_selected and mouse_just_release:
                        iggraph.links.append(NodeLink(parameter_selected, parameter))
                        # todo forbid 2 node links
                draw_list.add_circle_filled(center_with_offset.x, center_with_offset.y, io_anchors_width/2, get_parameter_color(parameter))

            # output parameters
            for parameter_name in node.outputs:
                parameter = node.outputs[parameter_name]
                center = node.get_output_slot_pos(parameter)
                center_with_offset = add(offset, center)
                imgui.set_cursor_pos(imgui.Vec2(center.x-io_anchors_width/2, center.y-io_anchors_width/2))
                if (imgui.invisible_button("output", io_anchors_width, io_anchors_width)):
                    if parameter.image:
                        image_texture, image_width, image_height = set_texture(parameter.image, image_texture)
                creating_link_active = imgui.is_item_active()
                draw_list.add_circle_filled(center_with_offset.x, center_with_offset.y, io_anchors_width/2, get_parameter_color(parameter))
                if creating_link_active:
                    parameter_selected = parameter

            if parameter_selected and imgui.is_mouse_dragging(0, 0.0):
                draw_link_param_to_point(draw_list, offset, parameter_selected, io.mouse_pos.x, io.mouse_pos.y)
            elif parameter_selected and not imgui.is_mouse_dragging(0, 0.0) and not mouse_just_release:
                mouse_just_release = True
            else:
                mouse_just_release = False
                parameter_selected = False

            if node_widgets_active or node_moving_active:
                node_selected = node.id
            if (node_moving_active and imgui.is_mouse_dragging(0, 0.0) and node.id==node_selected):
               node.pos = add(node.pos, io.mouse_delta)

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