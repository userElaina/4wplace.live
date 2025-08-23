import numpy as np
from PIL import Image
from collections import Counter

image = Image.open('wplace.png')
image = image.convert('RGB')
pixels = list(image.getdata())

color_counts = Counter(pixels)
# sorted_colors = color_counts.most_common()
sorted_colors = color_counts.items()

color_list = list()

i = 0
for color, count in sorted_colors:
    if count < 6000:
        continue
    i += 1
    if i not in (33, 34):
        color_list.append(color)
    print(
        '%02d' % i,
        '#%02x%02x%02x' % color,
        '\033[48;2;%d;%d;%dm  \033[0m' % color,
        count,
    )

# 33 #fefeff    7136
# 34 #617187    6979

def hamming_distance(color1, color2):
    return np.sum(np.abs(np.array(color1) - np.array(color2)))

def replace_with_nearest_color(image, color_list):
    image_np = np.array(image)
    new_image = np.copy(image_np)

    for i in range(image_np.shape[0]):
        for j in range(image_np.shape[1]):
            pixel = image_np[i, j]
            nearest_color = min(
                color_list,
                key=lambda x: hamming_distance(pixel, x)
            )
            new_image[i, j] = nearest_color
    
    return Image.fromarray(new_image)

image = Image.open('r.png')
image = image.convert('RGB')

new_image = replace_with_nearest_color(image, color_list)
new_image.save('rr.png')
