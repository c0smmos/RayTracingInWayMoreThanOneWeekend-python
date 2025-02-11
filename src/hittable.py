from vector import Vector3
from abc import ABC, abstractmethod

class Hit_record:
    def __init__(self, t = 0.0, p = Vector3(0.0, 0.0, 0.0,), normal = Vector3(0.0, 0.0, 0.0)):
        self.t = t
        self.p = p
        self.normal = normal

class Hittable:
    @abstractmethod
    def hit(self, t_min, t_max_hit_record):
        pass
        