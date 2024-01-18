import pyrr
import numpy as np

def create_model_transform(mesh, offset):
    model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
    model_transform = pyrr.matrix44.multiply(
        m1=model_transform,
        m2=pyrr.matrix44.create_from_eulers(
            eulers=np.radians(mesh.eulers),
            dtype=np.float32
        )
    )
    model_transform = pyrr.matrix44.multiply(
        m1=model_transform,
        m2=pyrr.matrix44.create_from_translation(
            vec=mesh.position,
            dtype=np.float32
        )
    )
    #model_transform = pyrr.matrix44.multiply(
    #    m1=model_transform,
    #    m2=pyrr.matrix44.create_from_translation(
    #        vec=offset,
    #        dtype=np.float32
    #    )
    #)
    return model_transform