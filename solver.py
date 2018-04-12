import unittest
from rubiks import *
import logging
import itertools


# self.cube is copied with the intent that no manipulation will
# occur to the cube after Solver takes control of it
class Solver(object):
    STAGE_UNKNOWN = -1
    STAGE_0 = 0
    STAGE_1 = 1
    STAGE_SOLVED = 100
    STAGES = [STAGE_UNKNOWN, STAGE_0, STAGE_1, STAGE_SOLVED]

    # Create Solver with copy of cube; once a cube is passed to Solver,
    # it is not intended to be modified by externally
    def __init__(self, cube):
        self.cube = cube.copy()
        self.current_stage = Solver.STAGE_0
        self.methods_to_move_any_face_to_top_list = {
            Cube.TOP: [[], []],
            Cube.BOTTOM: [[self.cube.rotate_cube_forward, self.cube.rotate_cube_forward],
                          [self.cube.rotate_cube_forward, self.cube.rotate_cube_forward]],
            Cube.FRONT: [[self.cube.rotate_cube_backward], [self.cube.rotate_cube_forward]],
            Cube.BACK: [[self.cube.rotate_cube_forward], [self.cube.rotate_cube_backward]],
            Cube.LEFT: [[self.cube.rotate_cube_right, self.cube.rotate_cube_backward],
                        [self.cube.rotate_cube_forward, self.cube.rotate_cube_left]],
            Cube.RIGHT: [[self.cube.rotate_cube_left, self.cube.rotate_cube_backward],
                         [self.cube.rotate_cube_forward, self.cube.rotate_cube_right]]}
        self.stage = self.__determine_stage()

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
        self.stage = self.__determine_stage()
        return self.stage

    def __determine_stage(self):
        if self.is_solved(): return Solver.STAGE_SOLVED
        if self.__is_stage_1(): return Solver.STAGE_1
        if not self.__is_stage_1(): return Solver.STAGE_0
        return Solver.STAGE_UNKNOWN

    def __is_stage_0(self):
        pass

    def __is_stage_1(self):
        # reset any stage_1 candidates
        self.stage_1_candidates = []

        # identify any faces that are candidates for having state_1 complete
        sides = self.__get_sides_mapped_by_name()
        candidates = []
        for side in sides.values():
            side_name = self.cube.get_side_name(side)
            logging.getLogger().debug("Checking %s to see if it has stage_1_part_1 solved", side_name)
            center_color = side.cubies[1][1]
            top_piece = side.cubies[0][1]
            right_piece = side.cubies[1][2]
            bottom_piece = side.cubies[2][1]
            left_piece = side.cubies[1][0]
            match = all(center_color == piece for piece in
                        [top_piece, right_piece, bottom_piece, left_piece])
            if match:
                candidates.append(side)
                logging.getLogger().debug("Side %s stage_1_part_1 solved", side_name)
            else:
                logging.getLogger().debug("Side %s stage_1_part_1 NOT solved", side_name)

        if len(candidates) == 0: return False

        # todo: consider flagging as part of the state of the solver the "top" that is the stage_1 solve
        for candidate_side in candidates:
            side_name = self.cube.get_side_name(candidate_side)
            method_list = self.methods_to_move_any_face_to_top_list[side_name]

            logging.getLogger().debug("Checking %s to see if it has stage_1_part_2 solved", side_name)

            moved = False
            for method_name in method_list[0]:
                if method_name is not None:
                    method_name()
                moved = True
            found = all(side.cubies[1][1] == side.cubies[0][1] for side in
                        [self.cube.back, self.cube.left, self.cube.front, self.cube.right])
            logging.getLogger().debug("Side %s stage_1_part_2 %s", side_name, "solved" if found else "unsolved")
            if moved:
                for method_name in method_list[1]:
                    method_name()
            if found: self.stage_1_candidates.append(side_name)

        return len(self.stage_1_candidates) > 0

