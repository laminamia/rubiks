import unittest
from rubiks import *
import logging
import itertools


# self.cube is copied with the intent that no manipulation will
# occur to the cube after Solver takes control of it
class Solver(object):

    # Create Solver with copy of cube; once a cube is passed to Solver,
    # it is not intended to be modified by externally
    def __init__(self, cube):
        self.cube = cube.copy()
        self.current_stage = StageEvaluator.STAGE_0
        self.methods_to_move_any_face_back = {
            Cube.TOP: [],
            Cube.BOTTOM: [self.cube.rotate_cube_backward, self.cube.rotate_cube_backward],
            Cube.FRONT: [self.cube.rotate_cube_forward],
            Cube.BACK: [self.cube.rotate_cube_backward],
            Cube.LEFT: [self.cube.rotate_cube_forward, self.cube.rotate_cube_left],
            Cube.RIGHT: [self.cube.rotate_cube_forward, self.cube.rotate_cube_right]
        }
        self.__init_side_dict()
        self.stage = StageEvaluator(self.cube).determine_stage()

    def __init_side_dict(self):
        self.side_dict = {self.cube.top.cubies[1][1]: Cube.TOP,
                          self.cube.right.cubies[1][1]: Cube.RIGHT,
                          self.cube.left.cubies[1][1]: Cube.LEFT,
                          self.cube.bottom.cubies[1][1]: Cube.BOTTOM,
                          self.cube.front.cubies[1][1]: Cube.FRONT,
                          self.cube.back.cubies[1][1]: Cube.BACK}

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


class StageEvaluator(object):
    STAGE_UNKNOWN = -1
    STAGE_0 = 0
    STAGE_TOP_CROSS_SOLVED = 1
    STAGE_SOLVED = 100
    STAGES = [STAGE_UNKNOWN, STAGE_0, STAGE_TOP_CROSS_SOLVED, STAGE_SOLVED]

    def __init__(self, cube):
        self.cube = cube

    def determine_stage(self):
        self.stage = self.__determine_stage()
        return self.stage

    def is_solved(self):
        for side in self.cube.get_sides():
            return all(side.get_center_color() == color for color in
                       [c for row in side.cubies for c in row])

    def __determine_stage(self):
        if self.is_solved():
            return StageEvaluator.STAGE_SOLVED
        if self.__is_top_cross_solved():
            return StageEvaluator.STAGE_TOP_CROSS_SOLVED
        else:
            return StageEvaluator.STAGE_0

    def __is_stage_0(self):
        pass

    def __is_top_cross_solved(self):
        # reset any stage_1 candidates
        self.stage_1_candidates = []

        # identify any faces that are candidates for having state_1 complete
        sides = self.cube.get_sides()
        candidates = []
        for side in sides:
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

        if len(candidates) == 0:
            return False

        # todo: consider flagging as part of the state of the solver the "top" that is the stage_1 solve
        for candidate_side in candidates:
            color = candidate_side.center_color()
            side_name = self.cube.get_color_location(color)

            logging.getLogger().debug("Checking %s to see if it has stage_1_part_2 solved", side_name)

            self.cube.move_side_to_top(color)

            found = all(side.cubies[1][1] == side.cubies[0][1] for side in
                        [self.cube.back, self.cube.left, self.cube.front, self.cube.right])
            logging.getLogger().debug("Side %s stage_1_part_2 %s", side_name, "solved" if found else "unsolved")
            self.cube.move_top_to_side(side_name)
            if found: self.stage_1_candidates.append(side_name)

        return len(self.stage_1_candidates) > 0


class TopCrossSolver(object):

    def __init__(self, cube, top_color=WHITE):
        self.top_color = top_color
        self.cube = cube

    def solve(self):

        if StageEvaluator(self.cube).determine_stage() >= StageEvaluator.STAGE_TOP_CROSS_SOLVED:
            return True

        logging.getLogger().debug(
            "Moving " + str(self.top_color) + " to top from " + str(self.cube.get_color_location(self.top_color)))

        self.cube.move_side_to_top(self.top_color)

        # repeat until all top_colors on bottom are in place
        while self.solve_cross_pieces_on_bottom():
            pass

        # todo clean this up
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()
        self.cube.rotate_cube_right()
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()
        self.cube.rotate_cube_right()
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()
        self.cube.rotate_cube_right()
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()
        self.solve_cross_pieces_on_front()

        # repeat until all top_colors on bottom are in place
        while self.solve_cross_pieces_on_bottom():
            pass

        # todo: find corner piece and then move into place

    def solve_cross_pieces_on_bottom(self):
        bottom = self.cube.bottom

        candidates_and_manipulations = [(bottom.cubies[0][1], []),
                                        (bottom.cubies[1][0], [self.cube.rotate_bottom_right]),
                                        (bottom.cubies[1][2], [self.cube.rotate_bottom_left]),
                                        (bottom.cubies[2][1], [self.cube.rotate_bottom_right,
                                                               self.cube.rotate_bottom_right])]

        found = False
        for candidate_color, manipulations in candidates_and_manipulations:
            if candidate_color == self.top_color:
                found = True
                # move candidate to front
                for manipulation in manipulations:
                    manipulation()
                # move candidate to top in correct cross location
                adjacent_color = self.cube.front.cubies[2][1]
                for manipulation in self.__get_manipulation_to_move_cross_piece_on_bottom_at_front_to_top(
                        adjacent_color):
                    manipulation()

        return found

    def solve_cross_pieces_on_front(self):
        front = self.cube.front
        if front.cubies[0][1] == self.top_color:
            adjacent_color = self.cube.top.cubies[2][1]
            adjacent_color_location = self.cube.get_color_location(adjacent_color)
            assert adjacent_color_location != Cube.TOP and adjacent_color_location != Cube.BOTTOM
            manipulations_dict = {Cube.FRONT: [self.cube.rotate_front_cw, self.cube.rotate_right_forward,
                                               self.cube.rotate_bottom_left, self.cube.rotate_right_backward,
                                               self.cube.rotate_front_cw, self.cube.rotate_front_cw],
                                  Cube.LEFT: [self.cube.rotate_left_backward],
                                  Cube.RIGHT: [self.cube.rotate_front_cw, self.cube.rotate_right_backward,
                                               self.cube.rotate_front_ccw],
                                  Cube.BACK: [self.cube.rotate_front_cw, self.cube.rotate_front_cw,
                                              self.cube.rotate_bottom_right, self.cube.rotate_right_forward,
                                              self.cube.rotate_back_left, self.cube.rotate_right_backward]}
            manipulations = manipulations_dict[adjacent_color_location]
            for manipulation in manipulations:
                manipulation()
            return True

        if front.cubies[1][0] == self.top_color:
            adjacent_color = self.cube.left.cubies[1][2]
            adjacent_color_location = self.cube.get_color_location(adjacent_color)
            assert adjacent_color_location != Cube.TOP and adjacent_color_location != Cube.BOTTOM
            manipulations_dict = {Cube.FRONT: [self.cube.rotate_left_forward, self.cube.rotate_bottom_right,
                                               self.cube.rotate_front_cw, self.cube.rotate_front_cw,
                                               self.cube.rotate_left_backward],
                                  Cube.LEFT: [self.cube.rotate_left_backward],
                                  Cube.RIGHT: [self.cube.rotate_front_cw, self.cube.rotate_front_cw,
                                               self.cube.rotate_right_backward,
                                               self.cube.rotate_front_cw, self.cube.rotate_front_cw],
                                  Cube.BACK: [self.cube.rotate_left_forward, self.cube.rotate_bottom_left,
                                              self.cube.rotate_back_left, self.cube.rotate_back_left,
                                              self.cube.rotate_left_backward]}
            manipulations = manipulations_dict[adjacent_color_location]
            for manipulation in manipulations:
                manipulation()
            return True

        if front.cubies[1][2] == self.top_color:
            adjacent_color = self.cube.right.cubies[1][0]
            adjacent_color_location = self.cube.get_color_location(adjacent_color)
            assert adjacent_color_location != Cube.TOP and adjacent_color_location != Cube.BOTTOM
            manipulations_dict = {Cube.FRONT: [self.cube.rotate_right_forward, self.cube.rotate_bottom_left,
                                               self.cube.rotate_front_cw, self.cube.rotate_front_cw,
                                               self.cube.rotate_right_backward],
                                  Cube.LEFT: [self.cube.rotate_front_cw, self.cube.rotate_front_cw,
                                              self.cube.rotate_left_backward,
                                              self.cube.rotate_front_cw, self.cube.rotate_front_cw],
                                  Cube.RIGHT: [self.cube.rotate_right_backward],
                                  Cube.BACK: [self.cube.rotate_right_forward, self.cube.rotate_bottom_right,
                                              self.cube.rotate_back_left, self.cube.rotate_back_left,
                                              self.cube.rotate_right_backward]}
            manipulations = manipulations_dict[adjacent_color_location]
            for manipulation in manipulations:
                manipulation()
            return True

        if front.cubies[2][1] == self.top_color:
            adjacent_color = self.cube.right.cubies[1][0]
            adjacent_color_location = self.cube.get_color_location(adjacent_color)
            assert adjacent_color_location != Cube.TOP and adjacent_color_location != Cube.BOTTOM
            manipulations_dict = {Cube.FRONT: [self.cube.rotate_bottom_right, self.cube.rotate_right_backward,
                                               self.cube.rotate_front_ccw, self.cube.rotate_right_forward],
                                  Cube.LEFT: [self.cube.rotate_front_cw, self.cube.rotate_left_backward,
                                              self.cube.rotate_front_ccw],
                                  Cube.RIGHT: [self.cube.rotate_front_ccw, self.cube.rotate_right_backward,
                                               self.cube.rotate_front_cw],
                                  Cube.BACK: [self.cube.rotate_bottom_right, self.cube.rotate_right_forward,
                                              self.cube.rotate_back_left, self.cube.rotate_right_backward]}
            manipulations = manipulations_dict[adjacent_color_location]
            for manipulation in manipulations:
                manipulation()
            return True

        return False

    def __get_manipulation_to_move_cross_piece_on_bottom_at_front_to_top(self, candidate_color):
        return {self.cube.front.get_center_color(): [self.cube.rotate_front_cw, self.cube.rotate_front_cw],
                self.cube.left.get_center_color(): [self.cube.rotate_bottom_left, self.cube.rotate_left_forward,
                                                    self.cube.rotate_left_forward],
                self.cube.right.get_center_color(): [self.cube.rotate_bottom_right,
                                                     self.cube.rotate_right_forward,
                                                     self.cube.rotate_right_forward],
                self.cube.back.get_center_color(): [self.cube.rotate_bottom_right, self.cube.rotate_bottom_right,
                                                    self.cube.rotate_back_left, self.cube.rotate_back_left]
                }[candidate_color]
