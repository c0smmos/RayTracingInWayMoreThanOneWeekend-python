from vector import Vector3
from hittable_L19 import*
from ray import*

import os
import sys
import random



class Camera():
    def __init__(self,aspect_ratio = 1.0, image_width = 100, samples_per_pixel = 10):
        self.aspect_ratio = aspect_ratio            
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel
        self.pixel_samples_scale = None
        self.image_height = None 
        self.camera_center = None
        self.pixel_00_loc = None  
        self.pixel_delta_u = None
        self.pixel_delta_v = None


    def initialize(self):
        self.image_height = max(int(self.image_width / self.aspect_ratio), 1)
        self.pixel_samples_scale = 1.0 / self.samples_per_pixel
         
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
    

    def sample_square(self):
            # Return a random point in the [-0.5, -0.5] to [+0.5, +0.5] unit square
            return Vector3(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), 0)


    def get_ray(self, i, j):
            # Construct a camera ray originating from the camera center
            offset = self.sample_square()
            pixel_sample = (self.pixel_00_loc + (self.pixel_delta_u * (i + offset.x)) + (self.pixel_delta_v) *(j + offset.y))

            ray_origin = self.camera_center
            ray_direction = pixel_sample - ray_origin

            return Ray(ray_origin, ray_direction)
    

    def ray_colour(self, r, world):
        hit_record = Hit_record()
        if world.hit(r, 0.0, sys.float_info.max, hit_record):
            return (hit_record.normal + Vector3(1.0, 1.0, 1.0)) / 2


        unit_direction = unit_vector(r.direction)
        # Graphics trick of scaling it to 0.0 < y < 1.0
        a = 0.5*(unit_direction.y + 1.0)
        # Lerping between (255, 255, 255) which is white to a light shade blue (128, 255*0.7, 255)
        return Vector3(1.0, 1.0, 1.0) * (1.0 - a) + Vector3(0.5, 0.7, 1.0) * a
        
    def clamp(x, min_val, max_val):
        if x < min_val:
            return min_val
        elif x > max_val:
            return max_val
        return x
    

    def render(self, world):
        self.initialize()

        path = os.path.join(os.path.dirname(__file__),"..","images", "Test.ppm")
        ppm_file = open(path, 'w')
        title = "P3\n{iw} {ih}\n 255\n".format(iw = self.image_width, ih = self.image_height)
        ppm_file.write(title)


        for j in range(self.image_height):
            print(f"\rScanlines remaining: {self.image_height - j} ", end='', flush=True)
            for i in range(self.image_width):
                pixel_colour = Vector3(0.0, 0.0, 0.0)
                for sample in range(self.samples_per_pixel):
                    ray = self.get_ray(i, j)
                    pixel_colour += self.ray_colour(ray, world)

                # Scale pixel color by the sample factor
                
                scaled_color = pixel_colour * self.pixel_samples_scale
    
                ir = int(255.99*scaled_color.r)
                ig = int(255.99*scaled_color.g)
                ib = int(255.99*scaled_color.b)
                value = (f"{ir} {ig} {ib}\n")
                ppm_file.write(value)
        print("\rDone.                 ", end="", flush=True)
        ppm_file.close()

