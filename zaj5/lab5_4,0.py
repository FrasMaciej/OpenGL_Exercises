import sys
from math import *

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0
piy2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0
R = 5.0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 10.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

selectedKey = 1


def startup():
    update_viewport(None, 1000, 1000)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def shutdown():
    pass


def render(time):
    global theta, phi
    global pix2angle, piy2angle
    global light_position
    global R


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * piy2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    _theta = 2*pi*theta/360
    _phi = 2*pi*phi/360

    xs = R * cos(_theta) * cos(_phi)
    ys = R * sin(_phi)
    zs = R * sin(_theta) * cos(_phi)
    glTranslate(xs, ys, zs)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    light_position[0] = xs
    light_position[1] = ys
    light_position[2] = zs
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

def keyboard_key_callback(window, key, scancode, action, mods):
    global light_ambient, mat_diffuse, mat_specular, selectedKey
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        selectedKey = 1
    elif key == GLFW_KEY_2 and action == GLFW_PRESS:
        selectedKey = 2
    elif key == GLFW_KEY_3 and action == GLFW_PRESS:
        selectedKey = 3
    elif key == GLFW_KEY_4 and action == GLFW_PRESS:
        selectedKey = 4

    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        if selectedKey == 1 and light_ambient[0] <= 0.9:
            light_ambient[0] = light_ambient[0] + 0.1
        elif selectedKey == 2 and light_ambient[1] <= 0.9:
            light_ambient[1] = light_ambient[1] + 0.1
        elif selectedKey == 3 and light_ambient[2] <= 0.9:
            light_ambient[2] = light_ambient[2] + 0.1
        elif selectedKey == 4 and light_ambient[3] <= 0.9:
            light_ambient[3] = light_ambient[3] + 0.1
        print(light_ambient)
    elif key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        if selectedKey == 1 and light_ambient[0] >= 0.1:
            light_ambient[0] = light_ambient[0] - 0.1
        elif selectedKey == 2 and light_ambient[1] >= 0.1:
            light_ambient[1] = light_ambient[1] - 0.1
        elif selectedKey == 3 and light_ambient[2] >= 0.1:
            light_ambient[2] = light_ambient[2] - 0.1
        elif selectedKey == 4 and light_ambient[3] >= 0.1:
            light_ambient[3] = light_ambient[3] - 0.1
        print(light_ambient)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(1000, 1000, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()