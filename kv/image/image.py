import cv2
import math
import numpy as np
from kv.image.image_mode import ImageMode
from kv import Size


class Image:
    def __init__(self, data, mode=ImageMode.BGR):
        self._data = data
        self._mode = mode

    @property
    def data(self):
        return self._data

    @property
    def mode(self):
        return self._mode

    @property
    def width(self):
        return self.data.shape[1]

    @property
    def height(self):
        return self.data.shape[0]

    @property
    def size(self):
        return Size(self.width, self.height)

    @property
    def aspect_ratio(self):
        return self.width / self.height

    @classmethod
    def copy(cls, img, target_mode=None):
        dst_mode = target_mode if target_mode else img.mode

        if img.mode == ImageMode.GRAY:
            if dst_mode != ImageMode.GRAY:
                raise ValueError("Cannot convert Gray scale image to Color.")

        img_data_copy = np.copy(img.data)
        if img.mode == dst_mode:
            return cls(img_data_copy, mode=dst_mode)

        converter = None
        if img.mode == ImageMode.BGR:
            if dst_mode == ImageMode.RGB:
                converter = cv2.COLOR_BGR2RGB
            elif dst_mode == ImageMode.GRAY:
                converter = cv2.COLOR_BGR2GRAY
        elif img.mode == ImageMode.RGB:
            if dst_mode == ImageMode.BGR:
                converter = cv2.COLOR_RGB2BGR
            elif dst_mode == ImageMode.GRAY:
                converter = cv2.COLOR_RGB2GRAY

        if not converter:
            raise ValueError("Cannot convert from {} to {}".format(img.mode, dst_mode))

        img_data_copy = cv2.cvtColor(img_data_copy, converter)
        return cls(img_data_copy, mode=dst_mode)

    @classmethod
    def downsize(cls, img, largest_dimension):
        img_copy = cls.copy(img)
        if img.size.max_dimension <= largest_dimension:
            return img_copy

        target_size = None
        if img.aspect_ratio >= 1:
            new_w = largest_dimension
            new_h = math.floor(largest_dimension * 1 / img.aspect_ratio + 0.5)
            target_size = Size(new_w, new_h)
        else:
            new_h = largest_dimension
            new_w = math.floor(largest_dimension * img.aspect_ratio + 0.5)
            target_size = Size(new_w, new_h)

        return cls.resize(img, target_size)

    @classmethod
    def resize(cls, img, target_size):
        img_copy = cls.copy(img)

        interpolation = None
        # When upscaling
        if img.size.max_dimension < target_size.max_dimension:
            interpolation = cv2.INTER_CUBIC
        # When downscaling
        else:
            interpolation = cv2.INTER_AREA

        data = cv2.resize(img_copy.data,
                          target_size.as_tuple(),
                          interpolation=interpolation)
        return Image(data, mode=img.mode)

    @classmethod
    def center_image_in_square(cls, image, side, padding=2):
        """Center image in a square of side"""
        downsized_image = cls.downsize(image, side - 2 * padding)

        data = np.zeros((side, side))
        center = side / 2.
        org_x = max(0., math.floor(center - downsized_image.width / 2.))
        org_y = max(0., math.floor(center - downsized_image.height / 2.))
        end_x = org_x + downsized_image.width
        end_y = org_y + downsized_image.height
        data[org_y:end_y, org_x:end_x] = downsized_image.data

        return cls(data, mode=image.mode)
