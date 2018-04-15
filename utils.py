from kv.colors import RGB
from kv.image import Image, ImageMode
import math
import os

from matplotlib.figure import Figure
import cv2

class ContrastColorGenerator:
    colors: [RGB] = [
        RGB(230, 25, 75),
        RGB(60, 180, 75),
        RGB(255, 225, 25),
        RGB(0, 130, 200),
        RGB(245, 130, 48),
        RGB(145, 30, 180),
        RGB(70, 240, 240),
        RGB(240, 50, 230),
        RGB(210, 245, 60),
        RGB(250, 190, 190),
        RGB(0, 128, 128),
        RGB(230, 190, 255),
        RGB(170, 110, 40),
        RGB(255, 250, 200),
        RGB(128, 0, 0),
        RGB(170, 255, 195),
        RGB(128, 128, 0),
        RGB(255, 215, 180),
        RGB(0, 0, 128)
    ]

    def __init__(self):
        self._current_index = 0

    def next_color(self) -> RGB:
        color = __class__.colors[self._current_index % len(__class__.colors)]
        self._current_index += 1
        return color


def generate_subplots_for_images(figure: Figure,
                                 images: [Image],
                                 titles: [str] = [],
                                 ncols=1):
    if len(images) <= 0:
        return

    if len(titles) > 0 and len(titles) != len(images):
        raise ValueError(
            "There is no enough title ({}) for the images ({}) provided"
            .format(len(titles), len(images))
        )
    if ncols < 1:
        raise ValueError(
            "There should be at least one column in the plot"
        )

    nrows = math.ceil(len(images)/ncols)
    for image_idx, image in enumerate(images):
        ax = figure.add_subplot(nrows, ncols, image_idx+1, xticks=[], yticks=[])
        if len(titles) > 0:
            ax.set_title(titles[image_idx])

        if image.mode == ImageMode.GRAY:
            ax.imshow(image.data, cmap='gray')
        else:
            ax.imshow(image.data)


def load_images_from_folder(folder) -> [Image]:
    images: [Image] = []

    for filename in os.listdir(folder):
        img_data = cv2.imread(os.path.join(folder, filename))
        if img_data is None:
            continue
        img_data_rgb = cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB)
        images.append(Image(img_data_rgb, mode=ImageMode.RGB))

    return images
