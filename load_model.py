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