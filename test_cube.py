import unittest
from rubiks import *
from solver import *
import logging
import sys


class TestSolver(unittest.TestCase):

    def setUp(self):
        self.solved_cube = Cube.create_solved_cube()

    def test_is_solved(self):
        solver = Solver(self.solved_cube)

        # rotations of a solved cube should not change its state
        self.assertTrue(solver.is_solved())
        self.solved_cube.rotate_cube_right()
        self.assertTrue(solver.is_solved())
        self.solved_cube.rotate_cube_left()
        self.assertTrue(solver.is_solved())
        self.solved_cube.rotate_cube_forward()
        self.assertTrue(solver.is_solved())
        self.solved_cube.rotate_cube_backward()
        self.assertTrue(solver.is_solved())

        cube = self.solved_cube
        cube.rotate_top_right()
        cube.rotate_right_backward()
        cube.rotate_bottom_left()
        cube.rotate_right_backward()
        cube.rotate_left_backward()
        cube.rotate_front_cw()

        self.assertFalse(Solver(cube).is_solved())

    def test_determine_state_solved(self):
        solver = Solver(self.solved_cube)
        self.assertEqual(Solver.STAGE_SOLVED,
                         solver.determine_stage())

    def test_determine_state_0(self):
        cube = Parser().parse_string_to_cube("OOG\n" +
                                             "BWG\n" +
                                             "GYY\n" +
                                             "GRR WGR GWW OYY\n" +
                                             "ROO GGB WRO WBW\n" +
                                             "YYB ORW OGW BBB\n" +
                                             "YYB\n" +
                                             "BYR\n" +
                                             "ROR")
        solver = Solver(cube)
        self.assertEqual(Solver.STAGE_0,
                         solver.determine_stage())

    def test_determine_top_state_1(self):
        # testing top at stage_1
        cube = Parser().parse_string_to_cube("    YWB\n" +
                                             "    WWW\n" +
                                             "    YWG\n" +
                                             "BRG OBY ROR YGO\n" +
                                             "ORR GBB YOY GGB\n" +
                                             "ORR GOO BRB ROG\n" +
                                             "    WYW\n" +
                                             "    BYY\n" +
                                             "    WGW")
        solver = Solver(cube)
        self.assertEqual(Solver.STAGE_1,
                         solver.determine_stage())
        self.assertEqual(1, len(solver.stage_1_candidates))
        self.assertEqual(Cube.TOP, solver.stage_1_candidates[0])

    def test_determine_front_stage_1(self):
        # testing front at stage_1
        cube = Parser().parse_string_to_cube("    GOR\n" +
                                             "    BGG\n" +
                                             "    OGY\n" +
                                             "OOB YWB RYB WGW\n" +
                                             "RRR WWW OOR YYB\n" +
                                             "RRG YWG RYB WYW\n" +
                                             "    OBY\n" +
                                             "    GBB\n" +
                                             "    GOO")
        solver = Solver(cube)
        self.assertEqual(Solver.STAGE_1,
                         solver.determine_stage())

    def test_determine_left_stage_1(self):
        # testing left at stage_1
        cube = Parser().parse_string_to_cube("    OBG\n" +
                                             "    GGO\n" +
                                             "    YGR\n" +
                                             "YWB RYB WGW OOB\n" +
                                             "WWW OOR YYB RRR\n" +
                                             "YWG RYB WYW RRG\n" +
                                             "    YBO\n" +
                                             "    BBO\n" +
                                             "    OGG")
        solver = Solver(cube)
        self.assertEqual(Solver.STAGE_1,
                         solver.determine_stage())
        self.assertEqual(1, len(solver.stage_1_candidates))
        self.assertEqual(Cube.LEFT, solver.stage_1_candidates[0])



class TestParser(unittest.TestCase):

    def test_is_string_valid(self):
        p = Parser()
        self.assertFalse(p.is_string_valid("YOG GOB RBW"))
        self.assertTrue(p.is_string_valid("    YOG    \n\n" +
                                          "   GOB  \n" +
                                          " RBW    \n" +
                                          "  BGR  YWR BOY   RYO\n\n" +
                                          "RRG RBB YOW GGW\n" +
                                          "RBW GGW OYO GOW\n" +
                                          "    OYB\n" +
                                          "    RYR\n" +
                                          "    GBY"
                                          ))
        self.assertFalse(p.is_string_valid("    YOG    \n\n" +
                                           "   GOB  \n" +
                                           " RBW    \n" +
                                           "  BGR  YWR BOY   RYO\n\n" +
                                           "RRG RBB YOW GGW\n" +
                                           "RBW GGW OYO GOW\n"
                                           ))
        self.assertTrue(p.is_string_valid("    YOG    \n\n" +
                                          "   GOB  \n" +
                                          " RBW    \n" +
                                          "  BGGYWRBOYRYO\n" +
                                          "RRG RBB YOW GGW\n" +
                                          "RBW GGW OYO GOW\n" +
                                          "    OYB\n" +
                                          "    RYR\n" +
                                          "    GBY"))
        self.assertTrue(p.is_string_valid("    YOG    \n\n" +
                                          "   GOB  \n" +
                                          " RBW    \n" +
                                          "  BGGYWRBOYRYO\n" +
                                          "RRG RBB YOW GGW\n" +
                                          "RBW GGW OYO GOW\n" +
                                          "  \n\n  OYB\n" +
                                          "  \t  RYR\n" +
                                          "\t\n    GBY\n\n\n\n\n   \t\t\t"))
        self.assertTrue(p.is_string_valid("    yog    \n\n" +
                                          "   GOB  \n" +
                                          " RBW    \n" +
                                          "  BGGYwRBOYRYO\n" +
                                          "RRG RBB YoW GGW\n" +
                                          "RBW GGW OyO GOW\n" +
                                          "  \n\n  OYB\n" +
                                          "  \t  RYR\n" +
                                          "\t\n    GBY\n\n\n\n\n   \t\t\t"))
        self.assertTrue(p.is_string_valid("    YOG\n" + \
                                          "    OWW\n" + \
                                          "    BBW\n" + \
                                          "BGR YWR BOY RYO\n" + \
                                          "RRG RBB YOW GGW\n" + \
                                          "RBW GGW OYO GOW\n" + \
                                          "    OYB\n" + \
                                          "    RYR\n" + \
                                          "    GBY"))

    def test_create_cube_from_string(self):
        expected = Cube(top=Side([[YELLOW, ORANGE, GREEN],
                                  [ORANGE, WHITE, WHITE],
                                  [BLUE, BLUE, WHITE]]),
                        bottom=Side([[ORANGE, YELLOW, BLUE],
                                     [RED, YELLOW, RED],
                                     [GREEN, BLUE, YELLOW]]),
                        left=Side([[BLUE, GREEN, RED],
                                   [RED, RED, GREEN],
                                   [RED, BLUE, WHITE]]),
                        front=Side([[YELLOW, WHITE, RED],
                                    [RED, BLUE, BLUE],
                                    [GREEN, GREEN, WHITE]]),
                        right=Side([[BLUE, ORANGE, YELLOW],
                                    [YELLOW, ORANGE, WHITE],
                                    [ORANGE, YELLOW, ORANGE]]),
                        back=Side([[RED, YELLOW, ORANGE],
                                   [GREEN, GREEN, WHITE],
                                   [GREEN, ORANGE, WHITE]]))

        cube = Parser().parse_string_to_cube("    YOG\n" +
                                             "    OWW\n" +
                                             "    BBW\n" +
                                             "BGR YWR BOY RYO\n" +
                                             "RRG RBB YOW GGW\n" +
                                             "RBW GGW OYO GOW\n" +
                                             "    OYB\n" +
                                             "    RYR\n" +
                                             "    GBY")

        self.assertEqual(expected, cube)


class TestCube(unittest.TestCase):

    def setUp(self):
        # sides for use in tests
        self.front = Side([[YELLOW, WHITE, RED],
                           [RED, BLUE, BLUE],
                           [GREEN, GREEN, WHITE]])
        self.back = Side([[RED, YELLOW, ORANGE],
                          [GREEN, GREEN, WHITE],
                          [GREEN, ORANGE, WHITE]])
        self.left = Side([[BLUE, GREEN, RED],
                          [RED, RED, GREEN],
                          [RED, BLUE, WHITE]])
        self.right = Side([[BLUE, ORANGE, YELLOW],
                           [YELLOW, ORANGE, WHITE],
                           [ORANGE, YELLOW, ORANGE]])
        self.top = Side([[YELLOW, ORANGE, GREEN],
                         [ORANGE, WHITE, WHITE],
                         [BLUE, BLUE, WHITE]])
        self.bottom = Side([[ORANGE, YELLOW, BLUE],
                            [RED, YELLOW, RED],
                            [GREEN, BLUE, YELLOW]])

        # use copies in cube because the lists will be modified by cube manipulation
        self.cube = Cube(front=self.front.copy(),
                         back=self.back.copy(),
                         left=self.left.copy(),
                         right=self.right.copy(),
                         top=self.top.copy(),
                         bottom=self.bottom.copy())

    def test_rotate_back_left(self):
        expected = Cube(front=self.front.copy(),
                        back=self.back.copy().rotate_face_colors_cw(),
                        left=Side([[GREEN, GREEN, RED],
                                   [ORANGE, RED, GREEN],
                                   [YELLOW, BLUE, WHITE]]),
                        right=Side([[BLUE, ORANGE, YELLOW],
                                    [YELLOW, ORANGE, BLUE],
                                    [ORANGE, YELLOW, GREEN]]),
                        top=Side([[YELLOW, WHITE, ORANGE],
                                  [ORANGE, WHITE, WHITE],
                                  [BLUE, BLUE, WHITE]]),
                        bottom=Side([[ORANGE, YELLOW, BLUE],
                                     [RED, YELLOW, RED],
                                     [BLUE, RED, RED]]))

        self.run_test_manipulation(self.cube.rotate_back_left, expected)

    def test_rotate_back_right(self):
        expected = Cube(front=self.front.copy(),
                        back=self.back.copy().rotate_face_colors_ccw(),
                        left=Side([[GREEN, GREEN, RED],
                                   [BLUE, RED, GREEN],
                                   [YELLOW, BLUE, WHITE]]),
                        right=Side([[BLUE, ORANGE, YELLOW],
                                    [YELLOW, ORANGE, ORANGE],
                                    [ORANGE, YELLOW, GREEN]]),
                        top=Side([[RED, RED, BLUE],
                                  [ORANGE, WHITE, WHITE],
                                  [BLUE, BLUE, WHITE]]),
                        bottom=Side([[ORANGE, YELLOW, BLUE],
                                     [RED, YELLOW, RED],
                                     [ORANGE, WHITE, YELLOW]]))

        self.run_test_manipulation(self.cube.rotate_back_right, expected)

    def test_rotate_front_cw(self):
        expected = Cube(front=Side([[GREEN, RED, YELLOW],
                                    [GREEN, BLUE, WHITE],
                                    [WHITE, BLUE, RED]]),
                        back=Side([[RED, YELLOW, ORANGE],
                                   [GREEN, GREEN, WHITE],
                                   [GREEN, ORANGE, WHITE]]),
                        left=Side([[BLUE, GREEN, ORANGE],
                                   [RED, RED, YELLOW],
                                   [RED, BLUE, BLUE]]),
                        right=Side([[BLUE, ORANGE, YELLOW],
                                    [BLUE, ORANGE, WHITE],
                                    [WHITE, YELLOW, ORANGE]]),
                        top=Side([[YELLOW, ORANGE, GREEN],
                                  [ORANGE, WHITE, WHITE],
                                  [WHITE, GREEN, RED]]),
                        bottom=Side([[ORANGE, YELLOW, BLUE],
                                     [RED, YELLOW, RED],
                                     [GREEN, BLUE, YELLOW]]))

        self.run_test_manipulation(self.cube.rotate_front_cw, expected)

        # Running another version
        cube = Parser().parse_string_to_cube("    OBG\n" +
                                             "    GGO\n" +
                                             "    YGR\n" +
                                             "YWB RYB WGW OOB\n" +
                                             "WWW OOR YYB RRR\n" +
                                             "YWG RYB WYW RRG\n" +
                                             "    YBO\n" +
                                             "    BBO\n" +
                                             "    OGG")

        expected = Parser().parse_string_to_cube("    YWY\n" +
                                                 "    WWW\n" +
                                                 "    GWB\n" +
                                                 "OBY ROR YGO BRG\n" +
                                                 "GBB YOY GGB ORR\n" +
                                                 "GOO BRB ROG ORR\n" +
                                                 "    WYW\n" +
                                                 "    YYG\n" +
                                                 "    WBW")
        sys.stdout.flush()
        print("\nCube Before Manipulation:\n\n")
        print(cube)
        sys.stdout.flush()
        print("\nExpected Before Cube Manipulation:\n\n")
        print(expected)
        print("\n\n\n")
        sys.stdout.flush()

        cube.rotate_front_cw()

        sys.stdout.flush()
        print("\nCube After Manipulation:\n\n")
        print(cube)
        sys.stdout.flush()
        print("\nExpected After Cube Manipulation:\n\n")
        print(expected)
        print("\n\n\n")
        sys.stdout.flush()

        self.assertEqual(cube, expected)

    def test_rotate_front_ccw(self):
        expected = Cube(front=Side([[RED, BLUE, WHITE],
                                    [WHITE, BLUE, GREEN],
                                    [YELLOW, RED, GREEN]]),
                        back=Side([[RED, YELLOW, ORANGE],
                                   [GREEN, GREEN, WHITE],
                                   [GREEN, ORANGE, WHITE]]),
                        left=Side([[BLUE, GREEN, WHITE],
                                   [RED, RED, BLUE],
                                   [RED, BLUE, BLUE]]),
                        right=Side([[BLUE, ORANGE, YELLOW],
                                    [YELLOW, ORANGE, WHITE],
                                    [ORANGE, YELLOW, ORANGE]]),
                        top=Side([[YELLOW, ORANGE, GREEN],
                                  [ORANGE, WHITE, WHITE],
                                  [BLUE, YELLOW, ORANGE]]),
                        bottom=Side([[RED, GREEN, WHITE],
                                     [RED, YELLOW, RED],
                                     [GREEN, BLUE, YELLOW]]))

        self.run_test_manipulation(self.cube.rotate_front_ccw, expected)

    def test_rotate_right_forward(self):
        expected = Cube(front=Side([[YELLOW, WHITE, GREEN],
                                    [RED, BLUE, WHITE],
                                    [GREEN, GREEN, WHITE]]),
                        back=Side([[YELLOW, YELLOW, ORANGE],
                                   [RED, GREEN, WHITE],
                                   [BLUE, ORANGE, WHITE]]),
                        left=self.left.copy(),
                        right=Side.create_from_side(self.right.copy().rotate_face_colors_ccw()),
                        top=Side([[YELLOW, ORANGE, GREEN],
                                  [ORANGE, WHITE, GREEN],
                                  [BLUE, BLUE, RED]]),
                        bottom=Side([[ORANGE, YELLOW, RED],
                                     [RED, YELLOW, BLUE],
                                     [GREEN, BLUE, WHITE]]))
        self.run_test_manipulation(self.cube.rotate_right_forward, expected)

    def test_rotate_right_backward(self):
        expected = Cube(front=Side([[YELLOW, WHITE, BLUE],
                                    [RED, BLUE, RED],
                                    [GREEN, GREEN, YELLOW]]),
                        back=Side([[WHITE, YELLOW, ORANGE],
                                   [WHITE, GREEN, WHITE],
                                   [GREEN, ORANGE, WHITE]]),
                        left=self.left.copy(),
                        right=Side.create_from_side(self.right.copy().rotate_face_colors_cw()),
                        top=Side([[YELLOW, ORANGE, RED],
                                  [ORANGE, WHITE, BLUE],
                                  [BLUE, BLUE, WHITE]]),
                        bottom=Side([[ORANGE, YELLOW, GREEN],
                                     [RED, YELLOW, GREEN],
                                     [GREEN, BLUE, RED]]))
        self.run_test_manipulation(self.cube.rotate_right_backward, expected)

    def test_rotate_left_forward(self):
        expected = Cube(front=Side([[YELLOW, WHITE, RED],
                                    [ORANGE, BLUE, BLUE],
                                    [BLUE, GREEN, WHITE]]),
                        back=Side([[RED, YELLOW, GREEN],
                                   [GREEN, GREEN, RED],
                                   [GREEN, ORANGE, ORANGE]]),
                        left=Side([[RED, RED, BLUE],
                                   [BLUE, RED, GREEN],
                                   [WHITE, GREEN, RED]]),
                        right=self.right.copy(),
                        top=Side([[WHITE, ORANGE, GREEN],
                                  [WHITE, WHITE, WHITE],
                                  [ORANGE, BLUE, WHITE]]),
                        bottom=Side([[YELLOW, YELLOW, BLUE],
                                     [RED, YELLOW, RED],
                                     [GREEN, BLUE, YELLOW]]))

        self.run_test_manipulation(self.cube.rotate_left_forward, expected)

    def test_rotate_left_backward(self):
        expected = Cube(front=Side([[ORANGE, WHITE, RED],
                                    [RED, BLUE, BLUE],
                                    [GREEN, GREEN, WHITE]]),
                        back=Side([[RED, YELLOW, BLUE],
                                   [GREEN, GREEN, ORANGE],
                                   [GREEN, ORANGE, YELLOW]]),
                        left=Side.create_from_side(self.left.copy().rotate_face_colors_ccw()),
                        right=self.right.copy(),
                        top=Side([[YELLOW, ORANGE, GREEN],
                                  [RED, WHITE, WHITE],
                                  [GREEN, BLUE, WHITE]]),
                        bottom=Side([[WHITE, YELLOW, BLUE],
                                     [WHITE, YELLOW, RED],
                                     [ORANGE, BLUE, YELLOW]]))

        self.run_test_manipulation(self.cube.rotate_left_backward, expected)

    def test_rotate_top_left(self):
        expected = Cube(front=Side([[BLUE, ORANGE, YELLOW],
                                    [RED, BLUE, BLUE],
                                    [GREEN, GREEN, WHITE]]),
                        back=Side([[BLUE, GREEN, RED],
                                   [GREEN, GREEN, WHITE],
                                   [GREEN, ORANGE, WHITE]]),
                        left=Side([[YELLOW, WHITE, RED],
                                   [RED, RED, GREEN],
                                   [RED, BLUE, WHITE]]),
                        right=Side([[RED, YELLOW, ORANGE],
                                    [YELLOW, ORANGE, WHITE],
                                    [ORANGE, YELLOW, ORANGE]]),
                        top=Side([[BLUE, ORANGE, YELLOW],
                                  [BLUE, WHITE, ORANGE],
                                  [WHITE, WHITE, GREEN]]),
                        bottom=self.bottom.copy())

        self.run_test_manipulation(self.cube.rotate_top_left, expected)

    def test_rotate_top_right(self):
        expected = Cube(front=Side([[BLUE, GREEN, RED],
                                    [RED, BLUE, BLUE],
                                    [GREEN, GREEN, WHITE]]),
                        back=Side([[BLUE, ORANGE, YELLOW],
                                   [GREEN, GREEN, WHITE],
                                   [GREEN, ORANGE, WHITE]]),
                        left=Side([[RED, YELLOW, ORANGE],
                                   [RED, RED, GREEN],
                                   [RED, BLUE, WHITE]]),
                        right=Side([[YELLOW, WHITE, RED],
                                    [YELLOW, ORANGE, WHITE],
                                    [ORANGE, YELLOW, ORANGE]]),
                        top=Side([[GREEN, WHITE, WHITE],
                                  [ORANGE, WHITE, BLUE],
                                  [YELLOW, ORANGE, BLUE]]),
                        bottom=self.bottom.copy())

        self.run_test_manipulation(self.cube.rotate_top_right, expected)

    def test_rotate_bottom_left(self):
        expected = Cube(front=Side([[YELLOW, WHITE, RED],
                                    [RED, BLUE, BLUE],
                                    [ORANGE, YELLOW, ORANGE]]),
                        back=Side([[RED, YELLOW, ORANGE],
                                   [GREEN, GREEN, WHITE],
                                   [RED, BLUE, WHITE]]),
                        left=Side([[BLUE, GREEN, RED],
                                   [RED, RED, GREEN],
                                   [GREEN, GREEN, WHITE]]),
                        right=Side([[BLUE, ORANGE, YELLOW],
                                    [YELLOW, ORANGE, WHITE],
                                    [GREEN, ORANGE, WHITE]]),
                        top=self.top.copy(),
                        bottom=self.bottom.copy().rotate_face_colors_ccw())

        self.run_test_manipulation(self.cube.rotate_bottom_left, expected)

    def test_rotate_bottom_right(self):
        expected = Cube(front=Side([[YELLOW, WHITE, RED],
                                    [RED, BLUE, BLUE],
                                    [RED, BLUE, WHITE]]),
                        back=Side([[RED, YELLOW, ORANGE],
                                   [GREEN, GREEN, WHITE],
                                   [ORANGE, YELLOW, ORANGE]]),
                        left=Side([[BLUE, GREEN, RED],
                                   [RED, RED, GREEN],
                                   [GREEN, ORANGE, WHITE]]),
                        right=Side([[BLUE, ORANGE, YELLOW],
                                    [YELLOW, ORANGE, WHITE],
                                    [GREEN, GREEN, WHITE]]),
                        top=self.top.copy(),
                        bottom=self.bottom.copy().rotate_face_colors_cw())

        self.run_test_manipulation(self.cube.rotate_bottom_right, expected)

    def test_rotate_cube_right(self):
        expected = Cube(right=self.front, back=self.right, left=self.back, front=self.left,
                        top=Side([[GREEN, WHITE, WHITE],
                                  [ORANGE, WHITE, BLUE],
                                  [YELLOW, ORANGE, BLUE]]),
                        bottom=Side([[GREEN, RED, ORANGE],
                                     [BLUE, YELLOW, YELLOW],
                                     [YELLOW, RED, BLUE]]))
        self.run_test_manipulation(self.cube.rotate_cube_right, expected)

    def test_rotate_cube_left(self):
        expected = Cube(left=self.front, back=self.left, right=self.back, front=self.right,
                        top=Side([[BLUE, ORANGE, YELLOW],
                                  [BLUE, WHITE, ORANGE],
                                  [WHITE, WHITE, GREEN]]),
                        bottom=Side([[BLUE, RED, YELLOW],
                                     [YELLOW, YELLOW, BLUE],
                                     [ORANGE, RED, GREEN]]))

        self.run_test_manipulation(self.cube.rotate_cube_left, expected)

    def test_rotate_cube_forward(self):
        expected = Cube(front=self.top,
                        bottom=self.front,
                        back=Side([[YELLOW, BLUE, GREEN],
                                   [RED, YELLOW, RED],
                                   [BLUE, YELLOW, ORANGE]]),
                        top=Side([[WHITE, ORANGE, GREEN],
                                  [WHITE, GREEN, GREEN],
                                  [ORANGE, YELLOW, RED]]),
                        left=self.left.copy().rotate_face_colors_cw(),
                        right=self.right.copy().rotate_face_colors_ccw())

        self.run_test_manipulation(self.cube.rotate_cube_forward, expected)

    def test_rotate_cube_forward_multi(self):
        expected = Cube(front=self.back.create_inverse(),
                        bottom=self.top.copy(),
                        back=self.front.create_inverse(),
                        top=self.bottom.copy(),
                        left=self.left.copy().rotate_face_colors_cw().rotate_face_colors_cw(),
                        right=self.right.copy().rotate_face_colors_ccw().rotate_face_colors_ccw())

        self.run_test_manipulation(self.cube.rotate_cube_forward, expected, 2)

    def test_rotate_cube_back(self):
        expected = Cube(top=self.front,
                        front=self.bottom,
                        back=self.top.copy().create_inverse(),
                        bottom=self.back.copy().create_inverse(),
                        left=self.left.copy().rotate_face_colors_ccw(),
                        right=self.right.copy().rotate_face_colors_cw())

        self.run_test_manipulation(self.cube.rotate_cube_backward, expected)

    def test_eq(self):
        cube1 = self.cube.copy()
        self.assertEqual(self.cube, cube1)
        cube1.rotate_front_cw()
        cube1.rotate_left_forward()
        self.assertNotEqual(self.cube, cube1)

    def run_test_manipulation(self, manipulation_fn, expected_cube, *args):
        self.assertEqual(self.front, self.cube.front, "Front not as expected before manipulation")
        self.assertEqual(self.back, self.cube.back, "Back not as expected before manipulation")
        self.assertEqual(self.left, self.cube.left, "Left not as expected before manipulation")
        self.assertEqual(self.right, self.cube.right, "Right not as expected before manipulation")
        self.assertEqual(self.top, self.cube.top, "Top not as expected before manipulation")
        self.assertEqual(self.bottom, self.cube.bottom, "Bottom not as expected before manipulation")

        logging.getLogger().debug("Cube before manipulation\n\n")
        logging.getLogger().debug("Right\n%r", self.cube.right)
        logging.getLogger().debug("Bottom\n%r", self.cube.bottom)
        logging.getLogger().debug("Left\n%r", self.cube.left)
        logging.getLogger().debug("Top\n%r", self.cube.top)
        logging.getLogger().debug("Front\n%r", self.cube.front)
        logging.getLogger().debug("Back\n%r", self.cube.back)

        manipulation_fn(*args)

        logging.getLogger().debug("Cube after manipulation\n\n")
        logging.getLogger().debug("Right\n%r", self.cube.right)
        logging.getLogger().debug("Bottom\n%r", self.cube.bottom)
        logging.getLogger().debug("Left\n%r", self.cube.left)
        logging.getLogger().debug("Top\n%r", self.cube.top)
        logging.getLogger().debug("Front\n%r", self.cube.front)
        logging.getLogger().debug("Back\n%r", self.cube.back)

        self.assertEqual(expected_cube.front, self.cube.front, "Front not as expected")
        self.assertEqual(expected_cube.back, self.cube.back, "Back not as expected")
        self.assertEqual(expected_cube.right, self.cube.right, "Right not as expected")
        self.assertEqual(expected_cube.top, self.cube.top, "Top not as expected")
        self.assertEqual(expected_cube.bottom, self.cube.bottom, "Bottom not as expected")
        self.assertEqual(expected_cube.left, self.cube.left, "Left not as expected")

    def test_get_side_name(self):
        self.assertEqual(Cube.FRONT, self.cube.get_side_name(self.cube.front))


class TestColor(unittest.TestCase):

    def test_eq(self):
        c1 = Color("W", None)
        c2 = Color("W", "Something")

        self.assertEqual(c1, c2)


class TestSide(unittest.TestCase):

    def test_create_inverse(self):
        s1 = Side([[YELLOW, WHITE, RED],
                   [RED, BLUE, BLUE],
                   [GREEN, GREEN, WHITE]])
        expected = Side([[WHITE, GREEN, GREEN],
                         [BLUE, BLUE, RED],
                         [RED, WHITE, YELLOW]])
        self.assertEqual(expected, s1.create_inverse())

    def test_get_row(self):
        rows = [[YELLOW, WHITE, RED],
                [RED, BLUE, BLUE],
                [GREEN, GREEN, WHITE]]

        s = Side(rows)

        for i in range(len(rows)):
            self.assertEqual(rows[i], s.get_row(i))

    def test_get_column(self):
        rows = [[YELLOW, WHITE, RED],
                [RED, BLUE, BLUE],
                [GREEN, GREEN, WHITE]]

        s = Side(rows)

        self.assertEqual([YELLOW, RED, GREEN], s.get_column(0))
        self.assertEqual([WHITE, BLUE, GREEN], s.get_column(1))
        self.assertEqual([RED, BLUE, WHITE], s.get_column(2))

    def test_init(self):
        try:
            Side([[]])
            self.fail("Didn't raise AssertionError")
        except AssertionError:
            pass

    def test_eq(self):
        s1 = Side.create_unicolor_side(RED)
        s2 = Side.create_unicolor_side(RED)
        self.assertEqual(s1, s2, "Two all Red sides should be equal")

        s2 = Side.create_unicolor_side(BLUE)
        self.assertNotEqual(s1, s2, "Red and Blue sides should not be equal")

        s2 = Side([[RED, BLUE, GREEN],
                   [YELLOW, WHITE, ORANGE],
                   [BLUE, GREEN, YELLOW]])
        self.assertNotEqual(s1, s2)

        s1 = Side([[RED, BLUE, GREEN],
                   [YELLOW, WHITE, ORANGE],
                   [BLUE, GREEN, YELLOW]])
        self.assertEqual(s1, s2)

    def test_copy(self):
        s1 = Side([[RED, BLUE, GREEN],
                   [YELLOW, WHITE, ORANGE],
                   [BLUE, GREEN, YELLOW]])

        self.assertEqual(s1, Side.create_from_side(s1))
        self.assertIsNot(s1, Side.create_from_side(s1))
        self.assertEqual(s1, s1.copy())
        self.assertIsNot(s1, s1.copy())

    def test_create_inverse(self):
        s1 = Side([[RED, BLUE, GREEN],
                   [YELLOW, WHITE, ORANGE],
                   [BLUE, GREEN, YELLOW]])
        s2 = Side([[YELLOW, GREEN, BLUE],
                   [ORANGE, WHITE, YELLOW],
                   [GREEN, BLUE, RED]])
        self.assertEqual(s2, s1.create_inverse())
        self.assertIsNot(s1, s1.create_inverse())

    def test_rotate_face_colors_cw(self):
        s1 = Side([[RED, BLUE, GREEN],
                   [YELLOW, WHITE, ORANGE],
                   [BLUE, GREEN, YELLOW]])
        s2 = Side([[BLUE, YELLOW, RED],
                   [GREEN, WHITE, BLUE],
                   [YELLOW, ORANGE, GREEN]])
        self.assertEqual(s2, s1.rotate_face_colors_cw())

    def test_rotate_face_colors_ccw(self):
        s1 = Side([[RED, BLUE, GREEN],
                   [YELLOW, WHITE, ORANGE],
                   [BLUE, GREEN, YELLOW]])
        s2 = Side([[GREEN, ORANGE, YELLOW],
                   [BLUE, WHITE, GREEN],
                   [RED, YELLOW, BLUE]])
        self.assertEqual(s2, s1.rotate_face_colors_ccw())

    def test_get_center_color(self):
        s1 = Side([[RED, BLUE, GREEN],
                   [YELLOW, WHITE, ORANGE],
                   [BLUE, GREEN, YELLOW]])
        s2 = Side([[GREEN, ORANGE, YELLOW],
                   [BLUE, BLUE, GREEN],
                   [RED, YELLOW, BLUE]])
        self.assertEqual(WHITE, s1.get_center_color())
        self.assertEqual(BLUE, s2.get_center_color())

    def test_is_side_unicolor(self):
        side = Side([[RED, RED, RED],
                   [RED, RED, RED],
                   [RED, RED, RED]])
        self.assertTrue(side.is_side_unicolor())


if __name__ == '__main__':
    # logging.getLogger().setLevel(logging.DEBUG)
    # logging.basicConfig()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSolver)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestCube)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSide)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestColor)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
    unittest.TextTestRunner(verbosity=2).run(suite)
