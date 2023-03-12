#!/usr/bin/env python3
from cmath import cos, pi, sin
import math
import sys
import numpy

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
    glRotatef(angle, 0.0, 1.0, 0.0)
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

def printEgg(tab):
    glColor3f(0.8, 0.7, 0.2)
    for i in range(len(tab)):
        for j in range(len(tab[i])-1):
            glBegin(GL_POINTS)
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glVertex3f(tab[i][j+1][0], tab[i][j+1][1], tab[i][j+1][2])
            glEnd()


def render(tab, time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / 3.1415)
    axes()
    printEgg(tab)
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
    n = 50
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(1920, 1080, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    tab = countEggVertices(n)
    print(tab)
    
    startup()
    while not glfwWindowShouldClose(window):
        render(tab, glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()