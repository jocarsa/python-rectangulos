from PIL import Image, ImageDraw

# Variables you can modify
rectangle_width = 5  # Number of squares in a row
rectangle_height = 4  # Number of squares in a column
square_size = 50  # Size of each square (width and height)
x_distance = 10  # Horizontal distance between squares
y_distance = 15  # Vertical distance between squares

# Calculate the size of the image
image_width = rectangle_width * (square_size + x_distance) - x_distance
image_height = rectangle_height * (square_size + y_distance) - y_distance

# Create a new image with a white background
image = Image.new('RGB', (image_width, image_height), 'white')
draw = ImageDraw.Draw(image)

# Draw the squares
for row in range(rectangle_height):
    for col in range(rectangle_width):
        x0 = col * (square_size + x_distance)
        y0 = row * (square_size + y_distance)
        x1 = x0 + square_size
        y1 = y0 + square_size
        draw.rectangle([x0, y0, x1, y1], fill='blue', outline='black')

# Save or display the image
image.show()  # This will display the image
#image.save('/mnt/data/rectangular_array_of_squares.png')  # This will save the image
