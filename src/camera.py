from vector import Vector3
from hittable_L19 import*
from ray import*
import os
import sys

class Camera():
    def __init__(self,aspect_ratio = 1.0, image_width = 100):
        self.aspect_ratio = aspect_ratio            
        self.image_width = image_width              
        self.image_height = None 
        self.camera_center = None
        self.pixel00_loc = None  
        self.pixel_delta_u = None
        self.pixel_delta_v = None


    def initialize(self):
        self.image_height = max(int(self.image_width / self.aspect_ratio), 1)
         
        # Determine viewport dimensions
        focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * (self.image_width / self.image_height)
        self.camera_center = Vector3(0.0, 0.0, 0.0)

        # Calculate the vectors across the horizontal and down the vertical viewport edges
        viewport_u = Vector3(viewport_width, 0.0, 0.0)                             # x, y, z (right handed)
        viewport_v = Vector3(0.0, -viewport_height, 0.0)

        # Calculate the horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate the location of the upper left pixel
        viewport_upper_left = self.camera_center - Vector3(0.0, 0.0, focal_length) - (viewport_u/2) - (viewport_v/2)
        self.pixel_00_loc = viewport_upper_left +  (self.pixel_delta_u + self.pixel_delta_v)/2


    def ray_colour(self, r, world):
        hit_record = Hit_record()
        if world.hit(r, 0.0, sys.float_info.max, hit_record):
            return (hit_record.normal + Vector3(1.0, 1.0, 1.0)) / 2


        unit_direction = unit_vector(r.direction)
        # Graphics trick of scaling it to 0.0 < y < 1.0
        a = 0.5*(unit_direction.y + 1.0)
        # Lerping between (255, 255, 255) which is white to a light shade blue (128, 255*0.7, 255)
        return Vector3(1.0, 1.0, 1.0) * (1.0 - a) + Vector3(0.5, 0.7, 1.0) * a
        

    def render(self, world):
        self.initialize()

        path = os.path.join(os.path.dirname(__file__),"..","images", "Test.ppm")
        ppm_file = open(path, 'w')
        title = "P3\n{iw} {ih}\n 255\n".format(iw = self.image_width, ih = self.image_height)
        ppm_file.write(title)


        for j in range(self.image_height):
            print(f"\rScanlines remaining: {self.image_height - j} ", end='', flush=True)
            for i in range(self.image_width):
                pixel_center = self.pixel_00_loc + (self.pixel_delta_u * i) + (self.pixel_delta_v * j)
                ray_direction = pixel_center - self.camera_center
                r = Ray(self.camera_center, ray_direction)

                pixel_colour = self.ray_colour(r, world)

                
                ir = int(255.99*pixel_colour.r)
                ig = int(255.99*pixel_colour.g)
                ib = int(255.99*pixel_colour.b)
                value = (f"{ir} {ig} {ib}\n")
                ppm_file.write(value)
        print("\rDone.                 ", end="", flush=True)
        ppm_file.close()

