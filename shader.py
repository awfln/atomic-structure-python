from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *

def create_shader(vertex_filepath, fragment_filepath):
    vertex_file = open(vertex_filepath,'r')
    fragment_file = open(fragment_filepath,'r')
    vertex_src = vertex_file.readlines()
    fragment_src = fragment_file.readlines()
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),compileShader(fragment_src, GL_FRAGMENT_SHADER))
    
    vertex_file.close()
    fragment_file.close()

    return shader