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

        _right_first_column = []

        # save right first column
        for i in [0, 1, 2]: _right_first_column.append(self.right.cubies[i][0])

        # fix right
        # top side last row is adjacent to front side
        # swap each item in top last row to first item of each row of right side
        for i in [0, 1, 2]: self.right.cubies[i][0] = self.top.cubies[2][i]

        # fix top
        # top side last row is adjacent to front top row
        # left side each item in last column should become last row of top side
        for i in [0, 1, 2]: self.top.cubies[2][i] = self.left.cubies[i][2]

        # fix left
        # bottom side first row is adjacent to front last row
        # swap each item in bottom first row to last item of each row of left side
        for i in [0, 1, 2]: self.left.cubies[i][2] = self.bottom.cubies[2][i]

        # fix bottom
        # right side first column is adjacent to front
        # swap each item in right first column to first row of bottom
        for i in [0, 1, 2]: self.bottom.cubies[0][i] = _right_first_column[i]


class Side(object):

    @staticmethod
    def create_unicolor_side(color):

        return Side([[color, color, color],
                     [color, color, color],
                     [color, color, color]])

    def __init__(self, cubies):

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

    def __eq__(self, other):

        if len(self.cubies) != len(other.cubies): return False

        for c1, c2 in zip(self.cubies, other.cubies):
            if len(c1) != len(c2): return False;

            for color1, color2 in zip(c1, c2):
                if color1 != color2: return False

        return True
