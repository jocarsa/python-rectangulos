from PIL import Image, ImageDraw, ImageEnhance
import noise
import numpy as np
import os
import time
import random
import colorsys

# Create the "render" directory if it doesn't exist
if not os.path.exists('render'):
    os.makedirs('render')

contador = 1
for i in range(300):  # Iterate 300 times to create 300 images
    try:
        # Variables for the grid
        numero = random.randint(10,200)  # Increase the number to accommodate the larger image size
        circle_columns = int(numero * (8192 / 8192))  # Number of circles in a row
        circle_rows = numero  # Number of circles in a column

        # Fixed image dimensions
        image_width = 8192
        image_height = 8192

        # Antialiasing factor (draw on a larger image and then downscale)
        aa_factor = 2
        large_image_width = image_width * aa_factor
        large_image_height = image_height * aa_factor

        # Calculate circle size and distance based on the larger image dimensions
        max_circle_size = large_image_width // (circle_columns + 1)
        distance = (large_image_width - (circle_columns * max_circle_size)) // (circle_columns - 1)

        # Create a new large image with a white background
        large_image = Image.new('RGB', (large_image_width, large_image_height), 'white')
        draw = ImageDraw.Draw(large_image)

        # Parameters for Perlin noise
        scale = float(random.randint(1,100))  # Adjust for more or less noise variation, scaled up for larger image
        octaves = random.randint(1,5)  # Number of levels of detail (higher = more detail)
        persistence = 1  # Amplitude of noise (higher = more contrast)
        lacunarity = 5.0  # Frequency of noise (higher = more features)
        
        # Generate a new seed for each image
        noise_seed = i  # Or use a random value for even more variation

        # Generate the Perlin noise pattern and normalize it to fit circle sizes
        noise_array = np.zeros((circle_rows, circle_columns))
        for y in range(circle_rows):
            for x in range(circle_columns):
                noise_value = noise.pnoise2(x / scale, 
                                            y / scale, 
                                            octaves=octaves, 
                                            persistence=persistence, 
                                            lacunarity=lacunarity, 
                                            repeatx=circle_columns, 
                                            repeaty=circle_rows, 
                                            base=noise_seed)  # Use the noise_seed
                # Normalize noise value to be between 10 and max_circle_size
                noise_value = (noise_value + 0.5) * (max_circle_size - 10) + 10
                noise_array[y][x] = noise_value

        # Draw the circles based on Perlin noise with a hue gradient
        for row in range(circle_rows):
            for col in range(circle_columns):
                # Calculate the center of the circle
                center_x = col * (max_circle_size + distance) + max_circle_size // 2
                center_y = row * (max_circle_size + distance) + max_circle_size // 2
                
                # Get the size from the noise array
                size = int(noise_array[row][col])
                
                # Calculate the coordinates of the circle based on the noise size
                x0 = center_x - size // 2
                y0 = center_y - size // 2
                x1 = center_x + size // 2
                y1 = center_y + size // 2
                
                # Map the size to a hue gradient (0 is red, 0.67 is blue in HSV)
                hue = (size - 10) / (max_circle_size - 10) * 0.67  # Map size to hue
                rgb_color = colorsys.hsv_to_rgb(hue, 1.0, 1.0)  # Convert HSV to RGB
                rgb_color = tuple(int(255 * c) for c in rgb_color)  # Convert to 8-bit RGB

                # Draw the circle (ellipse with equal width and height)
                draw.ellipse([x0, y0, x1, y1], fill=rgb_color, outline=rgb_color)

        # Apply a random hue shift to the entire image
        hue_offset = random.uniform(0, 1)  # Random hue shift between 0 and 1

        # Convert the large image to HSV
        hsv_image = large_image.convert('HSV')
        hsv_array = np.array(hsv_image)

        # Apply the hue shift
        hsv_array[..., 0] = (hsv_array[..., 0].astype(np.float32) / 255.0 + hue_offset) % 1.0 * 255.0

        # Convert back to RGB
        shifted_image = Image.fromarray(hsv_array, 'HSV').convert('RGB')

        # Downscale the image to the original dimensions for antialiasing
        final_image = shifted_image.resize((image_width, image_height), Image.Resampling.LANCZOS)

        # Get the current epoch time
        epoch_time = int(time.time())
        contador += 1

        # Save the image to the "render" folder with the epoch time as the filename
        final_image.save(f'render/image_{epoch_time}_{contador}.png')
    except Exception as e:
        print("Error:", e)
