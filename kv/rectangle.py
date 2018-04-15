from kv.size import Size
from kv.point import Point


class Rectangle:
    def __init__(self, origin: Point, size: Size):
        self.origin = origin
        self.size = size

    @property
    def end(self) -> Point:
        """Return the bottom right point of the rectangle"""
        return Point(
            self.origin.x + self.size.width,
            self.origin.y + self.size.height
        )

    def encloses(self, rect) -> bool:
        if self.origin.x > rect.origin.x:
            return False
        if self.origin.y > rect.origin.y:
            return False
        if self.end.x < rect.end.x:
            return False
        if self.end.y < rect.end.y:
            return False

        return True

    @classmethod
    def from_xy_wh(cls, x, y, w, h):
        """Construct a rectangle from Origin (x, y) and Size (w, h)."""

        origin = Point(x, y)
        size = Size(w, h)
        return cls(origin, size)

    @classmethod
    def enclosing_rectangle(cls, rect1, rect2):
        """Construct a rectangle such that it encloses rect1 and rect2 completely"""
        origin = Point.inner(rect1.origin, rect2.origin)
        end = Point.outer(rect1.end, rect2.end)
        size = Size.from_origin_end_points(origin, end)
        return cls(origin, size)

    @staticmethod
    def has_similar_origins(rect1, rect2, delta=5) -> bool:
        return rect1.origin.distance_from_point(rect2.origin) < delta

    def __str__(self):
        return "Rectangle: Origin({}) Size({})".format(self.origin, self.size)
