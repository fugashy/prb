import numpy as np



class RigidBody():
    def __init__(
            self,
            init_pos,
            pos_std,
            angle_deg,
            size,
            size_std):
        self.pos = np.array(init_pos)
        self.pos_std = np.array(pos_std)
        self.angle = np.deg2rad(angle_deg)
        self.size = np.array(size)
        self.size_std = np.array(size_std)

    def __str__(self):
        return f"""pos: {self.pos}
pos std: {self.pos_std}
angle: {self.angle}
size: {self.size}
size std: {self.size_std}
"""

    def __rstr__(self):
        return self.__str__(self)
