import numpy as np
from kv.image import ImageMode, GrayscaleImage
from kv import Rectangle


class MSERRegion:
    def __init__(self, bbox):
        self.bounding_box = bbox
        self.points = []

    def add_point(self, point):
        self.points.append(point)

    def add_region(self, region):
        self.bounding_box = Rectangle.enclosing_rectangle(
            self.bounding_box,
            region.bounding_box
        )
        self.points = self.points + region.points

    @property
    def image(self) -> GrayscaleImage:
        w, h = self.bounding_box.size.as_tuple()
        x, y = self.bounding_box.origin.as_tuple()
        data = np.zeros((h, w))
        for point, value in self.points:
            data[point.y - y, point.x - x] = value
        img = GrayscaleImage(data)
        return img

    def plot_in_mask(self, mask: GrayscaleImage):
        for point in self.points:
            mask.data[point.y, point.x] = 255

