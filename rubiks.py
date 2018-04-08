from colorama import *
import regex


class Color(object):
    are_colors_on = False

    @staticmethod
    def initialize(are_colors_on=False):
        Color.are_colors_on = are_colors_on

    def __init__(self, char, color_code):
        self.char = char
        self.color_code = color_code

    def opposite(self):
        return OPPOSITES.get(self)

    def __repr__(self):
        if Color.are_colors_on:
            return Style.BRIGHT + self.color_code + self.char + Style.RESET_ALL
        return self.char
        # return Style.BRIGHT + Fore.WHITE + self.colorcode + self.char + Style.RESET_ALL

    def __eq__(self, other):
        return self.char == other.char

    def __hash__(self):
        return self.char.__hash__()


RED = Color("R", Fore.RED)
YELLOW = Color("Y", Fore.LIGHTYELLOW_EX)
GREEN = Color("G", Fore.GREEN)
BLUE = Color("B", Fore.BLUE)
ORANGE = Color("O", Fore.LIGHTRED_EX)
WHITE = Color("W", Fore.WHITE)
COLORS = [RED, YELLOW, GREEN, BLUE, ORANGE, WHITE]
OPPOSITES = {RED: ORANGE, ORANGE: RED, YELLOW: WHITE, WHITE: YELLOW, BLUE: GREEN, GREEN: BLUE}
COLORS_BY_CHAR = {color.char: color for color in COLORS}


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

    @staticmethod
    def from_string(s=""):
        pass

    def __init__(self, front, back, left, right, top, bottom):
        self.front = front
        self.back = back
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def rotate_cube_backward(self, num_times=1):
        for i in range(num_times % 4):
            _temp = self.back
            self.back = self.top.create_inverse()
            self.top = self.front
            self.front = self.bottom
            self.bottom = _temp.create_inverse()
            self.left.rotate_face_colors_ccw()
            self.right.rotate_face_colors_cw()

    def rotate_cube_forward(self, num_times=1):
        for i in range(num_times % 4):
            _temp = self.front
            self.front = self.top
            self.top = self.back.create_inverse()
            self.back = self.bottom.create_inverse()
            self.bottom = _temp
            self.left.rotate_face_colors_cw()
            self.right.rotate_face_colors_ccw()

    def rotate_cube_right(self, num_times=1):
        for i in range(num_times % 4):
            _temp = self.front
            self.front = self.left
            self.left = self.back
            self.back = self.right
            self.right = _temp
            self.top.rotate_face_colors_ccw()
            self.bottom.rotate_face_colors_cw()

    def rotate_cube_left(self, num_times=1):
        n = num_times % 4
        if n == 0:
            return
        elif n == 1:
            self.rotate_cube_right(3)
        elif n == 2:
            self.rotate_cube_right(2)
        elif n == 3:
            self.rotate_cube_right(1)
        else:
            return

    def rotate_front_cw(self):
        # rotate pieces that change on other faces
        for i in [0, 1, 2]:
            # save right before it is rewritten
            _right = self.right.cubies[i][0]

            # fix right: top last row -> right first column
            self.right.cubies[i][0] = self.top.cubies[2][i]

            # fix top: left last column -> top last row
            # (in reverse order - will reverse below)
            # (if we try to reverse here, we overwrite values that still need to be assigned)
            self.top.cubies[2][i] = self.left.cubies[i][2]

            # fix left: bottom first row -> left last column
            self.left.cubies[i][2] = self.bottom.cubies[0][i]

            # fix bottom: right first column -> top first row
            # (in reverse order - will reverse below)
            # (if we try to reverse here, we overwrite values that still need to be assigned)
            self.bottom.cubies[0][i] = _right

        # need to swap first and last in left last column and right first column
        self.top.cubies[2][0], self.top.cubies[2][2] = self.top.cubies[2][2], self.top.cubies[2][0]
        self.bottom.cubies[0][0], self.bottom.cubies[0][2] = self.bottom.cubies[0][2], self.bottom.cubies[0][0]

        self.front.rotate_face_colors_cw()

    def rotate_front_ccw(self):

        # rotate pieces that change on other faces
        for i in [0, 1, 2]:
            # save right before it is rewritten
            _temp = self.right.cubies[i][0]

            # fix right: bottom first row -> right first column
            # (in reverse order - will reverse below)
            # (if we try to reverse here, we overwrite values that still need to be assigned)
            self.right.cubies[i][0] = self.bottom.cubies[0][i]

            # fix bottom: left last column -> bottom first row
            self.bottom.cubies[0][i] = self.left.cubies[i][2]

            # fix left: top last row -> left last column
            # (in reverse order - will reverse below)
            # (if we try to reverse here, we overwrite values that still need to be assigned)
            self.left.cubies[i][2] = self.top.cubies[2][i]

            # fix top: right first column -> top last row
            self.top.cubies[2][i] = _temp

        # need to swap first and last in left last column and right first column
        self.right.cubies[0][0], self.right.cubies[2][0] = self.right.cubies[2][0], self.right.cubies[0][0]
        self.left.cubies[2][2], self.left.cubies[0][2] = self.left.cubies[0][2], self.left.cubies[2][2]

        self.front.rotate_face_colors_ccw()

    # less efficient but can implement natively later
    def rotate_top_left(self):
        self.rotate_cube_forward()
        self.rotate_front_cw()
        self.rotate_cube_backward()

    # less efficient but can implement natively later
    def rotate_top_right(self):
        self.rotate_cube_forward()
        self.rotate_front_ccw()
        self.rotate_cube_backward()

    # less efficient but can implement natively later
    def rotate_bottom_left(self):
        self.rotate_cube_backward()
        self.rotate_front_ccw()
        self.rotate_cube_forward()

    # less efficient but can implement natively later
    def rotate_bottom_right(self):
        self.rotate_cube_backward()
        self.rotate_front_cw()
        self.rotate_cube_forward()

    # less efficient but can implement natively later
    def rotate_left_forward(self):
        self.rotate_cube_right()
        self.rotate_front_cw()
        self.rotate_cube_left()

    # less efficient but can implement natively later
    def rotate_left_backward(self):
        self.rotate_cube_right()
        self.rotate_front_ccw()
        self.rotate_cube_left()

    # less efficient but can implement natively later
    def rotate_right_forward(self):
        self.rotate_cube_left()
        self.rotate_front_ccw()
        self.rotate_cube_right()

    # less efficient but can implement natively later
    def rotate_right_backward(self):
        self.rotate_cube_left()
        self.rotate_front_cw()
        self.rotate_cube_right()

    # less efficient but can implement natively later
    def rotate_back_right(self):
        self.rotate_cube_forward(2)
        self.rotate_front_ccw()
        self.rotate_cube_backward(2)

    # less efficient but can implement natively later
    def rotate_back_left(self):
        self.rotate_cube_forward(2)
        self.rotate_front_cw()
        self.rotate_cube_backward(2)

    # less efficient but can implement natively later
    def rotate_right_backward(self):
        self.rotate_cube_left()
        self.rotate_front_cw()
        self.rotate_cube_right()

    def __repr__(self):
        s = ""
        for i in range(3):
            s += "    %s%s%s\n" % tuple(self.top.get_row(i))
        for i in range(3):
            s += "%s%s%s " % tuple(self.left.get_row(i))
            s += "%s%s%s " % tuple(self.front.get_row(i))
            s += "%s%s%s " % tuple(self.right.get_row(i))
            s += "%s%s%s\n" % tuple(self.back.get_row(i))
        for i in range(3):
            s += "    %s%s%s\n" % tuple(self.bottom.get_row(i))
        return s


class Side(object):

    # todo Consider using numpy arrays instead

    @staticmethod
    def create_unicolor_side(color):

        return Side([[color, color, color],
                     [color, color, color],
                     [color, color, color]])

    @staticmethod
    def create_from_side(side):
        return Side([list(side.get_row(0)), list(side.get_row(1)), list(side.get_row(2))])

    def copy(self):
        return Side.create_from_side(self)

    def create_inverse(self):
        rows = []
        for i in range(3):
            r = list(self.get_row(2 - i))
            r.reverse()
            rows.append(r)
        return Side(rows)

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

    def rotate_face_colors_ccw(self):
        # rotate turned face pieces - middles
        # save right middle
        _temp = self.cubies[1][2]
        # bottom middle to right middle
        self.cubies[1][2] = self.cubies[2][1]
        # left middle to bottom middle
        self.cubies[2][1] = self.cubies[1][0]
        # top middle to left middle
        self.cubies[1][0] = self.cubies[0][1]
        # right middle to top middle
        self.cubies[0][1] = _temp

        # rotate turned face pieces - corners
        # save top right
        _temp = self.cubies[0][2]
        # bottom right to top right
        self.cubies[0][2] = self.cubies[2][2]
        # bottom left to bottom right
        self.cubies[2][2] = self.cubies[2][0]
        # top left to bottom left
        self.cubies[2][0] = self.cubies[0][0]
        # top right to top left
        self.cubies[0][0] = _temp

        return self

    def rotate_face_colors_cw(self):
        # rotate turned face pieces - middles
        # save right middle
        _temp = self.cubies[1][2]
        # top middle to right middle
        self.cubies[1][2] = self.cubies[0][1]
        # left middle to top middle
        self.cubies[0][1] = self.cubies[1][0]
        # bottom middle to left middle
        self.cubies[1][0] = self.cubies[2][1]
        # right middle to bottom middle
        self.cubies[2][1] = _temp

        # rotate turned face pieces - corners
        # save top right
        _temp = self.cubies[0][2]
        # top left to top right
        self.cubies[0][2] = self.cubies[0][0]
        # bottom left to top left
        self.cubies[0][0] = self.cubies[2][0]
        # bottom right to bottom left
        self.cubies[2][0] = self.cubies[2][2]
        # top right to bottom right
        self.cubies[2][2] = _temp

        return self

    def __eq__(self, other):

        if len(self.cubies) != len(other.cubies):
            return False

        for c1, c2 in zip(self.cubies, other.cubies):
            if len(c1) != len(c2):
                return False;

            for color1, color2 in zip(c1, c2):
                if color1 != color2:
                    return False

        return True


class Parser(object):

    def __init__(self):
        self.expr = regex.compile("^(\s*[yrbgwo]{3}[ \t]*\n+){3}\s*" +
                                  "((\s*[yrbgwo]{3}[ \t]*){4}\n+){3}" +
                                  "(\s*[yrbgwo]{3}[ \t]*\n+){3}\s*$", regex.IGNORECASE)

    def is_string_valid(self, cube_string):
        cube_string += "\n"
        match = self.expr.match(cube_string)
        return match is not None
