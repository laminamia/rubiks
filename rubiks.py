from _ctypes import Array

from colorama import Back, Style, Fore

class Color(object):

    def __init__(self, char, colorcode):

        self.char = char
        self.colorcode = colorcode

    def opposite(self):

        return OPPOSITES.get(self)

    def __repr__(self):

        return Style.BRIGHT + Fore.BLACK + self.colorcode + self.char + Style.RESET_ALL

    def __eq__(self, other):

        return self.char == other.char

    def __hash__(self):

        return self.char.__hash__()


RED = Color("R", Back.RED)
YELLOW = Color("Y", Back.LIGHTYELLOW_EX)
GREEN = Color("G", Back.GREEN)
BLUE = Color("B", Back.BLUE)
ORANGE = Color("O", Back.LIGHTRED_EX)
WHITE = Color("W", Back.WHITE)
COLORS = [RED, YELLOW, GREEN, BLUE, ORANGE, WHITE]
OPPOSITES = {RED: ORANGE, ORANGE: RED, YELLOW: WHITE, WHITE: YELLOW, BLUE: GREEN, GREEN: BLUE}


class Cube(object):

    @staticmethod
    def create_solved_cube():
        front = Side.create_unicolor_side(BLUE)
        back = Side.create_unicolor_side(front.center_color().opposite())

        left = Side.create_unicolor_side(RED)
        right = Side.create_unicolor_side(left.center_color().opposite())

        top = Side.create_unicolor_side(WHITE)
        bottom = Side.create_unicolor_side(top.center_color().opposite())

        return Cube(front, back, left, right, top, bottom)

    def __init__(self, front, back, left, right, top, bottom):

        self.front = front
        self.back = back
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def __repr__(self):

        return "Front\n" + str(self.front) + \
                "Back\n" + str(self.back) + \
                "Left\n" + str(self.left) + \
                "Right\n" + str(self.right) + \
                "Top\n" + str(self.top) + \
                "Bottom\n" + str(self.bottom)

    def rotate_front_cw(self):
        # rotate pieces that change on other faces
        for i in [0, 1, 2]:
            # save right before it is rewritten
            _right = self.right.cubies[i][0]

            # fix right: top last row -> right first column
            self.right.cubies[i][0] = self.top.cubies[2][i]

            # fix top: left last column -> top last row
            self.top.cubies[2][i] = self.left.cubies[i][2]

            # fix left: bottom first row ->
            # bottom side first row is adjacent to front last row
            # swap each item in bottom first row to last item of each row of left side
            self.left.cubies[i][2] = self.bottom.cubies[0][i]

            # fix bottom
            # right side first column is adjacent to front
            # swap each item in right first column to first row of bottom
            self.bottom.cubies[0][i] = _right

        # rotate turned face pieces - middles
        # save right middle
        _temp = self.front.cubies[1][2]
        # top middle to right middle
        self.front.cubies[1][2] = self.front.cubies[0][1]
        # left middle to top middle
        self.front.cubies[0][1] = self.front.cubies[1][0]
        # bottom middle to left middle
        self.front.cubies[1][0] = self.front.cubies[2][1]
        # right middle to bottom middle
        self.front.cubies[2][1] = _temp

        # rotate turned face pieces - corners
        # save top right
        _temp = self.front.cubies[0][2]
        # top left to top right
        self.front.cubies[0][2] = self.front.cubies[0][0]
        # bottom left to top left
        self.front.cubies[0][0] = self.front.cubies[2][0]
        # bottom right to bottom left
        self.front.cubies[2][0] = self.front.cubies[2][2]
        # top right to bottom right
        self.front.cubies[2][2] = _temp

    def rotate_front_ccw(self):

        # rotate pieces that change on other faces
        for i in [0, 1, 2]:
            # save right before it is rewritten
            _temp = self.right.cubies[i][0]

            # fix right: bottom first row -> right first column
            self.right.cubies[i][0] = self.bottom.cubies[0][i]

            # fix bottom: left last column -> bottom first row
            self.bottom.cubies[0][i] = self.left.cubies[i][2]

            # fix left: top last row -> left last column
            self.left.cubies[i][2] = self.top.cubies[2][i]

            # fix top: right first column -> top last row
            self.top.cubies[2][i] = _temp

        # rotate turned face pieces - middles
        # save right middle
        _temp = self.front.cubies[1][2]
        # bottom middle to right middle
        self.front.cubies[1][2] = self.front.cubies[2][1]
        # left middle to bottom middle
        self.front.cubies[2][1] = self.front.cubies[1][0]
        # top middle to left middle
        self.front.cubies[1][0] = self.front.cubies[0][1]
        # right middle to top middle
        self.front.cubies[0][1] = _temp

        # rotate turned face pieces - corners
        # save top right
        _temp = self.front.cubies[0][2]
        # bottom right to top right
        self.front.cubies[0][2] = self.front.cubies[2][2]
        # bottom left to bottom right
        self.front.cubies[2][2] = self.front.cubies[2][0]
        # top left to bottom left
        self.front.cubies[2][0] = self.front.cubies[0][0]
        # top right to top left
        self.front.cubies[0][0] = _temp


class Side(object):

    # todo Consider using numpy arrays instead

    @staticmethod
    def create_unicolor_side(color):

        return Side([[color, color, color],
                     [color, color, color],
                     [color, color, color]])

    @staticmethod
    def create_copy(side):
        return Side([list(side.get_row(0)), list(side.get_row(1)), list(side.get_row(2))])

    def __init__(self, cubies):

        # todo get rid of these assertions
        isinstance(cubies, list)

        assert len(cubies) == 3
        for row in cubies: assert len(row) == 3

        self.cubies = cubies

    def __repr__(self):
        output = ""
        for r in self.cubies:
            for color in r:
                output += str(color) + " "
            output += "\n"

        return output

    def center_color(self):

        return self.cubies[1][1]

    def get_row(self, row_idx):

        return self.cubies[row_idx]

    def get_column(self, col_idx):

        column = []
        for i in range(3):
            column.append(self.cubies[i][col_idx])
        return column

    def __eq__(self, other):

        if len(self.cubies) != len(other.cubies): return False

        for c1, c2 in zip(self.cubies, other.cubies):
            if len(c1) != len(c2): return False;

            for color1, color2 in zip(c1, c2):
                if color1 != color2: return False

        return True
