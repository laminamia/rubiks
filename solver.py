import unittest
from rubiks import *
import logging
import itertools

# self.cube is copied with the intent that no manipulation will
# occur to the cube after Solver takes control of it
class Solver(object):

    STATE_0 = 0
    STATE_1 = 1
    STATE_SOLVED = 100
    STATES = [STATE_0, STATE_1, STATE_SOLVED]

    def __init__(self, cube):
        self.cube = cube.copy()
        self.current_state = Solver.STATE_0

    def is_solved(self):
        for side in self.__get_sides():
            return all(side.get_center_color() == color for color in
                       [c for row in side.cubies for c in row])

    # return sides in no particular order
    # remember the sides change with cube rotation
    def __get_sides(self):
        return [self.cube.left, self.cube.right, self.cube.top,
                self.cube.bottom, self.cube.front, self.cube.back]

    def determine_state(self):
        if self.is_solved(): return Solver.STATE_SOLVED
        if not self.__is_state_1(): return Solver.STATE_0
        pass

    def __is_state_0(self):
        pass

    def __is_state_1(self):
        # identify any faces that are candidates for having state_1 complete
        for side in self.__get_sides():
            center_color = side.cubies[1][1]
            top_piece = side.cubies[0][1]
            right_piece = side.cubies[1][2]
            bottom_piece = side.cubies[2][1]
            left_piece = side.cubies[1][0]
            match = all(center_color == piece for piece in
                [top_piece, right_piece, bottom_piece, left_piece])
            if not match: return False
