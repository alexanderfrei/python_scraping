import os
import re

START_PATH = r""

dir_list = os.listdir(START_PATH)
with open('./img.txt', 'w') as fl:
    for dir in dir_list:
        if (os.path.isdir(os.path.join(START_PATH, dir))):
            for img in os.listdir(os.path.join(START_PATH, dir)):
                img_name = os.path.basename(img)
                if re.match('.*(png|jpg|jpeg|gif)', img_name):
                    fl.write(img_name + '\n')

