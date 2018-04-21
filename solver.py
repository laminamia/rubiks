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
        self.stage = StageEvaluator(self.cube).determine_stage()


class StageEvaluator(object):
    STAGE_0 = 0
    STAGE_TOP_CROSS_SOLVED = 1
    STAGE_TOP_SOLVED = 2
    STAGE_SOLVED = 100
    STAGES = [STAGE_0, STAGE_TOP_CROSS_SOLVED, STAGE_SOLVED]

    def __init__(self, cube):
        self.cube = cube
        self.stage = self.STAGE_0

    def determine_stage(self):
        self.stage = self.__determine_stage()
        return self.stage

    def is_solved(self):
        solved = True
        for side in self.cube.get_sides():
            colors = [c for row in side.cubies for c in row]
            solved = solved and all(side.get_center_color() == color for color in colors)
        return solved

    def __determine_stage(self):
        if self.is_solved():
            return StageEvaluator.STAGE_SOLVED

        if not self.__is_top_cross_solved():
            return StageEvaluator.STAGE_0

        if not self.__is_top_solved():
            return StageEvaluator.STAGE_TOP_CROSS_SOLVED

        return StageEvaluator.STAGE_TOP_SOLVED

    def __is_top_cross_solved(self):
        # reset any stage candidates
        self.top_cross_candidates = []

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

        for candidate_side in candidates:
            color = candidate_side.get_center_color()
            side_name = self.cube.get_color_location(color)

            logging.getLogger().debug("Checking %s to see if it has stage_top_cross_solved is solved", side_name)

            self.cube.move_side_to_top(color)

            found = all(side.cubies[1][1] == side.cubies[0][1] for side in
                        [self.cube.back, self.cube.left, self.cube.front, self.cube.right])
            logging.getLogger().debug("Side %s stage_1_part_2 %s", side_name, "solved" if found else "unsolved")
            self.cube.move_top_to_side(side_name)

            if found:
                self.top_cross_candidates.append(side_name)

        return len(self.top_cross_candidates) > 0

    def __is_top_solved(self):
        if len(self.top_cross_candidates) == 0:
            return False

        # reset any stage candidates
        self.top_solved_candidates = []

        for side_name in self.top_cross_candidates:
            candidate_side = self.cube.get_side_by_name(side_name)
            center_color = candidate_side.get_center_color()
            self.cube.move_side_to_top(center_color)

            logging.getLogger().debug("Checking %s to see if it has stage_top_solved is solved", side_name)

            if not all(center_color == corner_color for corner_color in
                       [self.cube.top.cubies[0][0], self.cube.top.cubies[0][2],
                        self.cube.top.cubies[2][0], self.cube.top.cubies[2][2]]):
                # go to next candidate; this one was a loss
                continue

            found = all(side.cubies[0][0] == side.get_center_color() and
                        side.cubies[0][2] == side.get_center_color() for side in
                        [self.cube.back, self.cube.front, self.cube.left, self.cube.right])
            logging.getLogger().debug("Side %s stage_top_solved %s", side_name, "solved" if found else "unsolved")
            self.cube.move_top_to_side(side_name)

            if found:
                self.top_solved_candidates.append(side_name)

        return len(self.top_solved_candidates) > 0


class TopSolver(object):

    def __init__(self, cube, top_color=WHITE):
        self.cube = cube
        self.top_color = top_color
        self.cube.move_side_to_top(self.top_color)
        self.sub_solver = TopCrossSolver(self.cube, self.top_color)
        assert self.sub_solver.is_done(), "Top cross not solved"

    def is_done(self):
        self.cube.move_side_to_top(self.top_color)
        top = self.cube.top
        top_corners_complete = all(top.get_center_color() == color for color in
                                   [top.cubies[0][0], top.cubies[0][2], top.cubies[2][0], top.cubies[2][2]])
        if not top_corners_complete:
            return False

        return all(side.get_center_color() == side.cubies[0][0] and side.get_center_color() == side.cubies[0][2]
                   for side in [self.cube.front, self.cube.left, self.cube.right, self.cube.back])

    def solve(self):
        # while not self.is_done():
        while self.solve_corners_on_bottom():
            pass

    def solve_corners_on_bottom(self):
        candidates_and_adjacent_sides = [(self.cube.bottom.cubies[0][0], (Cube.LEFT, Cube.FRONT)),
                                         (self.cube.bottom.cubies[0][2], (Cube.FRONT, Cube.RIGHT)),
                                         (self.cube.bottom.cubies[2][0], (Cube.BACK, Cube.LEFT)),
                                         (self.cube.bottom.cubies[2][2], (Cube.RIGHT, Cube.BACK))]
        for candidate, adjacent_sides in candidates_and_adjacent_sides:
            if candidate != self.top_color:
                continue

            # get the sides that are currently adjacent to the candidate corner
            leftish_adj_side_name = adjacent_sides[0]
            rightish_adj_side_name = adjacent_sides[1]
            leftish_adj_side = self.cube.get_side_by_name(leftish_adj_side_name)
            rightish_adj_side = self.cube.get_side_by_name(rightish_adj_side_name)

            # get the colors that are adjacent to the candidate corner
            leftish_adj_color = leftish_adj_side.cubies[2][2]
            rightish_adj_color = rightish_adj_side.cubies[2][0]

            # get the sides that have the corner colors that match the candidate corner
            leftish_color_side = self.cube.get_side_by_color(leftish_adj_color)
            rightish_color_side = self.cube.get_side_by_color(rightish_adj_color)

            # get the destination names of the rightish_color and leftish_color sides
            # so that we know the name of the side where the corner cube is to be moved
            leftish_color_side_name = self.cube.get_side_name(leftish_color_side)
            rightish_color_side_name = self.cube.get_side_name(rightish_color_side)

            # corner not at location of sides of same center colors
            if {leftish_adj_side_name, rightish_adj_side_name} != {leftish_color_side_name, rightish_color_side_name}:
                sides_to_manipulations = {(frozenset({Cube.LEFT, Cube.FRONT}), frozenset({Cube.FRONT, Cube.RIGHT})):
                                              [self.cube.rotate_bottom_right],
                                          (frozenset({Cube.LEFT, Cube.FRONT}), frozenset({Cube.RIGHT, Cube.BACK})):
                                              [self.cube.rotate_bottom_right, self.cube.rotate_bottom_right],
                                          (frozenset({Cube.LEFT, Cube.FRONT}), frozenset({Cube.BACK, Cube.LEFT})):
                                              [self.cube.rotate_bottom_left],
                                          (frozenset({Cube.FRONT, Cube.RIGHT}), frozenset({Cube.RIGHT, Cube.BACK})):
                                              [self.cube.rotate_bottom_right],
                                          (frozenset({Cube.FRONT, Cube.RIGHT}), frozenset({Cube.BACK, Cube.LEFT})):
                                              [self.cube.rotate_bottom_right, self.cube.rotate_bottom_right],
                                          (frozenset({Cube.FRONT, Cube.RIGHT}), frozenset({Cube.LEFT, Cube.FRONT})):
                                              [self.cube.rotate_bottom_left],
                                          (frozenset({Cube.RIGHT, Cube.BACK}), frozenset({Cube.BACK, Cube.LEFT})):
                                              [self.cube.rotate_bottom_right],
                                          (frozenset({Cube.RIGHT, Cube.BACK}), frozenset({Cube.LEFT, Cube.FRONT})):
                                              [self.cube.rotate_bottom_right, self.cube.rotate_bottom_right],
                                          (frozenset({Cube.RIGHT, Cube.BACK}), frozenset({Cube.FRONT, Cube.RIGHT})):
                                              [self.cube.rotate_bottom_left],
                                          (frozenset({Cube.BACK, Cube.LEFT}), frozenset({Cube.LEFT, Cube.FRONT})):
                                              [self.cube.rotate_bottom_right],
                                          (frozenset({Cube.BACK, Cube.LEFT}), frozenset({Cube.FRONT, Cube.RIGHT})):
                                              [self.cube.rotate_bottom_right, self.cube.rotate_bottom_right],
                                          (frozenset({Cube.BACK, Cube.LEFT}), frozenset({Cube.RIGHT, Cube.BACK})):
                                              [self.cube.rotate_bottom_left],
                                          }
                key = (frozenset({leftish_adj_side_name, rightish_adj_side_name}),
                       frozenset({leftish_color_side_name, rightish_color_side_name}))

                manipulations = sides_to_manipulations[key]
                # rotate bottom so that corner is between two sides with relevant colors,
                # and top_color part of corner remains on the bottom
                for manipulation in manipulations:
                    manipulation()

            # now rotate cube so that corner is at front-left
            manipulation_dict = {frozenset({Cube.FRONT, Cube.LEFT}): [],
                                 frozenset({Cube.LEFT, Cube.BACK}):
                                     [self.cube.rotate_cube_left],
                                 frozenset({Cube.BACK, Cube.RIGHT}):
                                     [self.cube.rotate_cube_left, self.cube.rotate_cube_left],
                                 frozenset({Cube.RIGHT, Cube.FRONT}):
                                     [self.cube.rotate_cube_right]}
            key = frozenset({leftish_color_side_name, rightish_color_side_name})

            manipulations = manipulation_dict[key]
            for manipulation in manipulations:
                manipulation()

            # now move corner to top position
            self.cube.rotate_bottom_right()
            self.cube.rotate_left_forward()
            self.cube.rotate_bottom_left()
            self.cube.rotate_left_backward()
            self.cube.rotate_front_ccw()
            self.cube.rotate_bottom_left()
            self.cube.rotate_front_cw()
            self.cube.rotate_bottom_right()
            self.cube.rotate_bottom_right()
            self.cube.rotate_left_forward()
            self.cube.rotate_bottom_left()
            self.cube.rotate_left_backward()

            # skip checking remaining candidates as they
            # may have moved; return found = True
            return True

        return False


class TopCrossSolver(object):

    def __init__(self, cube, top_color=WHITE):
        self.top_color = top_color
        self.cube = cube
        self.cube.move_side_to_top(self.top_color)

    def is_done(self):
        self.cube.move_side_to_top(self.top_color)
        top = self.cube.top
        top_cross_complete = all(top.get_center_color() == color for color in
                                 [top.cubies[0][1], top.cubies[1][0], top.cubies[1][2], top.cubies[2][1]])
        return top_cross_complete and all(side.get_center_color() == side.cubies[0][1]
                                          for side in [self.cube.front, self.cube.left,
                                                       self.cube.right, self.cube.back])

    def solve(self):

        if StageEvaluator(self.cube).determine_stage() >= StageEvaluator.STAGE_TOP_CROSS_SOLVED:
            return True

        logging.getLogger().debug(
            "Moving " + str(self.top_color) + " to top from " + str(self.cube.get_color_location(self.top_color)))

        self.cube.move_side_to_top(self.top_color)

        # repeat until all top_colors on bottom are in place
        while not self.is_done():
            # check bottom
            while self.solve_cross_pieces_on_bottom():
                pass

            # check top
            while self.solve_cross_pieces_on_top():
                pass

            # check front
            while self.solve_cross_pieces_on_front():
                pass

            # check left
            self.cube.rotate_cube_right()
            while self.solve_cross_pieces_on_front():
                pass

            # check back
            self.cube.rotate_cube_right()
            while self.solve_cross_pieces_on_front():
                pass

            # check right
            self.cube.rotate_cube_right()
            while self.solve_cross_pieces_on_front():
                pass

    def solve_cross_pieces_on_top(self):
        found = False

        top = self.cube.top
        candidate_and_adjacent_side = [(top.cubies[0][1], Cube.BACK),
                                       (top.cubies[1][0], Cube.LEFT),
                                       (top.cubies[1][2], Cube.RIGHT),
                                       (top.cubies[2][1], Cube.FRONT)]

        for candidate_color, adjacent_side in candidate_and_adjacent_side:
            if candidate_color == self.top_color:
                # get side object that is adjacent to candidate
                side = self.cube.get_side_by_name(adjacent_side)
                # check to see if candidate already is in the correct position
                adjacent_color = side.cubies[0][1]

                # if in correct position, move on to next candidate
                if adjacent_color == side.get_center_color():
                    continue

                found = True

                # not in correct position, so move candidate to bottom
                manipulations = {Cube.BACK: [self.cube.rotate_back_left, self.cube.rotate_cube_left],
                                 Cube.LEFT: [self.cube.rotate_left_forward, self.cube.rotate_left_forward],
                                 Cube.RIGHT: [self.cube.rotate_right_forward, self.cube.rotate_right_forward],
                                 Cube.FRONT: [self.cube.rotate_front_cw, self.cube.rotate_front_cw]}[adjacent_side]
                for manipulation in manipulations:
                    manipulation()

                # move candidate to correct bottom position and then to top
                destination_side = self.cube.get_color_location(adjacent_color)
                self.solve_bottom(adjacent_side, destination_side)

                # end after a single manipulation solution because otherwise
                # the candidate information is now out of date
                break

        return found

    def solve_cross_pieces_on_bottom(self):
        bottom = self.cube.bottom

        candidate_and_adjacent_side = [(bottom.cubies[0][1], Cube.FRONT),
                                       (bottom.cubies[1][0], Cube.LEFT),
                                       (bottom.cubies[1][2], Cube.RIGHT),
                                       (bottom.cubies[2][1], Cube.BACK)]

        found = False
        for candidate_color, adjacent_side in candidate_and_adjacent_side:
            if candidate_color == self.top_color:
                found = True
                # move candidate to correct position and then to top
                adjacent_color = self.cube.get_side_by_name(adjacent_side).cubies[2][1]
                destination_side = self.cube.get_color_location(adjacent_color)

                self.solve_bottom(adjacent_side, destination_side)

        return found

    def solve_bottom(self, adjacent_side, destination_side):
        # rotate bottom so that candidate is lined up with correct color
        if adjacent_side != destination_side:
            manipulations_map = {(Cube.FRONT, Cube.LEFT): [self.cube.rotate_bottom_left],
                                 (Cube.FRONT, Cube.RIGHT): [self.cube.rotate_bottom_right],
                                 (Cube.FRONT, Cube.BACK): [self.cube.rotate_bottom_left,
                                                           self.cube.rotate_bottom_left],
                                 (Cube.LEFT, Cube.FRONT): [self.cube.rotate_bottom_right],
                                 (Cube.LEFT, Cube.RIGHT): [self.cube.rotate_bottom_right,
                                                           self.cube.rotate_bottom_right],
                                 (Cube.LEFT, Cube.BACK): [self.cube.rotate_bottom_left],
                                 (Cube.RIGHT, Cube.FRONT): [self.cube.rotate_bottom_left],
                                 (Cube.RIGHT, Cube.LEFT): [self.cube.rotate_bottom_left,
                                                           self.cube.rotate_bottom_left],
                                 (Cube.RIGHT, Cube.BACK): [self.cube.rotate_bottom_right],
                                 (Cube.BACK, Cube.FRONT): [self.cube.rotate_bottom_left,
                                                           self.cube.rotate_bottom_left],
                                 (Cube.BACK, Cube.LEFT): [self.cube.rotate_bottom_right],
                                 (Cube.BACK, Cube.RIGHT): [self.cube.rotate_bottom_left]}

            manipulations = manipulations_map[(adjacent_side, destination_side)]
            for manipulation in manipulations:
                manipulation()

        # rotate side so that candidate is now on top
        manipulations = {Cube.FRONT: [self.cube.rotate_front_cw, self.cube.rotate_front_cw],
                         Cube.LEFT: [self.cube.rotate_left_forward, self.cube.rotate_left_forward],
                         Cube.RIGHT: [self.cube.rotate_right_forward, self.cube.rotate_right_forward],
                         Cube.BACK: [self.cube.rotate_back_left, self.cube.rotate_back_left]}[destination_side]
        for manipulation in manipulations:
            manipulation()

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
            adjacent_color = self.cube.bottom.cubies[0][1]
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
