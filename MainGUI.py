import glfw
import OpenGL.GL as gl
import tkinter as tk
from tkinter import filedialog
import imgui
import math 
from imgui.integrations.glfw import GlfwRenderer
from PIL import Image
from PIL import ImageOps
import numpy
from IGNode import *
from IGGraph import *
import json

NODE_WINDOW_PADDING = imgui.Vec2(8.0, 8.0)
previous_key_callback = None
selected_link = None
selected_node = None
iggraph = None
debug_is_mouse_dragging = False
show_debug_window = False
slider_indexes = {}

class ImageToTexture:
    def __init__(self):
        self.image = None
        self.timestamp = 0
        self.gl_texture = 0
        self.gl_widh = 0
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
    size = 256, 256
    resized_image = image.copy()
    resized_image.thumbnail(size, Image.ANTIALIAS)
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
def draw_link_param_to_param(draw_list, offset, output_parameter, input_parameter, hovered):
    node_inp = input_parameter.owner
    node_out = output_parameter.owner
    p1 = add(offset, node_inp.get_intput_slot_pos(input_parameter))
    p2 = add(offset, node_out.get_output_slot_pos(output_parameter))
    draw_link(draw_list, p1.x, p1.y, p2.x, p2.y, output_parameter, hovered)

# draw link between 1 param, 1 point
def draw_link_param_to_point(draw_list, offset, parameter, p2_x, p2_y, hovered):
    node_out = parameter.owner
    p1 = add(offset, node_out.get_output_slot_pos(parameter))
    draw_link(draw_list, p1.x, p1.y, p2_x, p2_y, parameter, hovered)

# draw link between 2 points
def draw_link(draw_list, p1_x, p1_y, p2_x, p2_y, parameter, hovered):
    thickness = 2
    if hovered:
        thickness = 3
    draw_list.add_line(p1_x, p1_y, p2_x, p2_y,  get_parameter_color(parameter), thickness)

def get_parameter_color(parameter):
    if (parameter.type == "Image"):
        return imgui.get_color_u32_rgba(1,0,0,0.7)
    if (parameter.type == "Rectangle"):
        return imgui.get_color_u32_rgba(0,1,0,0.7)
    if (parameter.type == "Coordinates"):
        return imgui.get_color_u32_rgba(0.625,0.32,0.17,0.7)
    if (parameter.type == "Color"):
        return imgui.get_color_u32_rgba(1,1,0,0.7)
    if (parameter.type == "Integer"):
        return imgui.get_color_u32_rgba(1,1,1,0.7)
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

def display_parameter(parameter, editable):
    global slider_indexes
    if parameter.type == "List":
        if parameter.id not in slider_indexes:
            slider_indexes[parameter.id] = 0
        changed, values = imgui.slider_int("index", slider_indexes[parameter.id], 0, len(parameter.list)-1)
        if changed:
            slider_indexes[parameter.id] = values
        display_parameter(parameter.list[slider_indexes[parameter.id]], editable)
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
            imgui.text("width: " + str(parameter.image.width))
            imgui.text("height: " + str(parameter.image.height))
        else:
            imgui.text("No image available - run workflow or connect an image source")
    elif parameter.type == "Rectangle":
        if editable:
            changed, value = imgui.input_float("Left", parameter.left)
            if changed:
                parameter.left = value
            changed, value = imgui.input_float("Top", parameter.top)
            if changed:
                parameter.top = value
            changed, value = imgui.input_float("Right", parameter.right)
            if changed:
                parameter.right = value
            changed, value = imgui.input_float("Bottom", parameter.bottom)
            if changed:
                parameter.left = value
        else:
            imgui.text("Left: " + str(parameter.left))
            imgui.text("Top: " + str(parameter.top))
            imgui.text("Right: " + str(parameter.right))
            imgui.text("Bottom: " + str(parameter.bottom))
    elif parameter.type == "Coordinates":
        if editable:
            changed, value = imgui.input_float("x", parameter.x)
            if changed:
                parameter.x = value
            changed, value = imgui.input_float("y", parameter.y)
            if changed:
                parameter.y = value
        else:
            imgui.text("x: " + str(parameter.x))
            imgui.text("y: " + str(parameter.y))
    elif parameter.type == "Integer": # to do change to "number"
        if editable:
            changed, value = imgui.input_int("Value", parameter.value)
            if changed:
                parameter.value = value
        else:
            imgui.text("Value: " + str(parameter.value))
    elif parameter.type == "Color":
        changed, color = imgui.color_edit4(parameter.id, parameter.r, parameter.g, parameter.b, parameter.a)
        if editable and changed:
            parameter.r = color[0]
            parameter.g = color[1]
            parameter.b = color[2]
            parameter.a = color[3]
    elif parameter.type == "URL":
        changed, textval = imgui.input_text(parameter.id, parameter.url, 1024)
        if editable and changed:
            parameter.url = textval
        if editable:
            if imgui.button("browse..."):
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename()
                if file_path:
                    parameter.url = file_path
    elif parameter.type == "Text":
        changed, textval = imgui.input_text(parameter.id, parameter.text, 1024)
        if editable and changed:
            parameter.text = textval

def key_event(window,key,scancode,action,mods):
    global iggraph
    global selected_link
    global selected_node
    key_consumed = False;
    if action == glfw.PRESS and key == glfw.KEY_DELETE:
        if selected_link:
            iggraph.links.remove(selected_link)
            selected_link = None
            key_consumed = True
        elif selected_node:
            iggraph.remove_node(selected_node)
            selected_node = None
            key_consumed = True
    if not key_consumed:
        previous_key_callback(window,key,scancode,action,mods)

width_library = 200
width_shematic = 400
width_context = 200
height_window = 800
separator_width = 4

def example_mosaic(iggraph):
    # Example
    node_load_image = iggraph.create_node("Load Image", imgui.Vec2(200,100))
    node_load_image2 = iggraph.create_node("Load Image", imgui.Vec2(200,500))
    node_relative_coord = iggraph.create_node("Relative Coords", imgui.Vec2(400,400))
    node_pixel_color = iggraph.create_node("Pixel Color", imgui.Vec2(600,400))
    node_colorize_image = iggraph.create_node("Colorize Image", imgui.Vec2(800,400))
    node_grid = iggraph.create_node("Grid Rectangles", imgui.Vec2(400,50))
    node_for_each = iggraph.create_node("For Each Loop", imgui.Vec2(600,100))
    node_draw_image = iggraph.create_node("Draw Image", imgui.Vec2(600,300))
    node_grid.inputs["number of horizontal cells"].value = 10
    node_grid.inputs["number of vertical cells"].value = 20
    node_load_image.inputs["url"].url = "c:\\tmp\\rainbow.jpg"
    iggraph.links.append(NodeLink(node_load_image.outputs["loaded image"], node_grid.inputs["source image"]))
    iggraph.links.append(NodeLink(node_grid.outputs["cells"], node_for_each.inputs["List to iterate"]))
    iggraph.links.append(NodeLink(node_load_image.outputs["loaded image"], node_for_each.inputs["Input1"]))
    iggraph.links.append(NodeLink(node_for_each.outputs["Element"], node_relative_coord.inputs["rectangle"]))
    iggraph.links.append(NodeLink(node_relative_coord.outputs["coords"], node_pixel_color.inputs["coords"]))
    iggraph.links.append(NodeLink(node_load_image.outputs["loaded image"], node_pixel_color.inputs["image"]))
    iggraph.links.append(NodeLink(node_pixel_color.outputs["pixel color"], node_colorize_image.inputs["white"]))
    iggraph.links.append(NodeLink(node_load_image2.outputs["loaded image"], node_colorize_image.inputs["source image"]))
    iggraph.links.append(NodeLink(node_for_each.outputs["Element"], node_draw_image.inputs["coordinates"]))
    iggraph.links.append(NodeLink(node_for_each.outputs["Output1"], node_draw_image.inputs["source image"]))
    iggraph.links.append(NodeLink(node_colorize_image.outputs["colorized image"], node_draw_image.inputs["image to past"]))
    iggraph.links.append(NodeLink(node_draw_image.outputs["composed image"], node_for_each.inputs["Input1"]))

def show_outputs_popup(iggraph):
    if imgui.begin_popup("Outputs", 0):
        output_nodes = iggraph.get_output_nodes()
        for output_node in output_nodes:
            value = output_node.outputs["output"]
            if imgui.tree_node(output_node.inputs["parameter name"].text):
                display_parameter(value,True)
                imgui.tree_pop()
        imgui.separator()
        if imgui.button("ok"):
            imgui.close_current_popup()
        imgui.end_popup()

def show_inputs_popup(iggraph):
    show_result = False
    if imgui.begin_popup("User Input", 0):
        input_nodes = iggraph.get_input_nodes()
        for input_node in input_nodes:
            default_value = input_node.inputs["default value"]
            if imgui.tree_node(input_node.inputs["parameter name"].text):
                display_parameter(default_value,True)
                imgui.tree_pop()
        imgui.separator()
        if imgui.button("run workflow"):
            imgui.close_current_popup()
            # iggraph.reset()
            iggraph.run()
            show_result = True
        imgui.same_line()
        if imgui.button("cancel"):
            iggraph.reset()
            iggraph.set_state(iggraph.STATE_IDLE)
            imgui.close_current_popup()
        imgui.end_popup()
    return show_result

def main():
    global width_library
    global width_shematic
    global width_context
    global height_window

    global previous_key_callback
    global selected_link
    global selected_node
    global iggraph
    global debug_is_mouse_dragging
    
    global show_debug_window

    # states -------------------------
    
    scrolling = imgui.Vec2(0, 0)

    iggraph = IGGraph()

    # iggraph.reset()

    node_hovered_in_scene = -1
    parameter_link_start = None
    selected_parameter = None

    io_hovered = None 
    io_anchors_width_not_hovered = 10
    io_anchors_width_hovered = 15 
    
    image_width = 0
    image_height = 0
    image_texture = None

    # states -------------------------

    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    io = imgui.get_io()
    previous_key_callback = glfw.set_key_callback(window,key_event)

    init_textures()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                clicked_load, selected_load = imgui.menu_item(
                    "Load", 'Cmd+L', False, True
                )
                if clicked_load:
                    root = tk.Tk()
                    root.withdraw()
                    filename = filedialog.askopenfilename()
                    if filename :
                        f=open(filename)
                        iggraph.from_json(json.load(f))
                        f.close()
                clicked_save, selected_save = imgui.menu_item(
                    "Save", 'Cmd+S', False, True
                )
                if clicked_save:
                    iggraph.reset()
                    graph_json = iggraph.to_json()
                    text2save = json.dumps(graph_json, indent=4, sort_keys=True)
                    root = tk.Tk()
                    root.withdraw()
                    f = filedialog.asksaveasfile(mode='w', defaultextension=".json")
                    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                        return
                    f.write(text2save)
                    f.close()
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )
                if clicked_quit:
                    exit(0)
                imgui.end_menu()
            if imgui.begin_menu("Debug", True):
                show_debug_window_clicked,  show_debug_window_selected = imgui.menu_item(
                    "Show Debug window", 'Cmd+D', show_debug_window, True
                )
                if show_debug_window_clicked:
                    show_debug_window = not show_debug_window
                catch_exceptions_clicked,  catch_exceptions_selected = imgui.menu_item(
                    "Catch Exceptions", '', iggraph.catch_exceptions, True
                )
                if catch_exceptions_clicked:
                    iggraph.catch_exceptions = not iggraph.catch_exceptions
                imgui.separator()
                imgui.menu_item(
                    "Examples", '', False, False
                )
                show_example_mosaic_clicked,  show_example_mosaic_selected = imgui.menu_item(
                    "Mosaic", '', False, True
                )
                if show_example_mosaic_clicked:
                    example_mosaic(iggraph)
                imgui.end_menu()
            imgui.end_main_menu_bar()

        height_window = io.display_size.y - imgui.get_cursor_pos_y()

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, imgui.Vec2(0,0))
        imgui.set_next_window_size(io.display_size.x, height_window)
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.begin("Splitter test", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS)
        imgui.pop_style_var()
        imgui.pop_style_var()

        width_shematic = io.display_size.x - separator_width  - width_context - separator_width - width_library

        # ==============================================================================
        # Library
        # ==============================================================================

        imgui.push_style_var(imgui.STYLE_CHILD_BORDERSIZE, 0)
        imgui.begin_child("Library", width_library, 0, True)
        for node_name in iggraph.node_library.nodes:
            if imgui.button(node_name):
                iggraph.create_node(node_name)
        imgui.end_child()
        imgui.pop_style_var()

        imgui.same_line()
        imgui.button("left_splitter", separator_width, height_window - 20)
        if (imgui.is_item_active()):
            width_library += io.mouse_delta.x
        
        imgui.same_line()

        # ==============================================================================
        # Shematic
        # ==============================================================================
        imgui.push_style_var(imgui.STYLE_CHILD_BORDERSIZE, 0)
        imgui.begin_child("shematic", width_shematic, 0, True)

        if show_inputs_popup(iggraph):
            imgui.open_popup("Outputs")
        show_outputs_popup(iggraph)

        # create our child canvas
        if iggraph.get_state() == iggraph.STATE_IDLE:
            imgui.text("status: edit | ")
        elif iggraph.get_state() == iggraph.STATE_RUNNING:
            imgui.text("status: run  | ")
        imgui.same_line()
        if iggraph.get_state() == iggraph.STATE_IDLE:
            if imgui.button("run"):
                #TODO if not running
                iggraph.set_state(iggraph.STATE_RUNNING)
                iggraph.prepare_to_run()
                imgui.open_popup("User Input")
            imgui.same_line()
            if imgui.button("run one step"):
                iggraph.set_state(iggraph.STATE_RUNNING)
                iggraph.prepare_to_run()
                iggraph.run_one_step()
        elif iggraph.get_state() == iggraph.STATE_RUNNING:
            if imgui.button("stop running"):
                iggraph.reset()
                iggraph.set_state(iggraph.STATE_IDLE)
            imgui.same_line()
            if imgui.button("run one step"):
                iggraph.set_state(iggraph.STATE_RUNNING)
                iggraph.run_one_step()
        # imgui.same_line(imgui.get_window_width() - 100)
        imgui.push_style_var(imgui.STYLE_FRAME_PADDING, imgui.Vec2(1, 1))
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, imgui.Vec2(0, 0))
        imgui.begin_child("scrolling_region", 0, 0, True, imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE)
        imgui.pop_style_var()
        imgui.pop_style_var()
        imgui.push_item_width(120.0)

        offset = add(imgui.get_cursor_screen_pos(), scrolling)
        draw_list = imgui.get_window_draw_list()

        # Display links
        draw_list.channels_split(2)
        draw_list.channels_set_current(0)
        for link in iggraph.links:
            draw_link_param_to_param(draw_list, offset, link.output_parameter, link.input_parameter, selected_link == link)

        # Display nodes
        parameter_link_end = None
        one_parameter_hovered = False
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
            imgui.invisible_button(str(node.id), node.size.x, node.size.y)
            if imgui.is_item_hovered():
                node_hovered_in_scene = node.id
            else:
                node_hovered_in_scene = None
            node_moving_active = imgui.is_item_active()
            use_hovered_color = node_hovered_in_scene or selected_node == node
            draw_list.add_rect_filled(node_rect_min.x, node_rect_min.y, node_rect_max.x, node_rect_max.y, get_node_color(node, iggraph, use_hovered_color), 5)
            if node_hovered_in_scene and iggraph.is_error(node):
                imgui.begin_tooltip()
                imgui.text(iggraph.error_nodes[node])
                imgui.end_tooltip()

            # input parameters
            for parameter_name in node.inputs:
                parameter = node.inputs[parameter_name]
                center = node.get_intput_slot_pos(parameter)
                center_with_offset = add(offset, center)
                if io_hovered == parameter:
                    io_anchors_width = io_anchors_width_hovered
                else:
                    io_anchors_width = io_anchors_width_not_hovered
                imgui.set_cursor_pos(imgui.Vec2(center.x-io_anchors_width/2, center.y-io_anchors_width/2))
                imgui.push_id(str(str(node.id) + "input" + parameter.id))
                if (imgui.invisible_button("input", io_anchors_width, io_anchors_width)):
                    selected_parameter = parameter
                # imgui.is_item_hovered() does not work when dragging
                is_hovering = ((io.mouse_pos.x-offset.x>center.x-io_anchors_width/2) and 
                               (io.mouse_pos.x-offset.x<center.x+io_anchors_width/2) and
                               (io.mouse_pos.y-offset.y>center.y-io_anchors_width/2) and
                               (io.mouse_pos.y-offset.y<center.y+io_anchors_width/2))
                if is_hovering:
                    io_hovered = parameter
                    one_parameter_hovered = True
                    imgui.begin_tooltip()
                    imgui.text(parameter_name)
                    imgui.end_tooltip()
                if is_hovering and imgui.is_mouse_released(0):
                    parameter_link_end = parameter
                imgui.pop_id()
                draw_list.add_circle_filled(center_with_offset.x, center_with_offset.y, io_anchors_width/2, get_parameter_color(parameter))

            # output parameters
            for parameter_name in node.outputs:
                parameter = node.outputs[parameter_name]
                center = node.get_output_slot_pos(parameter)
                center_with_offset = add(offset, center)
                if io_hovered == parameter:
                    io_anchors_width = io_anchors_width_hovered
                else:
                    io_anchors_width = io_anchors_width_not_hovered
                imgui.set_cursor_pos(imgui.Vec2(center.x-io_anchors_width/2, center.y-io_anchors_width/2))
                imgui.push_id(str(str(node.id) + "output" + parameter.id))
                if (imgui.invisible_button("output", io_anchors_width, io_anchors_width)):
                    selected_parameter = parameter
                if imgui.is_item_hovered():
                    io_hovered = parameter
                    one_parameter_hovered = True
                    imgui.begin_tooltip()
                    imgui.text(parameter_name)
                    imgui.end_tooltip()
                draw_list.add_circle_filled(center_with_offset.x, center_with_offset.y, io_anchors_width/2, get_parameter_color(parameter))
                imgui.pop_id()
                if imgui.is_item_active():
                    parameter_link_start = parameter

            if node_widgets_active or node_moving_active:
                selected_node = node
            if (node_moving_active and imgui.is_mouse_dragging(0) and node.id==selected_node.id):
               node.pos = add(node.pos, io.mouse_delta)

            imgui.pop_id()
        draw_list.channels_merge()
        if not one_parameter_hovered:
            io_hovered = None


        debug_is_mouse_dragging = imgui.is_mouse_dragging(0)
        if parameter_link_start and parameter_link_end:
            iggraph.add_link(parameter_link_start, parameter_link_end)
        elif parameter_link_start and imgui.is_mouse_dragging(0):
            draw_link_param_to_point(draw_list, offset, parameter_link_start, io.mouse_pos.x, io.mouse_pos.y, True)
        if imgui.is_mouse_released(0):
            parameter_link_start = None

        imgui.pop_item_width()
        imgui.end_child()

        # mouse click on the scene
        if imgui.is_mouse_clicked(0):
            mouse_pos = imgui.get_mouse_pos()
            local_mouse_pos = imgui.Vec2(mouse_pos.x - offset.x, mouse_pos.y - offset.y)
            selected_link = None
            for link in iggraph.links:
                start_node = link.output_parameter.owner
                start_pos = start_node.get_output_slot_pos(link.output_parameter)
                end_node = link.input_parameter.owner
                end_pos = end_node.get_intput_slot_pos(link.input_parameter)
                distance_mouse_start = math.sqrt(((local_mouse_pos.x-start_pos.x)**2) + ((local_mouse_pos.y-start_pos.y)**2))
                distance_mouse_end = math.sqrt(((local_mouse_pos.x-end_pos.x)**2) + ((local_mouse_pos.y-end_pos.y)**2))
                distance_start_end = math.sqrt(((start_pos.x-end_pos.x)**2) + ((start_pos.y-end_pos.y)**2))
                if ((distance_mouse_start + distance_mouse_end) - distance_start_end) < 0.1:
                    selected_link = link
                
        imgui.end_child()
        imgui.pop_style_var()

        imgui.same_line()
        imgui.button("right_splitter", separator_width, height_window - 20)
        if (imgui.is_item_active()):
            width_context -= io.mouse_delta.x
        
        # ==============================================================================
        # Context
        # ==============================================================================

        imgui.same_line()
        imgui.push_style_var(imgui.STYLE_CHILD_BORDERSIZE, 0)
        imgui.begin_child("child3", width_context, 0, True);
        if selected_node:
            if imgui.tree_node("Inputs"):
                for parameter_name in selected_node.inputs:
                    parameter = selected_node.inputs[parameter_name]
                    if imgui.tree_node(parameter.id):
                        display_parameter(parameter, True)
                        imgui.tree_pop()
                imgui.tree_pop()
            if imgui.tree_node("Output"):
                for parameter_name in selected_node.outputs:
                    parameter = selected_node.outputs[parameter_name]
                    if imgui.tree_node(parameter.id):
                        display_parameter(parameter, False)
                        imgui.tree_pop()
                imgui.tree_pop()
        imgui.end_child()
        imgui.pop_style_var()

        # 
        imgui.end()

        #------------------------------------------------------------
        if show_debug_window:
            debug_window_expanded, show_debug_window = imgui.begin("Debug", True)
            if parameter_link_start:
                imgui.text("parameter_link_start: " + parameter_link_start.id)
            else:
                imgui.text("parameter_link_start: " + "None")
            if selected_parameter:
                imgui.text("selected_parameter: " + selected_parameter.id)
            else:
                imgui.text("selected_parameter: " + "None")
            imgui.text("is_mouse_dragging: " + str(debug_is_mouse_dragging))
            imgui.text("mouse.x: " + str(io.mouse_pos.x))
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