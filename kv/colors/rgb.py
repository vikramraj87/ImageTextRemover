class RGB:
    def __init__(self, red: int, green: int, blue: int):
        self._red = red
        self._green = green
        self._blue = blue

    @property
    def red(self) -> int:
        return self._red

    @property
    def green(self) -> int:
        return self._green

    @property
    def blue(self) -> int:
        return self._blue

    def as_tuple(self) -> (int, int, int):
        return self.red, self.green, self.blue
