from PIL import Image
from collections import Counter
import os

GREEN_THRESHOLD = 0.4
PATH = "/media/frei/data/Wallpapers/wallpaper_ru/"

def max_rgb_color (img_path):
    rgb = Counter({'red': 0,
                   'green': 0,
                   'blue': 0})

    i = Image.open(img_path)
    colors = i.convert('RGB').getcolors(10000000)
    for color in colors:
        freq = color[0]
        for name, value in zip(('red', 'green', 'blue'), color[1]):
            rgb[name] += value * freq

    rgb_rel = {}
    rgb_sum = sum(rgb.values())

    for color, value in rgb.items():
        rgb_rel[color] = value / rgb_sum
    max_color = max(rgb_rel, key=rgb_rel.get)
    print(max_color, rgb_rel)
    if rgb_rel['green'] > GREEN_THRESHOLD or max_color == 'green':
        print(img_path)

for img in os.listdir(PATH):
    max_rgb_color(PATH + img)