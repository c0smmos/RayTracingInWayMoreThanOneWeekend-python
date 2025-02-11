from vector import*
from abc import ABC, abstractmethod

class Hit_record:
    def __init__(self, t = 0.0, p = Vector3(0.0, 0.0, 0.0,), normal = Vector3(0.0, 0.0, 0.0), front_face = False):
        self.t = t
        self.p = p
        self.normal = normal
        self.front_face = front_face

    def set_face_normal(self, r, outward_normal):
        """
        Sets the hit record normal vector.
        NOTE: the parameter `outward_normal` is assumed to have unit length.
        """
        self.front_face = dot(r.direction, outward_normal)
        if self.front_face < 0.0:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal
        

class Hittable:
    @abstractmethod
    def hit(self, t_min, t_max_hit_record):
        pass
        