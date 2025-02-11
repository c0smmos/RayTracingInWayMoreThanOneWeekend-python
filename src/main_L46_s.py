from hittable_L19 import*
from hittable_list import*
from sphere_L20 import*
from camera_L45_s import*



def main():
    
    # World
    object_list = []
    
    object_list.append(Sphere(Vector3(0, 0, -1), 0.5))
    object_list.append(Sphere(Vector3(0, -100.5, -1), 100))
    
    
    world = Hittable_List(object_list)

    cam = Camera()

    # Set camera properties
    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.samples_per_pixel = 10

    # Render the scene
    cam.render(world)

if __name__ == "__main__":
    main()