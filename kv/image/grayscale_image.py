from kv import Size
from kv.image.image import Image
from kv.image.image_mode import ImageMode
import numpy as np
import cv2


class GrayscaleImage(Image):
    def __init__(self, data):
        super().__init__(data, mode=ImageMode.GRAY)

    def dilate(self, kernel_size: int=5, iterations: int=1):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self._data = cv2.dilate(self._data, kernel, iterations=iterations)

    @classmethod
    def black_canvas(cls, size: Size):
        data = np.zeros((size.height, size.width)).astype(np.uint8)
        return cls(data)
