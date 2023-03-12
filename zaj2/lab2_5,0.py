#!/usr/bin/env python3
from cmath import cos, pi, sin
import math
import sys
import numpy
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 1920, 1080)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


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

# 1000x1000px
def countCoords(tab):
    for y in range(0, len(tab)):
        for x in range(0, len(tab[y])):
            tab[x][y][0]=(x/len(tab))*1000
            tab[x][y][1]=(y/len(tab))*1000
    return tab

def randomizeColours(tab):
    for y in range(0, len(tab)):
        for x in range(0, len(tab[y])):
            tab[y][x][0]=random.random()
            tab[y][x][1]=random.random()
            tab[y][x][2]=random.random()
    return tab

def printPlasma(tab, colours):
    glColor(1, 1, 1)
    for y in range(0, len(tab)-1):
        for x in range(0, len(tab[y])-1):
            glBegin(GL_LINES)
            glVertex2d(tab[x][y][0], tab[x][y][1])
            glVertex2d(tab[x][y+1][0], tab[x][y+1][1])
            glVertex2d(tab[x+1][y+1][0], tab[x+1][y+1][1])
            glVertex2d(tab[x+1][y][0], tab[x+1][y][1])
            glVertex2d(tab[x][y][0], tab[x][y][1])
            glEnd()

def render(tab, colours, time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 60 / 3.1415)
    axes()
    printPlasma(tab, colours)
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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    n = 16

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(1920, 1080, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    colours = randomizeColours(numpy.zeros((n, n, 3)))
    tab = countCoords(numpy.zeros((n, n, 2)))
    print(tab)
    
    startup()
    while not glfwWindowShouldClose(window):
        render(tab, colours, glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()