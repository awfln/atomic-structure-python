from OpenGL.GL import *
from load_model import *
import numpy as np
import pywavefront

class Mesh:
    def __init__(self, filepath):
        mesh = pywavefront.Wavefront(filepath, collect_faces=True)
        
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

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.indices_count, GL_UNSIGNED_INT, None)
    
    def destroy(self):
        glDeleteVertexArrays(1,(self.vao,))
        glDeleteBuffers(1,(self.vbo_vertices,))
        glDeleteBuffers(1,(self.vbo_indices,))