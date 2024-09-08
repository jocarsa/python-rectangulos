from PIL import Image, ImageDraw
import noise
import numpy as np
import os
import time

# Create a folder named 'render' if it doesn't exist
if not os.path.exists('render'):
    os.makedirs('render')

for i in range(5):
    try:
        print(f"Starting iteration {i+1}")
        
        # Variables for the grid
        numero = 40
        rectangle_width = int(numero * (1920 / 1080))  # Number of squares in a row
        rectangle_height = numero  # Number of squares in a column

        # Fixed image dimensions
        image_width = 1920
        image_height = 1080

        # Calculate square size and distance based on image dimensions
        max_square_size = image_width // (rectangle_width + 1)
        distance = (image_width - (rectangle_width * max_square_size)) // (rectangle_width - 1)

        # Create a new image with a white background
        print("Creating a new image...")
        image = Image.new('RGB', (image_width, image_height), 'white')
        draw = ImageDraw.Draw(image)

        # Parameters for Perlin noise
        scale = 10.0  # Adjust for more or less noise variation
        octaves = 1  # Number of levels of detail (higher = more detail)
        persistence = 0.5  # Amplitude of noise (higher = more contrast)
        lacunarity = 2.0  # Frequency of noise (higher = more features)

        # Generate the Perlin noise pattern and normalize it to fit square sizes
        noise_array = np.zeros((rectangle_height, rectangle_width))
        seed = int(time.time())  # Use the current epoch time as a seed
        print("Generating Perlin noise...")
        for y in range(rectangle_height):
            for x in range(rectangle_width):
                noise_value = noise.pnoise2(x / scale, 
                                            y / scale, 
                                            octaves=octaves, 
                                            persistence=persistence, 
                                            lacunarity=lacunarity, 
                                            repeatx=rectangle_width, 
                                            repeaty=rectangle_height, 
                                            base=seed)
                # Normalize noise value to be between 10 and max_square_size
                noise_value = (noise_value + 0.5) * (max_square_size - 10) + 10
                noise_array[y][x] = noise_value
        
        print("Drawing squares based on noise...")
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

        # Save the image using the epoch time
        filename = f'render/image_{int(time.time())}.png'
        print(f"Saving image to {filename}")
        image.save(filename)

    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        print(f"Iteration {i+1} completed successfully.")
