# image
aspect_ratio = 16/9
image_width = 400

# Calculate the image height, and ensure that it's at least 1.
image_height = int(image_width / aspect_ratio)
image_height = max(image_height, 1)                              # if image_height < 1, then 1

# Viewport widths less than one are ok since they are real valued.
viewport_height = 2.0
viewport_width = viewport_height * (image_width / image_height)

















