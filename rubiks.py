RED = 1
YELLOW = 2
GREEN = 3
BLUE = 4
ORANGE = 5
WHITE = 6


class Cube(object):

    pass


class Piece(object):

    s1 = None
    s2 = None
    s3 = None

    def __init__(self, s1, s2=None, s3=None):
        """
        :type s1: int
        :type s2: int
        :type s3: int
        """
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3

    def __repr__(self):

        if self.is_center:

            return "Center"

        elif self.is_side:

            return "Side"

        return "Corner"

    @property
    def is_center(self):

        if self.s1 is not None and self.s2 is None and self.s3 is None:

            return True

        return False

    @property
    def is_side(self):

        if self.s1 is not None and self.s2 is not None and self.s3 is None:

            return True

        return False

    @property
    def is_corner(self):

        if self.s1 is not None and self.s2 is not None and self.s3 is not None:

            return True

        return False
