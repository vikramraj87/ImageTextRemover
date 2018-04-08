import numpy as np
from kv.image import ImageMode, Image


class MSERRegion:
    def __init__(self, bbox):
        self.bounding_box = bbox
        self.points = []

    def add_point(self, point, value=255):
        self.points.append((point, value))

    @property
    def image(self):
        w, h = self.bounding_box.size.as_tuple()
        x, y = self.bounding_box.origin.as_tuple()
        data = np.zeros((h, w))
        for point, value in self.points:
            data[point.y - y, point.x - x] = value
        img = Image(data, mode=ImageMode.GRAY)
        return img
