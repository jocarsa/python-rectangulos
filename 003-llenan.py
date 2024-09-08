from PIL import Image, ImageDraw

# Variables for the grid
rectangle_width = 19  # Number of squares in a row
rectangle_height = 10  # Number of squares in a column

# Fixed image dimensions
image_width = 1920
image_height = 1080

# Calculate square size and distance based on image dimensions
square_size = image_width // (rectangle_width + 1)
distance = (image_width - (rectangle_width * square_size)) // (rectangle_width - 1)

# Create a new image with a white background
image = Image.new('RGB', (image_width, image_height), 'white')
draw = ImageDraw.Draw(image)

# Draw the squares
for row in range(rectangle_height):
    for col in range(rectangle_width):
        x0 = col * (square_size + distance)
        y0 = row * (square_size + distance)
        x1 = x0 + square_size
        y1 = y0 + square_size
        draw.rectangle([x0, y0, x1, y1], fill='black', outline='black')

# Display the image
image.show()
