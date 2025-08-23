import numpy as np
from PIL import Image
from collections import Counter

image = Image.open('r.png')

image = image.convert('RGB')

pixels = list(image.getdata())

color_counts = Counter(pixels)
sorted_colors = color_counts.most_common()

i = 0
for color, count in sorted_colors:
    i += 1
    print(
        '%02d' % i,
        '#%02x%02x%02x' % color,
        '\033[48;2;%d;%d;%dm  \033[0m' % color,
        count,
    )

for color, count in color_counts.items():
    i2 = image.copy()
    for y in range(i2.height):
        for x in range(i2.width):
            if i2.getpixel((x, y)) == color:
                i2.putpixel((x, y), (0, 0, 0))
    i2.save('split/%02x%02x%02x.png' % color)

