from PIL import Image
from collections import Counter

image = Image.open('wplace.png')
image = image.convert('RGB')
pixels = list(image.getdata())
color_counts = Counter(pixels)
sorted_colors = color_counts.most_common()

color_list = list()

i = 0
for color, count in sorted_colors:
    if count < 100:
        continue
    i += 1
    print(
        '%02d' % i,
        '#%02x%02x%02x' % color,
        '\033[48;2;%d;%d;%dm  \033[0m' % color,
        count,
    )
