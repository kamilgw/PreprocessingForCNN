import sys
import time
from pathlib import Path
from PIL import Image


images_folder = Path("D:/Wagony/zdjWag")
all_images = images_folder.glob('*.jpg')
starting_number = 29
items = [x for x in all_images if x.is_file()]


def progress(count, total, status='', bar_len=60):
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    fmt = '[%s] %s%s ...%s' % (bar, percents, '%', status)
    print('\b' * len(fmt), end='')  # clears the line
    sys.stdout.write(fmt)
    sys.stdout.flush()


def resize(start_from):
    # Print progress bar
    progress(0, len(items), 'Start')
    for i, item in enumerate(items):
        im = Image.open(item)
        new_path = images_folder / f'{start_from}.png'
        # Set the size of image to 1920x1080
        imResize = im.resize((1920, 1080), Image.ANTIALIAS)
        imResize.save(new_path, quality=90)
        # Refresh progress bar
        progress(i + 1, len(items), 'Resizing files')
        time.sleep(0.05)
        start_from += 1


resize(starting_number)
