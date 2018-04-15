class Size:
    def __init__(self, w, h):
        self.width = w
        self.height = h

    @classmethod
    def from_origin_end_points(cls, origin, end):
        return cls(
            abs(origin.x - end.x),
            abs(origin.y - end.y)
        )

    def __str__(self):
        return "({}, {})".format(self.width, self.height)

    def __eq__(self, other):
        return (self.width, self.height) == (other.width, other.height)

    def __ne__(self, other):
        return not self == other

    def as_tuple(self):
        return self.width, self.height

    @property
    def max_dimension(self):
        return self.width if self.width > self.height else self.height
