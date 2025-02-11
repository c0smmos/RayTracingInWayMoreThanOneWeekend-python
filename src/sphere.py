from hittable import Hittable
from vector import*
from ray import Ray

class Sphere (Hittable):
    def __init__(self, center, radius,):
        self.center = center
        self.radius = radius


    def hit(self, r, t_min, t_max, hit_record):
        oc = self.center - r.origin
        a = dot(r.direction, r.direction)
        h = dot(r.direction, oc)
        c = dot(oc, oc) - self.radius*self.radius
        discriminant = h*h - a*c
        if discriminant < 0.0:
            False

        sqrtd = math.sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        root = (h - sqrtd) / a
        if t_min >= root >= t_max:
            root = (h + sqrtd) / a
            if t_min >= root >= t_max:
                return False
        
        hit_record.t = root
        hit_record.p = r.point_at_t(hit_record.t)
        hit_record.normal = (hit_record.p - self.center) / self.radius

        return True
