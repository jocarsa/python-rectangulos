from PIL import Image, ImageDraw
import noise
import numpy as np
import os
import time
import random

# Create the "render" directory if it doesn't exist
if not os.path.exists('render'):
    os.makedirs('render')

contador = 1
for i in range(300):  # Iterate 5 times to create 5 images
    try:
        # Variables for the grid
        numero = random.randint(10,200)  # Increase the number to accommodate the larger image size
        rectangle_width = int(numero * (8192 / 8192))  # Number of squares in a row
        rectangle_height = numero  # Number of squares in a column

        # Fixed image dimensions
        image_width = 8192
        image_height = 8192

        # Calculate square size and distance based on image dimensions
        max_square_size = image_width // (rectangle_width + 1)
        distance = (image_width - (rectangle_width * max_square_size)) // (rectangle_width - 1)

        # Create a new image with a white background
        image = Image.new('RGB', (image_width, image_height), 'white')
        draw = ImageDraw.Draw(image)

        # Parameters for Perlin noise
        scale = float(random.randint(1,100))  # Adjust for more or less noise variation, scaled up for larger image
        octaves = random.randint(1,5)  # Number of levels of detail (higher = more detail)
        persistence = 1  # Amplitude of noise (higher = more contrast)
        lacunarity = 5.0  # Frequency of noise (higher = more features)
        
        # Generate a new seed for each image
        noise_seed = i  # Or use a random value for even more variation

        # Generate the Perlin noise pattern and normalize it to fit square sizes
        noise_array = np.zeros((rectangle_height, rectangle_width))
        for y in range(rectangle_height):
            for x in range(rectangle_width):
                noise_value = noise.pnoise2(x / scale, 
                                            y / scale, 
                                            octaves=octaves, 
                                            persistence=persistence, 
                                            lacunarity=lacunarity, 
                                            repeatx=rectangle_width, 
                                            repeaty=rectangle_height, 
                                            base=noise_seed)  # Use the noise_seed
                # Normalize noise value to be between 10 and max_square_size
                noise_value = (noise_value + 0.5) * (max_square_size - 10) + 10
                noise_array[y][x] = noise_value

        # Draw the squares based on Perlin noise
        for row in range(rectangle_height):
            for col in range(rectangle_width):
                # Calculate the center of the square
                center_x = col * (max_square_size + distance) + max_square_size // 2
                center_y = row * (max_square_size + distance) + max_square_size // 2
                
                # Get the size from the noise array
                size = int(noise_array[row][col])
                
                # Calculate the coordinates of the square based on the noise size
                x0 = center_x - size // 2
                y0 = center_y - size // 2
                x1 = center_x + size // 2
                y1 = center_y + size // 2
                
                # Draw the square
                draw.rectangle([x0, y0, x1, y1], fill='black', outline='black')

        # Get the current epoch time
        epoch_time = int(time.time())
        contador += 1

        # Save the image to the "render" folder with the epoch time as the filename
        image.save(f'render/image_{epoch_time}_{contador}.png')
    except:
        print("error")
