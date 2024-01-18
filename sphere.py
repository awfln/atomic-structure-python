import numpy as np

class Sphere:
    def __init__(self, position, eulers, mesh):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
        self.mesh = mesh