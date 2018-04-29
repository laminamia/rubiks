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
            Cube.LEFT: [self.cube.rotate_cube_forward, self.cube.rotate_cube_cw],
            Cube.RIGHT: [self.cube.rotate_cube_forward, self.cube.rotate_cube_ccw]
        }
        self.stage = StageEvaluator(self.cube).determine_stage()


class TopCornerSolver(object):

    def __init__(self, cube, top_color=WHITE):
        self.cube = cube
        self.top_color = top_color
        self.cube.move_side_to_top(self.top_color)
        self.sub_solver = TopCrossSolver(self.cube, self.top_color)
        assert self.sub_solver.is_done(), "Top cross not solved"

    def is_done(self):
        return self.count_completed_corners() == 4

    def count_completed_corners(self):
        return sum(self.top_color == top_corner and adj1 == adj1_center and adj2 == adj2_center
                   for top_corner, adj1, adj1_center, adj2, adj2_center in
                   [(self.cube.top.cubies[0][0],
                     self.cube.back.cubies[0][2], self.cube.back.get_center_color(),
                     self.cube.left.cubies[0][0], self.cube.left.get_center_color()),
                    (self.cube.top.cubies[0][2],
                     self.cube.back.cubies[0][0], self.cube.back.get_center_color(),
                     self.cube.right.cubies[0][2], self.cube.right.get_center_color()),
                    (self.cube.top.cubies[2][0],
                     self.cube.front.cubies[0][0], self.cube.front.get_center_color(),
                     self.cube.left.cubies[0][2], self.cube.left.get_center_color()),
                    (self.cube.top.cubies[2][2],
                     self.cube.front.cubies[0][2], self.cube.front.get_center_color(),
                     self.cube.right.cubies[0][0], self.cube.right.get_center_color())])

    def solve(self):
        while not self.is_done():
            side_name, candidate_coords = self.find_candidate()

            assert side_name in Cube.SIDE_NAMES

            if side_name == Cube.TOP:
                self.solve_corner_on_top(candidate_coords)
                continue

            if side_name == Cube.BOTTOM:
                self.solve_corners_on_bottom(candidate_coords)
                continue

            # if one of the face sides but not front, rotate cube
            # so that side is in front (maintaining coordinate position)
            if side_name == Cube.LEFT:
                self.cube.rotate_cube_ccw()
            elif side_name == Cube.RIGHT:
                self.cube.rotate_cube_cw()
            elif side_name == Cube.BACK:
                self.cube.rotate_cw(2)

            # must be front
            # candidate is on bottom row
            if candidate_coords[0] == 2:
                self.solve_corner_on_front_bottom_row(candidate_coords)
                continue
            # candidate is on top row
            elif candidate_coords[0] == 0:
                self.solve_corners_on_front_top_row(candidate_coords)
                continue

    def find_candidate(self):
        for side in [self.cube.front, self.cube.right, self.cube.left, self.cube.back, self.cube.bottom, self.cube.top]:
            for n, m in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                if side.cubies[n][m] == self.top_color:
                    # if a top candidate and already solved then skip
                    side_name = self.cube.get_side_name(side)
                    if side_name == Cube.TOP and self.is_top_corner_solved((n, m)):
                        continue
                    return side_name, (n, m)
        return None, None

    """
    coords are a tuple of coordinates to a cubie location on the bottom row
    of the front side that has the top_color on the face of that location
    """

    def solve_corner_on_front_bottom_row(self, coords):
        adjacent_sides = {(2, 0): (Cube.LEFT, Cube.FRONT),
                          (2, 2): (Cube.FRONT, Cube.RIGHT)}[coords]

        adjacent_side_color = None
        adjacent_bottom_color = None
        if Cube.LEFT in adjacent_sides:
            adjacent_side_color = self.cube.left.cubies[2][2]
            adjacent_bottom_color = self.cube.bottom.cubies[0][0]
        elif Cube.RIGHT in adjacent_sides:
            adjacent_side_color = self.cube.right.cubies[2][0]
            adjacent_bottom_color = self.cube.bottom.cubies[0][2]

        side_color_side_name = self.cube.get_side_name_by_color(adjacent_side_color)
        bottom_color_side_name = self.cube.get_side_name_by_color(adjacent_bottom_color)

        # check if corner at location of adjacent colors, and if not, move to that position
        if set(adjacent_sides) != {side_color_side_name, bottom_color_side_name}:
            sides_to_manipulations = {(frozenset({Cube.LEFT, Cube.FRONT}), frozenset({Cube.FRONT, Cube.RIGHT})):
                                          [self.cube.rotate_bottom_right, self.cube.rotate_cube_cw],
                                      (frozenset({Cube.LEFT, Cube.FRONT}), frozenset({Cube.RIGHT, Cube.BACK})):
                                          [self.cube.rotate_bottom_right, self.cube.rotate_bottom_right,
                                           self.cube.rotate_cube_ccw, self.cube.rotate_cube_ccw],
                                      (frozenset({Cube.LEFT, Cube.FRONT}), frozenset({Cube.BACK, Cube.LEFT})):
                                          [self.cube.rotate_bottom_left, self.cube.rotate_cube_ccw],
                                      (frozenset({Cube.FRONT, Cube.RIGHT}), frozenset({Cube.RIGHT, Cube.BACK})):
                                          [self.cube.rotate_bottom_right, self.cube.rotate_cube_cw],
                                      (frozenset({Cube.FRONT, Cube.RIGHT}), frozenset({Cube.BACK, Cube.LEFT})):
                                          [self.cube.rotate_bottom_right, self.cube.rotate_bottom_right,
                                           self.cube.rotate_cube_ccw, self.cube.rotate_cube_ccw],
                                      (frozenset({Cube.FRONT, Cube.RIGHT}), frozenset({Cube.LEFT, Cube.FRONT})):
                                          [self.cube.rotate_bottom_left, self.cube.rotate_cube_ccw]}
            # move corner to be below destination and turn cube so that corner solver.top_color is facing forward
            key = (frozenset(adjacent_sides), frozenset({side_color_side_name, bottom_color_side_name}))
            for manipulation in sides_to_manipulations[key]:
                manipulation()

        # now corner is positioned below destination, with solver.top_color facing forward
        # so move into solved location
        if Cube.LEFT in adjacent_sides:
            self.cube.rotate_bottom_right()
            self.cube.rotate_left_forward()
            self.cube.rotate_bottom_left()
            self.cube.rotate_left_backward()
        elif Cube.RIGHT in adjacent_sides:
            self.cube.rotate_bottom_left()
            self.cube.rotate_right_forward()
            self.cube.rotate_bottom_right()
            self.cube.rotate_right_backward()

    """
    coords are a tuple of coordinates to a cubie location on the top row
    of the front side that has the top_color on the face at the candidate_coords
    """

    def solve_corners_on_front_top_row(self, candidate_coords):
        adjacent_sides = {(0, 0): (Cube.LEFT, Cube.FRONT),
                          (0, 2): (Cube.FRONT, Cube.RIGHT)}[candidate_coords]

        adjacent_side_color = None
        adjacent_top_color = None
        if Cube.LEFT in adjacent_sides:
            adjacent_side_color = self.cube.left.cubies[0][2]
            adjacent_top_color = self.cube.top.cubies[2][0]
        elif Cube.RIGHT in adjacent_sides:
            adjacent_side_color = self.cube.right.cubies[0][0]
            adjacent_top_color = self.cube.top.cubies[2][2]

        side_color_side_name = self.cube.get_side_name_by_color(adjacent_side_color)
        top_color_side_name = self.cube.get_side_name_by_color(adjacent_top_color)

        sides_to_manipulations = {(frozenset({Cube.LEFT, Cube.FRONT}), frozenset({Cube.LEFT, Cube.FRONT})):
                                      [self.cube.rotate_front_ccw, self.cube.rotate_bottom_left,
                                       self.cube.rotate_front_cw, self.cube.rotate_bottom_right,
                                       self.cube.rotate_bottom_right, self.cube.rotate_left_forward,
                                       self.cube.rotate_bottom_left, self.cube.rotate_left_backward],
                                  (frozenset({Cube.LEFT, Cube.FRONT}), frozenset({Cube.FRONT, Cube.RIGHT})):
                                      [self.cube.rotate_front_ccw, self.cube.rotate_bottom_left,
                                       self.cube.rotate_front_cw, self.cube.rotate_bottom_left,
                                       self.cube.rotate_front_cw, self.cube.rotate_bottom_left,
                                       self.cube.rotate_front_ccw],
                                  (frozenset({Cube.LEFT, Cube.FRONT}), frozenset({Cube.RIGHT, Cube.BACK})):
                                      [self.cube.rotate_front_ccw, self.cube.rotate_bottom_left,
                                       self.cube.rotate_front_cw, self.cube.rotate_right_backward,
                                       self.cube.rotate_bottom_left, self.cube.rotate_right_forward],
                                  (frozenset({Cube.LEFT, Cube.FRONT}), frozenset({Cube.BACK, Cube.LEFT})):
                                      [self.cube.rotate_front_ccw, self.cube.rotate_bottom_left,
                                       self.cube.rotate_front_cw, self.cube.rotate_bottom_right,
                                       self.cube.rotate_back_left, self.cube.rotate_bottom_left,
                                       self.cube.rotate_back_right],
                                  (frozenset({Cube.FRONT, Cube.RIGHT}), frozenset({Cube.FRONT, Cube.RIGHT})):
                                      [self.cube.rotate_front_cw, self.cube.rotate_bottom_right,
                                       self.cube.rotate_front_ccw, self.cube.rotate_bottom_left,
                                       self.cube.rotate_bottom_left, self.cube.rotate_right_forward,
                                       self.cube.rotate_bottom_right, self.cube.rotate_right_backward],
                                  (frozenset({Cube.FRONT, Cube.RIGHT}), frozenset({Cube.RIGHT, Cube.BACK})):
                                      [self.cube.rotate_front_cw, self.cube.rotate_bottom_right,
                                       self.cube.rotate_front_ccw, self.cube.rotate_bottom_left,
                                       self.cube.rotate_back_right, self.cube.rotate_bottom_right,
                                       self.cube.rotate_back_left],
                                  (frozenset({Cube.FRONT, Cube.RIGHT}), frozenset({Cube.BACK, Cube.LEFT})):
                                      [self.cube.rotate_front_cw, self.cube.rotate_bottom_right,
                                       self.cube.rotate_front_ccw, self.cube.rotate_left_backward,
                                       self.cube.rotate_bottom_right, self.cube.rotate_left_forward],
                                  (frozenset({Cube.FRONT, Cube.RIGHT}), frozenset({Cube.LEFT, Cube.FRONT})):
                                      [self.cube.rotate_front_cw, self.cube.rotate_bottom_right,
                                       self.cube.rotate_front_ccw, self.cube.rotate_bottom_right,
                                       self.cube.rotate_front_ccw, self.cube.rotate_bottom_right,
                                       self.cube.rotate_front_cw]}

        # corner to top location
        key = (frozenset(adjacent_sides), frozenset({side_color_side_name, top_color_side_name}))
        for manipulation in sides_to_manipulations[key]:
            manipulation()

    def solve_corners_on_bottom(self, candidate_coords):
        adjacent_sides = {(0, 0): (Cube.LEFT, Cube.FRONT),
                          (0, 2): (Cube.FRONT, Cube.RIGHT),
                          (2, 0): (Cube.BACK, Cube.LEFT),
                          (2, 2): (Cube.RIGHT, Cube.BACK)}[candidate_coords]

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
                                 [self.cube.rotate_cube_ccw],
                             frozenset({Cube.BACK, Cube.RIGHT}):
                                 [self.cube.rotate_cube_cw, self.cube.rotate_cube_cw],
                             frozenset({Cube.RIGHT, Cube.FRONT}):
                                 [self.cube.rotate_cube_cw]}
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

    def is_top_corner_solved(self, coords):
        adj_sides = {(0, 0): (Cube.LEFT, Cube.BACK),
                     (0, 2): (Cube.BACK, Cube.RIGHT),
                     (2, 0): (Cube.FRONT, Cube.LEFT),
                     (2, 2): (Cube.RIGHT, Cube.FRONT)}[coords]

        # in place if the color at that corner is the same color as the
        # center color of that side for both adj_sides
        return (self.cube.top.get_color_by_coords(coords) == self.top_color and
                self.cube.get_side_by_name(adj_sides[0]).cubies[0][0] ==
                self.cube.get_side_by_name(adj_sides[0]).get_center_color() and
                self.cube.get_side_by_name(adj_sides[1]).cubies[0][2] ==
                self.cube.get_side_by_name(adj_sides[1]).get_center_color())

    # candidate_coords should be coordinate to top piece that is of top_color
    # but that needs to be manipulated into correct corner position
    def solve_corner_on_top(self, candidate_coords):
        adj_side_1, adj_side_2 = {(0, 0): (Cube.LEFT, Cube.BACK),
                                  (0, 2): (Cube.BACK, Cube.RIGHT),
                                  (2, 0): (Cube.FRONT, Cube.LEFT),
                                  (2, 2): (Cube.RIGHT, Cube.FRONT)}[candidate_coords]

        # turn cube so that candidate is in front, top, left
        sides_to_manipulations = {frozenset({Cube.LEFT, Cube.FRONT}):
                                      [],
                                  frozenset({Cube.FRONT, Cube.RIGHT}):
                                      [self.cube.rotate_cube_cw],
                                  frozenset({Cube.RIGHT, Cube.BACK}):
                                      [self.cube.rotate_cube_cw, self.cube.rotate_cube_cw],
                                  frozenset({Cube.BACK, Cube.LEFT}):
                                      [self.cube.rotate_cube_ccw]}

        key = frozenset({adj_side_1, adj_side_2})

        manipulations = sides_to_manipulations[key]

        # rotate cube so that candidate is at front, top, left
        for manipulation in manipulations:
            manipulation()

        # now move the candidate out of the top
        # and to the bottom row, in (2,0) with white
        # facing forward
        self.cube.rotate_left_forward()
        self.cube.rotate_bottom_right()
        self.cube.rotate_left_backward()
        self.cube.rotate_cube_cw()

        # leverage solve_corners_on_front_bottom_row
        # now that we have this candidate moved there
        # and in the front
        return self.solve_corner_on_front_bottom_row((2, 0))


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

    def find_candidate(self):
        for side in [self.cube.front, self.cube.right, self.cube.left, self.cube.back, self.cube.bottom, self.cube.top]:
            for n, m in [(0, 1), (1, 0), (1, 2), (2, 1)]:
                if side.cubies[n][m] == self.top_color:
                    # if a top candidate and already solved then skip
                    side_name = self.cube.get_side_name(side)
                    if side_name == Cube.TOP and self.is_top_candidate_solved((n, m)):
                        continue
                    return side_name, (n, m)
        return None, None

    # a top cross candidate is solved if its adjacent color is the same
    # color as the center color on the adjacent side
    def is_top_candidate_solved(self, coordinates):
        adj_side = {(0, 1): self.cube.back,
                    (1, 0): self.cube.left,
                    (1, 2): self.cube.right,
                    (2, 1): self.cube.front}[coordinates]
        return adj_side.get_center_color() == adj_side.cubies[0][1]

    def count_completed(self):
        return sum(cross_color == self.top_color and adj_side.cubies[0][1] == adj_side.get_center_color()
                   for cross_color, adj_side in
                   [(self.cube.top.cubies[0][1], self.cube.back),
                    (self.cube.top.cubies[1][0], self.cube.left),
                    (self.cube.top.cubies[1][2], self.cube.right),
                    (self.cube.top.cubies[2][1], self.cube.front)])

    def solve(self):
        # todo do I need this?
        self.cube.move_side_to_top(self.top_color)

        while not self.is_done():
            side_name, coordinates = self.find_candidate()

            assert side_name in Cube.SIDE_NAMES

            if side_name == Cube.TOP:
                self.solve_cross_piece_on_top(coordinates)
            elif side_name == Cube.FRONT:
                self.solve_cross_piece_on_front(coordinates)
            elif side_name == Cube.BOTTOM:
                self.solve_cross_piece_on_bottom(coordinates)
            elif side_name == Cube.LEFT:
                self.cube.rotate_cube_ccw()
                self.solve_cross_piece_on_front(coordinates)
            elif side_name == Cube.RIGHT:
                self.cube.rotate_cube_cw()
                self.solve_cross_piece_on_front(coordinates)
            elif side_name == Cube.BACK:
                self.cube.rotate_cube_cw(2)
                self.solve_cross_piece_on_front(coordinates)

    """
    expects candidate_coordinates to identify a center-side piece that is of 
    top-color and that is not in the correct position
    """
    def solve_cross_piece_on_top(self, candidate_coordinates):

        coords_to_adj_side = {(0, 1): Cube.BACK,
                              (1, 0): Cube.LEFT,
                              (1, 2): Cube.RIGHT,
                              (2, 1): Cube.FRONT}

        adj_side_name = coords_to_adj_side[candidate_coordinates]
        adj_side = self.cube.get_side_by_name(adj_side_name)

        adj_color = adj_side.cubies[0][1]

        # todo: confirm whether we care to keep this check or not
        # if in correct position, return
        if adj_color == adj_side.get_center_color():
            return

        # not in correct position, so move candidate to bottom
        manipulations = {Cube.BACK: [self.cube.rotate_back_left, self.cube.rotate_cube_cw],
                         Cube.LEFT: [self.cube.rotate_left_forward, self.cube.rotate_left_forward],
                         Cube.RIGHT: [self.cube.rotate_right_forward, self.cube.rotate_right_forward],
                         Cube.FRONT: [self.cube.rotate_front_cw, self.cube.rotate_front_cw]}[adj_side_name]
        for manipulation in manipulations:
            manipulation()

        # move candidate to correct bottom position and then to top
        destination_side_name = self.cube.get_side_name_by_color(adj_color)
        self.move_bottom_cross_piece_into_place(adj_side_name, destination_side_name)

    """
    solve a cross_piece where the top-color on the bottom side at 
    candidate_coordinates to its location on the top
    """

    def solve_cross_piece_on_bottom(self, candidate_coordinates):
        coordinates_to_adj_side = {(0, 1): Cube.FRONT,
                                   (1, 0): Cube.LEFT,
                                   (1, 2): Cube.RIGHT,
                                   (2, 1): Cube.BACK}
        adj_side_name = coordinates_to_adj_side[candidate_coordinates]
        destination_side_name = self.cube.get_side_name_by_color(self.cube.get_side_by_name(adj_side_name).cubies[2][1])
        self.move_bottom_cross_piece_into_place(adj_side_name, destination_side_name)

    """
    utility function that moves a cross-piece of top-color from the bottom
    to the top based on the side that the bottom piece is adjacent to (because
    the top-color side of the piece is facing bottom) and based on the 
    destination side that has the same center-color as the adjacent color
    of the cross piece
    """

    def move_bottom_cross_piece_into_place(self, adj_side_name, destination_side_name):
        # rotate bottom so that candidate is lined up with correct color
        if adj_side_name != destination_side_name:
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
            manipulations = manipulations_map[(adj_side_name, destination_side_name)]
            for manipulation in manipulations:
                manipulation()

        # rotate side so that candidate is now on top
        manipulations = {Cube.FRONT: [self.cube.rotate_front_cw, self.cube.rotate_front_cw],
                         Cube.LEFT: [self.cube.rotate_left_forward, self.cube.rotate_left_forward],
                         Cube.RIGHT: [self.cube.rotate_right_forward, self.cube.rotate_right_forward],
                         Cube.BACK: [self.cube.rotate_back_left, self.cube.rotate_back_left]}[destination_side_name]
        for manipulation in manipulations:
            manipulation()

    """
    solve for a cross piece given candidate_coordinates that is for a piece on the front side
    that is of top color
    """

    def solve_cross_piece_on_front(self, candidate_coordinates):
        if (0, 1) == candidate_coordinates:
            adj_color = self.cube.top.cubies[2][1]
            adjacent_color_location = self.cube.get_side_name_by_color(adj_color)
            # todo consider whether we need this check
            assert adjacent_color_location != Cube.TOP and adjacent_color_location != Cube.BOTTOM
            manipulations_by_side = {Cube.FRONT: [self.cube.rotate_front_cw, self.cube.rotate_right_forward,
                                                  self.cube.rotate_bottom_left, self.cube.rotate_right_backward,
                                                  self.cube.rotate_front_cw, self.cube.rotate_front_cw],
                                     Cube.LEFT: [self.cube.rotate_left_backward],
                                     Cube.RIGHT: [self.cube.rotate_front_cw, self.cube.rotate_right_backward,
                                                  self.cube.rotate_front_ccw],
                                     Cube.BACK: [self.cube.rotate_front_cw, self.cube.rotate_front_cw,
                                                 self.cube.rotate_bottom_right, self.cube.rotate_right_forward,
                                                 self.cube.rotate_back_left, self.cube.rotate_right_backward]}
            manipulations = manipulations_by_side[adjacent_color_location]
            for manipulation in manipulations:
                manipulation()
            return

        elif (1, 0) == candidate_coordinates:
            adj_color = self.cube.left.cubies[1][2]
            adjacent_color_location = self.cube.get_side_name_by_color(adj_color)
            # todo consider whether we need this check
            assert adjacent_color_location != Cube.TOP and adjacent_color_location != Cube.BOTTOM
            manipulations_by_side = {Cube.FRONT: [self.cube.rotate_left_forward, self.cube.rotate_bottom_right,
                                                  self.cube.rotate_front_cw, self.cube.rotate_front_cw,
                                                  self.cube.rotate_left_backward],
                                     Cube.LEFT: [self.cube.rotate_left_backward],
                                     Cube.RIGHT: [self.cube.rotate_front_cw, self.cube.rotate_front_cw,
                                                  self.cube.rotate_right_backward,
                                                  self.cube.rotate_front_cw, self.cube.rotate_front_cw],
                                     Cube.BACK: [self.cube.rotate_left_forward, self.cube.rotate_bottom_left,
                                                 self.cube.rotate_back_left, self.cube.rotate_back_left,
                                                 self.cube.rotate_left_backward]}
            manipulations = manipulations_by_side[adjacent_color_location]
            for manipulation in manipulations:
                manipulation()
            return

        elif (1, 2) == candidate_coordinates:
            adj_color = self.cube.right.cubies[1][0]
            adjacent_color_location = self.cube.get_side_name_by_color(adj_color)
            # todo consider whether we need this check
            assert adjacent_color_location != Cube.TOP and adjacent_color_location != Cube.BOTTOM
            manipulations_by_side = {Cube.FRONT: [self.cube.rotate_right_forward, self.cube.rotate_bottom_left,
                                                  self.cube.rotate_front_cw, self.cube.rotate_front_cw,
                                                  self.cube.rotate_right_backward],
                                     Cube.LEFT: [self.cube.rotate_front_cw, self.cube.rotate_front_cw,
                                                 self.cube.rotate_left_backward,
                                                 self.cube.rotate_front_cw, self.cube.rotate_front_cw],
                                     Cube.RIGHT: [self.cube.rotate_right_backward],
                                     Cube.BACK: [self.cube.rotate_right_forward, self.cube.rotate_bottom_right,
                                                 self.cube.rotate_back_left, self.cube.rotate_back_left,
                                                 self.cube.rotate_right_backward]}
            manipulations = manipulations_by_side[adjacent_color_location]
            for manipulation in manipulations:
                manipulation()
            return

        elif (2, 1) == candidate_coordinates:
            adj_color = self.cube.bottom.cubies[0][1]
            adjacent_color_location = self.cube.get_side_name_by_color(adj_color)
            # todo consider whether we need this check
            assert adjacent_color_location != Cube.TOP and adjacent_color_location != Cube.BOTTOM
            manipulations_by_side = {Cube.FRONT: [self.cube.rotate_bottom_right, self.cube.rotate_right_backward,
                                                  self.cube.rotate_front_ccw, self.cube.rotate_right_forward],
                                     Cube.LEFT: [self.cube.rotate_front_cw, self.cube.rotate_left_backward,
                                                 self.cube.rotate_front_ccw],
                                     Cube.RIGHT: [self.cube.rotate_front_ccw, self.cube.rotate_right_backward,
                                                  self.cube.rotate_front_cw],
                                     Cube.BACK: [self.cube.rotate_bottom_right, self.cube.rotate_right_forward,
                                                 self.cube.rotate_back_left, self.cube.rotate_right_backward]}
            manipulations = manipulations_by_side[adjacent_color_location]
            for manipulation in manipulations:
                manipulation()
            return


class SecondRowSolver(object):

    # top_color: indicates the color of side of the cube from which we began solving
    #            (although it might not be on the top here because we flip the cube)
    # bottom_color: indicates color of the side cube opposite top_color, but it should
    #               will be on top for this solver, so bit of a misnomber
    # todo: consider appropriateness of names of top_color and bottom_color
    def __init__(self, cube, top_color=WHITE):
        self.cube = cube
        self.top_color = top_color
        self.bottom_color = top_color.opposite()
        assert TopCrossSolver(self.cube, self.top_color).is_done(), "Top not solved"
        self.cube.move_side_to_top(self.bottom_color)

    def is_done(self):
        return all(side.get_center_color() == side.cubies[1][0] and
                   side.get_center_color() == side.cubies[1][2]
                   for side in [self.cube.front, self.cube.left,
                                self.cube.right, self.cube.back])

    def count_completed(self):
        return sum(side1.get_center_color() == side1.cubies[1][2] and
                   side2.get_center_color() == side2.cubies[1][0]
                   for side1, side2 in [(self.cube.front, self.cube.right),
                                        (self.cube.right, self.cube.back),
                                        (self.cube.back, self.cube.left),
                                        (self.cube.left, self.cube.front)])

    def find_candidate(self):
        # todo: revise to do top first
        for top_candidate_color, side_name in [(self.cube.top.cubies[0][2], Cube.BACK),
                                               (self.cube.top.cubies[1][0], Cube.LEFT),
                                               (self.cube.top.cubies[1][2], Cube.RIGHT),
                                               (self.cube.top.cubies[2][1], Cube.FRONT)]:
            # if neither colors of the candidate is self.bottom_color, we have a candidate
            if self.bottom_color not in {top_candidate_color, self.cube.get_side_by_name(side_name).cubies[0][1]}:
                return {Cube.TOP, side_name}

        # check sides
        for side1, side2 in [(self.cube.front, self.cube.right),
                             (self.cube.right, self.cube.back),
                             (self.cube.back, self.cube.left),
                             (self.cube.left, self.cube.front)]:
            # discard candidate if either color on cubie is bottom color
            if self.bottom_color in {side1.cubies[1][2], side2.cubies[1][0]}:
                continue
            # if either side color is not in position on its correct side
            # then this is a valid candidate (because we already checked that neither
            # is bottom_color)
            if side1.get_center_color() != side1.cubies[1][2] or side2.get_center_color() != side2.cubies[1][0]:
                return {self.cube.get_side_name(side1), self.cube.get_side_name(side2)}
            continue


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
            side_name = self.cube.get_side_name_by_color(color)

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
