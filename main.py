import pygame
from OpenGL.GL import *
import numpy as np
import ctypes
import os
import pyrr

from shader import *
from mesh import *
from sphere import *
from model_transform import *
from rotate import *

pygame.init()
pygame.display.set_mode((0,0), pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN)
pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, 1)
clock = pygame.time.Clock()
glEnable(GL_DEPTH_TEST)
glClearColor(0,0,0,1)  #rgba

shader = create_shader(vertex_filepath = "shaders/vertex.txt", fragment_filepath = "shaders/fragment.txt")
glUseProgram(shader)

offset = [0,0,-8]
mouse_sensitivity = 0.1

nucleons = [
Sphere(
    position = [-0.25,0,0-8],
    eulers = [0,0,0],
    mesh = Mesh("proton.obj")
),
Sphere(
    position = [0.25,0,0-8],
    eulers = [0,0,0],
    mesh = Mesh("neutron.obj")
),
Sphere(
    position = [0,0.4330127018922193,0-8],
    eulers = [0,0,0],
    mesh = Mesh("neutron.obj")
),
Sphere(
    position = [0, 0.2165063509461097, 0.433012701892219-8],
    eulers = [0,0,0],
    mesh = Mesh("proton.obj")
)
]

projection_transform = pyrr.matrix44.create_perspective_projection(
    fovy = 45, aspect = pygame.display.Info().current_w/pygame.display.Info().current_h,
    near = 0.1, far = 20, dtype = np.float32
)

glUniformMatrix4fv(
    glGetUniformLocation(shader, "projection"),
    1, GL_FALSE, projection_transform
)
modelMatrixLocation = glGetUniformLocation(shader, "model")

delta_theta = np.pi / 256 #radians

running = True
while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        if event.type == pygame.MOUSEWHEEL:
            offset[2] += mouse_sensitivity*event.y

    #logic
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader) # you may remove this ##############################################################################

    for nucleon in nucleons:
        new_positions = rotate_about_origin(nucleon.position[0],nucleon.position[2],delta_theta, offset[2])
        nucleon.position[0] = new_positions[0]
        nucleon.position[2] = new_positions[1]

    for nucleon in nucleons:
        glUniformMatrix4fv(modelMatrixLocation, 1, GL_FALSE, create_model_transform(nucleon, offset))
        nucleon.mesh.draw()
    
    pygame.display.flip()
    clock.tick(60)  

for nucleon in nucleons:
    nucleon.mesh.destroy()
glDeleteProgram(shader)
