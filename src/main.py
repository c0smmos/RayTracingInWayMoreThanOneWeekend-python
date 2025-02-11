from vector import*

from ray import Ray

import sys

def ray_colour(r):
    return Vector3(0, 0, 0)

def main():
    # image
    aspect_ratio = 16/9
    image_width = 400

    # Calculate the image height, and ensure that it's at least 1.
    image_height = int(image_width / aspect_ratio)
    image_height = max(image_height, 1)                              # if image_height < 1, then 1
    
    # Camera
    focal_lenght = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (image_width / image_height)
    camera_center = Vector3(0.0, 0.0, 0.0)

    # Calculate the vectors across the horizontal and down the vertical viewport edges.
    viewport_u = Vector3(viewport_width, 0.0, 0.0)                             # x, y, z (right handed)
    viewport_v = Vector3(0.0, -viewport_height, 0.0)

    # Calculate the horizontal and vertical delta vectors from pixel to pixel
    pixel_delta_u = (viewport_u / image_width)
    pixel_delta_v = (viewport_v / image_height)

    # calculate the location of the upper left pixel.
    viewport_upper_left = camera_center - Vector3(0.0, 0.0, focal_lenght) - (viewport_u/2) - (viewport_v/2)
    pixel_00_loc = viewport_upper_left +  (pixel_delta_u + pixel_delta_v)/2

    #Render
    print("P3")
    print(image_width, image_height)
    print(255)
    


    for j in range(image_height):
        print(f"\rScanlines remaining: {image_height - j} ", end='', flush=True)
        for i in range(image_width):
            pixel_center = pixel_00_loc + (pixel_delta_u * i) + (pixel_delta_v * j)
            ray_direction = pixel_center - camera_center
            r = (camera_center, ray_direction)

            pixel_colour = ray_colour(r)

            colour = pixel_colour
            ir = int(255.99*colour.r)
            ig = int(255.99*colour.g)
            ib = int(255.99*colour.b)
            value = "{ir} {ig} {ib}\n".format(ir=ir, ig=ig, ib=ib)
            print(value)


            
    
main()