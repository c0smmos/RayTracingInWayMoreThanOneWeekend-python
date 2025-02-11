from vector import*
from ray import Ray


# standard libs
import os
import sys
import math



def hit_sphere(center, radius, r):
    oc = center - r.origin
    a = dot(r.direction, r.direction)
    h = dot(r.direction, oc)
    c = dot(oc, oc) - radius*radius
    discriminant = h*h - a*c
    if discriminant < 0.0:
        return -1.0                                             #If the discriminant is less than 0, there are no real roots, meaning the ray doesn't intersect the sphere. Return -1.0 to indicate no intersection.
    else:
        return (h - math.sqrt(discriminant)) / a


def ray_colour(r):
    t =  hit_sphere(Vector3(0.0, 0.0, -1.0), 0.5, r)
    if t > 0.0:
        N = unit_vector(r.point_at_t(t)- Vector3(0.0, 0.0, -1.0))
        return  Vector3(N.r + 1.0, N.g + 1.0, N.b + 1.0) * 0.5

    
    
    unit_direction = unit_vector(r.direction)
    # Graphics trick of scaling it to 0.0 < y < 1.0
    a = 0.5*(unit_direction.y + 1.0)
    # Lerping between (255, 255, 255) which is white to a light shade blue (128, 255*0.7, 255)
    return Vector3(1.0, 1.0, 1.0) * (1.0 - a) + Vector3(0.5, 0.7, 1.0) * a
    

def main():
    # image
    aspect_ratio = 16/9
    image_width = 400

    # Calculate the image height, and ensure that it's at least 1.
    image_height = int(image_width / aspect_ratio)
    image_height = max(image_height, 1)                              # if image_height < 1, then 1
    
    # Camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (image_width / image_height)
    camera_center = Vector3(0.0, 0.0, 0.0)

    # Calculate the vectors across the horizontal and down the vertical viewport edges.
    viewport_u = Vector3(viewport_width, 0.0, 0.0)                             # x, y, z (right handed)
    viewport_v = Vector3(0.0, -viewport_height, 0.0)

    # Calculate the horizontal and vertical delta vectors from pixel to pixel
    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    # calculate the location of the upper left pixel.
    viewport_upper_left = camera_center - Vector3(0.0, 0.0, focal_length) - (viewport_u/2) - (viewport_v/2)
    pixel_00_loc = viewport_upper_left +  (pixel_delta_u + pixel_delta_v)/2

    #Render
    path = os.path.join(os.path.dirname(__file__),"..","images", "blue_white_background_surface_normals.ppm")
    ppm_file = open(path, 'w')
    title = "P3\n{iw} {ih}\n 255\n".format(iw = image_width, ih = image_height)
    ppm_file.write(title)


    for j in range(image_height):
        print(f"\rScanlines remaining: {image_height - j} ", end='', flush=True)
        for i in range(image_width):
            pixel_center = pixel_00_loc + (pixel_delta_u * i) + (pixel_delta_v * j)
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)

            pixel_colour = ray_colour(r)

            
            ir = int(255.99*pixel_colour.r)
            ig = int(255.99*pixel_colour.g)
            ib = int(255.99*pixel_colour.b)
            value = (f"{ir} {ig} {ib}\n")
            ppm_file.write(value)
    print("\rDone.                 ", end="", flush=True)
    ppm_file.close()
    
            



if __name__ == "__main__":
    main()   