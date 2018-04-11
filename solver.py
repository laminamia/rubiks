import unittest
from rubiks import *
import logging
import itertools


# self.cube is copied with the intent that no manipulation will
# occur to the cube after Solver takes control of it
class Solver(object):
    STAGE_0 = 0
    STAGE_1 = 1
    STAGE_SOLVED = 100
    STAGES = [STAGE_0, STAGE_1, STAGE_SOLVED]

    def __init__(self, cube):
        self.cube = cube.copy()
        self.current_stage = Solver.STAGE_0

    def is_solved(self):
        for side in self.__get_sides():
            return all(side.get_center_color() == color for color in
                       [c for row in side.cubies for c in row])

    def __get_sides(self):
        return [self.cube.left, self.cube.right, self.cube.top,
                self.cube.bottom, self.cube.front, self.cube.back]

    # return sides in dict mapped by name of side
    # remember the sides change with cube rotation
    def __get_sides_mapped_by_name(self):
        return {"left": self.cube.left, "right": self.cube.right, "top": self.cube.top,
                "bottom": self.cube.bottom, "front": self.cube.front, "back": self.cube.back}

    def __get_sides_mapped_to_adjacent_sides(self):
        return {"front": (self.cube.front, (self.cube.top, self.cube.right, self.cube.bottom, self.cube.left)),
                "top": (self.cube.top, (self.cube.back, self.cube.right, self.cube.left, self.cube.front)),
                "left": (self.cube.left, (self.cube.top, self.cube.front, self.cube.back, self.cube.bottom)),
                "right": (self.cube.right, (self.cube.top, self.cube.back, self.cube.front, self.cube.bottom)),
                "back": (self.cube.back, (self.cube.top, self.cube.left, self.cube.bottom, self.cube.right)),
                "bottom": (self.cube.bottom, (self.cube.front, self.cube.right, self.cube.back, self.cube.left))}

    def determine_stage(self):
        if self.is_solved(): return Solver.STAGE_SOLVED
        if self.__is_stage_1(): return Solver.STAGE_1
        if not self.__is_stage_1(): return Solver.STAGE_0
        pass

    def __is_stage_0(self):
        pass

    def __is_stage_1(self):
        # identify any faces that are candidates for having state_1 complete
        sides = self.__get_sides_mapped_by_name()
        candidates = []
        for side in sides.values():
            center_color = side.cubies[1][1]
            top_piece = side.cubies[0][1]
            right_piece = side.cubies[1][2]
            bottom_piece = side.cubies[2][1]
            left_piece = side.cubies[1][0]
            match = all(center_color == piece for piece in
                        [top_piece, right_piece, bottom_piece, left_piece])
            if match:
                candidates.append(side)

        if len(candidates) == 0: return False

        methods = {
            Cube.TOP: self.__check_top_for_stage_1_part_2,
            #  Cube.BOTTOM: __check_bottom_for_stage_1_part_2,
            Cube.FRONT: self.__check_front_for_stage_1_part_2,
            #  Cube.BACK: __check_back_for_stage_1_part_2,
            Cube.LEFT: self.__check_left_for_stage_1_part_2,
            #  Cube.RIGHT: __check_right_for_stage_1_part_2
        }

        # todo: consider flagging as part of the state of the solver the "top" that is the stage_1 solve
        for candidate_side in candidates:
            side_name = self.cube.get_side_name(candidate_side)
            method = methods[side_name]
            logging.getLogger().debug("Checking %s, which has cross, to see if stage_1_part_2 is solved")
            if method(): return True;

        return False

    def __check_top_for_stage_1_part_2(self):
        return all(side.cubies[1][1] == side.cubies[0][1] for side in
                   [self.cube.back, self.cube.left, self.cube.front, self.cube.right])

    def __check_front_for_stage_1_part_2(self):
        return all(side.cubies[1][1] == side.cubies[coordinate_tuple[0]][coordinate_tuple[1]]
                   for (side, coordinate_tuple) in
                   [(self.cube.top, (2, 1)), (self.cube.bottom, (0, 1)),
                    (self.cube.left, (1, 2)), (self.cube.right, (1, 0))])

    def __check_left_for_stage_1_part_2(self):
        return all(side.cubies[1][1] == side.cubies[coordinate_tuple[0]][coordinate_tuple[1]]
                   for (side, coordinate_tuple) in
                   [(self.cube.back, (2, 1)), (self.cube.front, (0, 1)),
                    (self.cube.top, (1, 2)), (self.cube.bottom, (1, 0))])
