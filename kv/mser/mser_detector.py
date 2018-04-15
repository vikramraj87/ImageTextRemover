import cv2
from kv.image import ImageMode, Image
from kv import Rectangle, Point
from kv.mser.mser_region import MSERRegion


class MSERDetector:
    def __init__(self, delta=35):
        self._mser = cv2.MSER_create(delta)

    def detect(self, image):
        image = Image.copy(image, target_mode=ImageMode.GRAY)

        regions = []
        regs, bboxes = self._mser.detectRegions(image.data)
        for points, (x, y, w, h) in zip(regs, bboxes):
            bounding_box = Rectangle.from_xy_wh(x, y, w, h)

            # Create a new region if no regions are created till
            if len(regions) == 0:
                regions.append(MSERRegion(bounding_box))

            # During the first iteration both prev_region and current_region
            # are same
            prev_region = regions[-1]
            current_region = None

            if Rectangle.has_similar_origins(prev_region.bounding_box, bounding_box):
                new_bounding_box = Rectangle.enclosing_rectangle(
                    prev_region.bounding_box,
                    bounding_box)
                prev_region.bounding_box = new_bounding_box
                current_region = prev_region
            else:
                current_region = MSERRegion(bounding_box)
                regions.append(current_region)

            for pt_x, pt_y in points:
                point = Point(pt_x, pt_y)
                current_region.add_point(point)

        return regions
