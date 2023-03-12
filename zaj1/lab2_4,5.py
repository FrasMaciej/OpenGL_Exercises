#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

class P:
    x=0.0
    y=0.0

def startup():
    update_viewport(None, 1000, 1600)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def printSierpCurpet(A, B, C, D, iteration):
    if(iteration == 0): return 0
    iteration-=1
    # Zewnętrzny kwadrat
    glColor3f(0.5,0.25,0.25)
    glBegin(GL_QUADS)
    glVertex2f(A.x, A.y)
    glVertex2f(B.x, B.y)
    glVertex2f(C.x, C.y)
    glVertex2f(D.x, D.y)
    glEnd()

    # Wewnętrzny kwadrat
    glColor3f(1.0,1.0,1.0)
    glBegin(GL_QUADS)
    glVertex2f(A.x+1/3*(D.x-A.x), A.y+1/3*(B.y-A.y))
    glVertex2f(A.x+1/3*(D.x-A.x), A.y+2/3*(B.y-A.y))
    glVertex2f(A.x+2/3*(D.x-A.x), A.y+2/3*(B.y-A.y))
    glVertex2f(A.x+2/3*(D.x-A.x), A.y+1/3*(B.y-A.y))
    glEnd()

    glColor3f(0.0,0.0,0.0)
    # glBegin(GL_LINES)

    # rysowanie małych prostokątów (konturów)
    for j in [1/3,2/3,3/3]:
        for i in [1/3,2/3,3/3]:
            glBegin(GL_LINES)
            glVertex2f(A.x+(i-1/3)*(D.x-A.x), A.y+((3/3-j)*(B.y-A.y)))
            glVertex2f(A.x+(i-1/3)*(D.x-A.x), A.y+((4/3-j))*(B.y-A.y))
            glVertex2f(A.x+(i-1/3)*(D.x-A.x), A.y+((4/3-j))*(B.y-A.y))
            glVertex2f(A.x+(i*(D.x-A.x)), A.y+((4/3-j))*(B.y-A.y))
            glVertex2f(A.x+(i*(D.x-A.x)), A.y+((4/3-j))*(B.y-A.y))
            glVertex2f(A.x+(i*(D.x-A.x)), A.y+((3/3-j)*(B.y-A.y)))
            glVertex2f(A.x+(i*(D.x-A.x)), A.y+((3/3-j)*(B.y-A.y)))
            glVertex2f(A.x+(i-1/3)*(D.x-A.x), A.y+((3/3-j)*(B.y-A.y)))
            glEnd()
            if(not(j==2/3 and i==2/3)):
                a = P()
                a.x = A.x+(i-1/3)*(D.x-A.x)
                a.y = A.y+((3/3-j)*(B.y-A.y))

                b = P()
                b.x = A.x+(i-1/3)*(D.x-A.x)
                b.y = A.y+((4/3-j))*(B.y-A.y)

                c = P()
                c.x = A.x+(i*(D.x-A.x))
                c.y = A.y+((4/3-j))*(B.y-A.y)

                d = P()
                d.x = A.x+(i*(D.x-A.x))
                d.y = A.y+((3/3-j)*(B.y-A.y))
                printSierpCurpet(a, b, c, d, iteration)

def render(a, b, degree):
    glClear(GL_COLOR_BUFFER_BIT)

    X = a/2
    Y = b/2

    A = P()
    A.x = -X
    A.y = -Y

    B = P()
    B.x = -X
    B.y = Y

    C = P()
    C.x = X
    C.y = Y

    D = P()
    D.x = X
    D.y = -Y

    printSierpCurpet(A, B, C, D, degree)

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

    window = glfwCreateWindow(1000, 1600, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(300, 150, 4)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
