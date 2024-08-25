import cv2
import numpy as np
import sys
import os

def convert_image_to_yuyv(image_path):
    # Read the image using OpenCV
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"Image file '{image_path}' not found")

    # Convert the image from BGR to YUV
    image_yuv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YUV)

    # Prepare YUYV data
    height, width, _ = image_yuv.shape
    yuyv_data = np.zeros((height, width * 2), dtype=np.uint8)

    # Fill YUYV data
    for y in range(height):
        for x in range(0, width, 2):
            yuyv_data[y, x * 2]     = image_yuv[y, x, 0]  # Y0
            yuyv_data[y, x * 2 + 1] = image_yuv[y, x, 1]  # U
            yuyv_data[y, x * 2 + 2] = image_yuv[y, x + 1, 0]  # Y1
            yuyv_data[y, x * 2 + 3] = image_yuv[y, x, 2]  # V

    # Derive the output C file path from the input image path
    output_c_file = os.path.splitext(image_path)[0] + ".c"

    # Save the YUYV data to a binary file
    yuyv_output_path = os.path.splitext(image_path)[0] + ".yuyv"
    with open(yuyv_output_path, 'wb') as f:
        f.write(yuyv_data.tobytes())

    # Generate C code for the YUYV data
    generate_c_code(yuyv_data, output_c_file)

def generate_c_code(yuyv_data, output_c_file):
    # Get the filename without the extension
    variable_name = os.path.basename(output_c_file).split('.')[0]

    # Convert the YUYV data to C code
    yuyv_data_flat = yuyv_data.flatten()
    c_code = f"const unsigned char {variable_name}_yuyv[] = {{\n"
    for i, value in enumerate(yuyv_data_flat):
        if i % 12 == 0:
            c_code += "\n"
        c_code += f"0x{value:02x}, "
    c_code = c_code.rstrip(", ") + "\n};"

    # Create the content for the C file
    c_file_content = f"#include <stdint.h>\n\n"
    c_file_content += c_code

    # Save the C code to the C file
    with open(output_c_file, 'w') as f:
        f.write(c_file_content)

    print(f"C file saved to {output_c_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_image_to_yuyv.py <input_image>")
        sys.exit(1)

    image_path = sys.argv[1]  # Path to the input image

    convert_image_to_yuyv(image_path)
