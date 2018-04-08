from kv.size import Size
from kv.point import Point


class Rectangle:
    def __init__(self, origin, size):
        self.origin = origin
        self.size = size

    @property
    def end(self):
        return Point(
            self.origin.x + self.size.width,
            self.origin.y + self.size.height
        )

    @classmethod
    def from_xy_wh(cls, x, y, w, h):
        origin = Point(x, y)
        size = Size(w, h)
        return cls(origin, size)

    @classmethod
    def enclosing_rectangle(cls, rect1, rect2):
        origin = Point.inner(rect1.origin, rect2.origin)
        end = Point.outer(rect1.end, rect2.end)
        size = Size.from_origin_end_points(origin, end)
        return cls(origin, size)

    @staticmethod
    def has_similar_origins(rect1, rect2, delta=5):
        return rect1.origin.distance_from_point(rect2.origin) < delta

    def __str__(self):
        return "Rectangle: Origin({}) Size({})".format(self.origin, self.size)