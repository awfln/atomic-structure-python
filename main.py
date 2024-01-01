import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import ctypes
import os
import pyrr
import pywavefront

def create_shader(vertex_filepath, fragment_filepath) -> int:
    vertex_file = open(vertex_filepath,'r')
    fragment_file = open(fragment_filepath,'r')
    vertex_src = vertex_file.readlines()
    fragment_src = fragment_file.readlines()
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),compileShader(fragment_src, GL_FRAGMENT_SHADER))
    
    vertex_file.close()
    fragment_file.close()

    return shader

def loadVertices(mesh):
    vertices = []
    for vertex in mesh.vertices:
        vertices.extend(vertex)
    return vertices

def loadIndices(mesh):
    indices = []
    for mesh_in in mesh.mesh_list:
        for face in mesh_in.faces:
            indices.extend(face)
    return indices

class Cube:
    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

class Mesh:
    def __init__(self):
        mesh = pywavefront.Wavefront("sphere.obj", collect_faces=True)
        
        #x,y,z,r,g,b (for every vertex)
        vertices = loadVertices(mesh)
        vertices = np.array(vertices, dtype=np.float32)

        indices = loadIndices(mesh)
        indices = np.array(indices, dtype=np.uint32)

        self.vertex_count = len(vertices) // 6
        self.indices_count = len(indices)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        self.vbo_vertices = glGenBuffers(1) 
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_vertices) 
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        self.vbo_indices = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo_indices) 
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    
    def arm_for_drawing(self):
        glBindVertexArray(self.vao)

    def draw(self):
        glDrawElements(GL_TRIANGLES, self.indices_count, GL_UNSIGNED_INT, None)
    
    def destroy(self):
        glDeleteVertexArrays(1,(self.vao,))
        glDeleteBuffers(1,(self.vbo_vertices,))
        glDeleteBuffers(1,(self.vbo_indices,))


pygame.init()
pygame.display.set_mode((0,0), pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN)
clock = pygame.time.Clock()
glEnable(GL_DEPTH_TEST)
glClearColor(0,0,0,1) #rgba

shader = create_shader(vertex_filepath = "shaders/vertex.txt",
                    fragment_filepath = "shaders/fragment.txt")
glUseProgram(shader)

my_cube = Cube(
    position = [0,0,-8],
    eulers = [0,0,0]
)

my_cube_mesh = Mesh()

projection_transform = pyrr.matrix44.create_perspective_projection(
    fovy = 45, aspect = 1366/768, #EEEEEEEEEEEEEEE
    near = 0.1, far = 10, dtype = np.float32
)

glUniformMatrix4fv(
    glGetUniformLocation(shader, "projection"),
    1, GL_FALSE, projection_transform
)
modelMatrixLocation = glGetUniformLocation(shader, "model")


running = True
while(running):
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False

    #logic
    my_cube.eulers[2] += 0.7
    if(my_cube.eulers[2] > 360):
        my_cube.eulers[2] = 0


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    #do things here
    glUseProgram(shader) # may remove

    model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
    model_transform = pyrr.matrix44.multiply(
        m1=model_transform,
        m2=pyrr.matrix44.create_from_eulers(
            eulers=np.radians(my_cube.eulers),
            dtype=np.float32
        )
    )
    model_transform = pyrr.matrix44.multiply(
        m1=model_transform,
        m2=pyrr.matrix44.create_from_translation(
            vec=my_cube.position,
            dtype=np.float32
        )
    )
    glUniformMatrix4fv(modelMatrixLocation, 1, GL_FALSE, model_transform)

    my_cube_mesh.arm_for_drawing()
    my_cube_mesh.draw()
    
    pygame.display.flip()

    clock.tick(60)  

my_cube_mesh.destroy()
glDeleteProgram(shader)
