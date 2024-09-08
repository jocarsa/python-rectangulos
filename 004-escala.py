from PIL import Image, ImageDraw
import random

# Variables for the grid
numero = 40
rectangle_width = int(numero*(1920/1080))  # Number of squares in a row
rectangle_height = numero  # Number of squares in a column

# Fixed image dimensions
image_width = 1920
image_height = 1080

# Calculate square size and distance based on image dimensions
max_square_size = image_width // (rectangle_width + 1)
distance = (image_width - (rectangle_width * max_square_size)) // (rectangle_width - 1)

# Create a new image with a white background
image = Image.new('RGB', (image_width, image_height), 'white')
draw = ImageDraw.Draw(image)

# Draw the squares with random sizes
for row in range(rectangle_height):
    for col in range(rectangle_width):
        # Calculate the center of the square
        center_x = col * (max_square_size + distance) + max_square_size // 2
        center_y = row * (max_square_size + distance) + max_square_size // 2
        
        # Generate a random size for the square
        random_size = random.randint(10, max_square_size)
        
        # Calculate the coordinates of the square based on the random size
        x0 = center_x - random_size // 2
        y0 = center_y - random_size // 2
        x1 = center_x + random_size // 2
        y1 = center_y + random_size // 2
        
        # Draw the square
        draw.rectangle([x0, y0, x1, y1], fill='black', outline='black')

# Display the image
image.show()
