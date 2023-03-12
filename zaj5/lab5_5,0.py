from cmath import cos, pi, sin
import math
import sys
import numpy
import random
from math import *
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

n = 30
theta = 0.0
phi = 0.0
pix2angle = 1.0
piy2angle = 1.0

left_mouse_button_pressed = 0
linesAreVisible = 1
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
    update_viewport(None, 1920, 1080)
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


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 1.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def countX(u, v):
    return (((-90*pow(u,5))+(225*pow(u,4))-(270*pow(u,3))+(180*pow(u,2))-(45*u))* math.cos(pi*v))

def countY(u, v):
    return ((160*pow(u,4))-(320*pow(u,3))+(160*pow(u,2))-5)

def countZ(u, v):
    return (((-90*pow(u,5))+(225*pow(u,4))-(270*pow(u,3))+(180*pow(u,2))-(45*u))*math.sin(pi*v))

def countNormalVectors():
    global n
    normalVectorsTab = numpy.zeros((n, n, 3))

    for i in range (0, n):
        for j in range (0, n):
            u = i/n
            v = j/n
            
            # pochodne cząstkowe
            xu = (-450*pow(u,4)+900*pow(u,3)-810*pow(u,2)+360*u-45)*cos(pi*v)
            xv = pi*(90*pow(u,5)-225*pow(u,4)+270*pow(u,3)-180*pow(u,2)+45*u)*sin(pi*v)
            yu = 640*pow(u,3)-960*pow(u,2)+320*u
            yv = 0
            zu = (-450*pow(u,4)+900*pow(u,3)-810*pow(u,2)+360*u-45)*sin(pi*v)
            zv = (-pi)*(90*pow(u,5)-225*pow(u,4)+270*pow(u,3)-180*pow(u,2)+45*u)*cos(pi*v)

            # wyznaczenie wektorów normalnych
            x = yu * zv - zu * yv
            y = zu * xv - xu * zv
            z = xu * yv - yu * xv
            
            # pitagoras
            vectorLength = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))
 
            # dzielenie współrzędnych przez wartość
            if vectorLength > 0:
                x = x / vectorLength
                y = y / vectorLength
                z = z / vectorLength    

            # odwrócenie wektorów na drugiej połówce modelu
            if i > n / 2:
                x *= -1
                y *= -1
                z *= -1       
            
            normalVectorsTab[i][j][0] =  x
            normalVectorsTab[i][j][1] =  y
            normalVectorsTab[i][j][2] =  z
            
    return normalVectorsTab


def countEggVertices(N):
    tab = numpy.zeros((N, N, 3))
    for i in range(0, N):
        for j in range(0, N):
            u=i/(N-1)
            v=j/(N-1)
            tab[i][j][0]=countX(u, v)
            tab[i][j][1]=countY(u, v)
            tab[i][j][2]=countZ(u, v)
    return tab

def randomizeColours(tab):
    for i in range(0, len(tab)):
        for j in range(0, len(tab[i])):
            tab[i][j][0]=random.random()
            tab[i][j][1]=random.random()
            tab[i][j][2]=random.random()
    return tab

def printEgg(tab, normalVectorsTab, colours):
    global R
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(len(tab)-1):
        for j in range(len(tab[i])):

            # glColor3f(colours[i][j][0], colours[i][j][1], colours[i][j][2])
            glNormal3f(normalVectorsTab[i][j][0], normalVectorsTab[i][j][1], normalVectorsTab[i][j][2])
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            # glColor3f(colours[i+1][j][0], colours[i+1][j][1], colours[i+1][j][2])
            glNormal3f(normalVectorsTab[i+1][j][0], normalVectorsTab[i+1][j][1], normalVectorsTab[i+1][j][2])
            glVertex3f(tab[i+1][j][0], tab[i+1][j][1], tab[i+1][j][2])
    glEnd()

def printNormalVectors(tab, normalVectorsTab):
    for i in range (0, n):
        for j in range (0, n):
            glBegin(GL_LINES)
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glVertex3f(tab[i][j][0] + normalVectorsTab[i][j][0], tab[i][j][1] + normalVectorsTab[i][j][1], tab[i][j][2] + normalVectorsTab[i][j][2])
            glEnd()   

def render(tab, normalVectorsTab, colours, time):
    global theta, phi
    global pix2angle, piy2angle
    global light_position
    global R

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * piy2angle


    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    printEgg(tab, normalVectorsTab, colours)

    if linesAreVisible:
        printNormalVectors(tab, normalVectorsTab)

    # spin(time * 60 / 3.1415)
    # axes()
    glFlush()



def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

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
    global linesAreVisible
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_Q and action == GLFW_PRESS:
        if linesAreVisible == 1:
            linesAreVisible = 0
        else: 
            linesAreVisible = 1

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

def main():
    global n

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(1920, 1080, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    colours = randomizeColours(numpy.zeros((n, n, 3)))
    tab = countEggVertices(n)
    normalVectorsTab = countNormalVectors()

    startup()
    while not glfwWindowShouldClose(window):
        render(tab, normalVectorsTab, colours, glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()