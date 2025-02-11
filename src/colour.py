from vector import Vector3

# Define `colour` as an alias for Vector3
colour = Vector3

def write_colour(pixel_colour):
    r = pixel_colour.x
    g = pixel_colour.y
    b = pixel_colour.z

    # Translate the [0,1] component values to the byte range [0,255].
    rbyte = int(255.999 * r)
    gbyte = int(255.999 * g)
    bbyte = int(255.999 * b)

    # Write out the pixel colour components.
    print(f"{rbyte} {gbyte} {bbyte}")