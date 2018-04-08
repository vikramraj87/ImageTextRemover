import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def distance_from_point(self, point):
        delta_x = self.x - point.x
        delta_y = self.y - point.y
        return math.sqrt(delta_x * delta_x + delta_y * delta_y)

    @classmethod
    def inner(cls, point1, point2):
        """Returns a new point which is higher and to the left of both the points"""
        return Point(
            min(point1.x, point2.x),
            min(point1.y, point2.y)
        )

    @classmethod
    def outer(cls, point1, point2):
        """Returns a new point which is lower and to the right of both the points"""
        return cls(
            max(point1.x, point2.x),
            max(point1.y, point2.y)
        )

    def __str__(self):
        return "({}, {})".format(self.x, self.y)
