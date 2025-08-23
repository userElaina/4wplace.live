from PIL import Image

original_image = Image.open('7.png')
original_image = original_image.convert('RGB')
original_width, original_height = original_image.size

new_width = original_width // 10
new_height = original_height // 10

resized_image = Image.new('RGB', (new_width, new_height))

for y in range(new_height):
    for x in range(new_width):
        top_left_x = x * 10
        top_left_y = y * 10

        pixel_color = original_image.getpixel((top_left_x, top_left_y))
        resized_image.putpixel((x, y), pixel_color)

resized_image.save('r.png')
