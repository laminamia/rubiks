from colorama import Back, Style, Fore


class Color(object):

    def __init__(self, n, char, colorcode):

        self.n = n
        self.char = char
        self.colorcode = colorcode

    def opposite(self):

        return OPPOSITES.get(self)

    def __repr__(self):

        return Style.BRIGHT + Fore.BLACK + self.colorcode + self.char + Style.RESET_ALL


RED = Color(1, "R", Back.RED)
YELLOW = Color(2, "Y", Back.LIGHTYELLOW_EX)
GREEN = Color(3, "G", Back.GREEN)
BLUE = Color(4, "B", Back.BLUE)
ORANGE = Color(5, "O", Back.LIGHTRED_EX)
WHITE = Color(6, "W", Back.WHITE)
COLORS = [RED, YELLOW, GREEN, BLUE, ORANGE, WHITE]
OPPOSITES = {RED: ORANGE, ORANGE: RED, YELLOW: WHITE, WHITE: YELLOW, BLUE: GREEN, GREEN: BLUE}


class Cube(object):

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


class Side(object):

    @staticmethod
    def create_unicolor_side(color):

        return Side([[color, color, color],
                     [color, color, color],
                     [color, color, color]])

    def __init__(self, cubies):

        isinstance(cubies, list)

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
