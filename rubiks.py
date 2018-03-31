RED = 1
YELLOW = 2
GREEN = 3
BLUE = 4
ORANGE = 5
WHITE = 6

COLORS = {RED: "R", YELLOW: "Y", GREEN: "G", BLUE: "B", ORANGE: "O", WHITE: "W"}


class Cube(object):

    front=None
    back=None
    top=None
    bottom=None
    left=None
    right=None

    def __init__(self):

        pass

    def __init__(self, front, back, top, bottom, left, right):

        self.front=front
        self.back=back
        self.top=top
        self.button=bottom
        self.left=left
        self.right=right

    pass

class Side(object):

    cubies = None

    def __init__(self, cubies):

        self.cubies=cubies

    def __repr__(self):
        output = ""
        for r in self.cubies:
            for c in r:
                output += COLORS.get(c)

            output += "\n"

        return output

class Cubie(object):

    s1 = None
    s2 = None
    s3 = None

    def __init__(self, s1, s2=None, s3=None):
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
