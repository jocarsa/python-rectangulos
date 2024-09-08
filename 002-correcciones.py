from PIL import Image, ImageDraw

# Variables you can modify
rectangle_width = 10  # Number of squares in a row
rectangle_height = 5  # Number of squares in a column
square_size = 100  # Size of each square (width and height)
distance = 20  # Distance between squares (both x and y)

# Fixed image dimensions
image_width = 1920
image_height = 1080

# Create a new image with a white background
image = Image.new('RGB', (image_width, image_height), 'white')
draw = ImageDraw.Draw(image)

# Calculate starting positions to center the rectangle array
start_x = (image_width - (rectangle_width * square_size + (rectangle_width - 1) * distance)) // 2
start_y = (image_height - (rectangle_height * square_size + (rectangle_height - 1) * distance)) // 2

# Draw the squares
for row in range(rectangle_height):
    for col in range(rectangle_width):
        x0 = start_x + col * (square_size + distance)
        y0 = start_y + row * (square_size + distance)
        x1 = x0 + square_size
        y1 = y0 + square_size
        draw.rectangle([x0, y0, x1, y1], fill='blue', outline='black')

# Display the image
image.show()
