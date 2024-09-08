from PIL import Image, ImageDraw
import noise
import numpy as np
import cv2  # OpenCV for video creation
import os
import random
import time

# Video properties
frame_width = 1920
frame_height = 1080
fps = 60
duration = 60  # Duration in seconds
total_frames = fps * duration

# Grid properties
numero = 50
circle_columns = numero
circle_rows = numero

# Calculate circle size and distance
max_circle_size = frame_width // (circle_columns + 1)
distance = (frame_width - (circle_columns * max_circle_size)) // (circle_columns - 1)

# Create a video writer object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('render/perlin_noise_video.mp4', fourcc, fps, (frame_width, frame_height))

# Parameters for Perlin noise
initial_scale = float(100)
initial_octaves = 2
initial_lacunarity = 5.0

# Start time for progress tracking
start_time = time.time()

for frame in range(total_frames):
    # Adjust Perlin noise parameters over time more slowly
    scale = initial_scale + (frame / total_frames) * 10  # Gradually increase scale more slowly
    octaves = initial_octaves
    lacunarity = initial_lacunarity + (frame / total_frames) * 1  # Gradually increase lacunarity more slowly

    # Create a new image with a white background
    image = Image.new('RGB', (frame_width, frame_height), 'white')
    draw = ImageDraw.Draw(image)

    # Generate the Perlin noise pattern and normalize it to fit circle sizes
    noise_array = np.zeros((circle_rows, circle_columns))
    for y in range(circle_rows):
        for x in range(circle_columns):
            noise_value = noise.pnoise2(x / scale,
                                        y / scale,
                                        octaves=octaves,
                                        persistence=1,
                                        lacunarity=lacunarity,
                                        repeatx=circle_columns,
                                        repeaty=circle_rows,
                                        base=frame)  # Use the frame number as the seed
            # Normalize the noise value to be between 10 and max_circle_size with a reduced range
            noise_value = (noise_value + 0.5) * (max_circle_size * 0.5 - 10) + 10
            noise_array[y][x] = noise_value

    # Draw the circles based on Perlin noise
    for row in range(circle_rows):
        for col in range(circle_columns):
            center_x = col * (max_circle_size + distance) + max_circle_size // 2
            center_y = row * (max_circle_size + distance) + max_circle_size // 2

            size = int(noise_array[row][col])
            x0 = center_x - size // 2
            y0 = center_y - size // 2
            x1 = center_x + size // 2
            y1 = center_y + size // 2

            draw.ellipse([x0, y0, x1, y1], fill='black', outline='black')

    # Convert the image to a NumPy array and write it to the video
    frame_array = np.array(image)
    video.write(cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR))

    # Print progress every 60 frames
    if (frame + 1) % 60 == 0:
        elapsed_time = time.time() - start_time
        remaining_time = (elapsed_time / (frame + 1)) * (total_frames - frame - 1)
        estimated_finish_time = start_time + elapsed_time + remaining_time
        completion_percentage = (frame + 1) / total_frames * 100

        print(f"Frames: {frame + 1}/{total_frames}")
        print(f"Time Passed: {elapsed_time:.2f} seconds")
        print(f"Time Remaining: {remaining_time:.2f} seconds")
        print(f"Estimated Time of Finish: {time.strftime('%H:%M:%S', time.localtime(estimated_finish_time))}")
        print(f"Completion: {completion_percentage:.2f}%\n")

# Release the video writer
video.release()
