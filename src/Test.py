"""
hello = "hello world!"
print(hello)

n: int = 10000000000
print(f'{n:,}')

from vector import Vector3

def subtraction():
    a = Vector3(1.0, 1.0, 2.0)-Vector3(1.0, 1.0, 0.0)
    return a



print(subtraction())

"""

from vector import Vector3, unit_vector
from ray import Ray

def ray_colour(r):
    unit_direction = unit_vector(r.direction)
    t = 0.5 * (unit_direction.y + 1.0)
    return Vector3(1.0, 1.0, 1.0) * (1.0 - t) + Vector3(0.5, 0.7, 1.0) * t

def main():
    aspect_ratio = 16 / 9
    image_width = 400
    image_height = max(int(image_width / aspect_ratio), 1)

    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * aspect_ratio
    camera_center = Vector3(0.0, 0.0, 0.0)

    viewport_u = Vector3(viewport_width, 0.0, 0.0)
    viewport_v = Vector3(0.0, -viewport_height, 0.0)

    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    viewport_upper_left = (
        camera_center
        - Vector3(0.0, 0.0, focal_length)
        - viewport_u / 2
        - viewport_v / 2
    )
    pixel_00_loc = viewport_upper_left + (pixel_delta_u + pixel_delta_v) / 2

    print("P3")
    print(image_width, image_height)
    print(255)

    for j in range(image_height):
        print(f"\rScanlines remaining: {image_height - j} ", end='', flush=True)
        for i in range(image_width):
            pixel_center = pixel_00_loc + (pixel_delta_u * i) + (pixel_delta_v * j)
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)

            pixel_colour = ray_colour(r)

            ir = int(255.99 * pixel_colour.x)
            ig = int(255.99 * pixel_colour.y)
            ib = int(255.99 * pixel_colour.z)
            print(f"{ir} {ig} {ib}")

if __name__ == "__main__":
    main()

