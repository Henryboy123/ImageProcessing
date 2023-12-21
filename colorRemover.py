from PIL import Image, ImageEnhance
import os
import numpy as np

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Relative path to the image file from the script's directory
relative_path = 'MIDTERM/2M113/OOP.MT2.240315.m113.p1 copy.jpg'

# Construct the absolute path by joining the script's directory and the relative path
image_path = os.path.join(script_dir, relative_path)

img = Image.open(image_path)

# Display the original image
img.show()

# Convert the image to the HSV color space
img_hsv = img.convert("HSV")

# Define the range of red hues in HSV
lower_red = np.array([0, 250, 250])
upper_red = np.array([10, 255, 255])

# Create a mask to identify red pixels
mask = Image.eval(img_hsv.split()[0], lambda h: 255 if lower_red[0] < h < upper_red[0] else 0)

# Apply the mask to the original image
img = Image.composite(Image.new("RGB", img.size, (0, 0, 0)), Image.new("RGB", img.size, "white"), mask)

# Modify saturation and value
enhancer = ImageEnhance.Color(img)
img = enhancer.enhance(0)  # Set saturation to -100

enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(2.0)  # Set brightness (value) to +100

# Display the modified image
img.show()



# from PIL import Image
# import os

# # Get the current script's directory
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Relative path to the image file from the script's directory
# relative_path = 'MIDTERM/2M113/OOP.MT2.240315.m113.p1 copy.jpg'

# # Construct the absolute path by joining the script's directory and the relative path
# image_path = os.path.join(script_dir, relative_path)

# img = Image.open(image_path)

# img.show()

# for x in range(img.size[0]):
#     for y in range(img.size[1]):
#         r, g, b = img.getpixel((x,y))
#         if r < 50 and g < 50 and b < 50:
#             img.putpixel((x,y),(255,255,255))

# img.show()







# try:
#     os.startfile(image_path)
# except Exception as e:
#     print(f"Error: {e}")
