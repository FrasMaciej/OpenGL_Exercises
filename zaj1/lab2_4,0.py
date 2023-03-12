#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 1920, 1080)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(x, y, a, b, d=0.0, ):
    glClear(GL_COLOR_BUFFER_BIT)
    R=random.random()
    G=random.random()
    B=random.random()
    glColor3f(R, G, B)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, d*a)
    glVertex2f(d*b, y)
    glEnd()
    glBegin(GL_TRIANGLES)
    glVertex2f(x, d*a)
    glVertex2f(d*b, y)
    glVertex2f(d*b, d*a)

    glEnd()

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(1920, 1080, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(-10.0, -10.0, 20.0, 25.0, 1.0)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
