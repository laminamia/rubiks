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
        self.solved_cube.rotate_cube_forward(2)
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

    def test_determine_stage_0(self):
        cube = Parser().parse_string_to_cube("    ORG\n" +
                                             "    OWY\n" +
                                             "    YGG\n" +
                                             "GWB RWR WOY RYY\n" +
                                             "OGR GRW RBY GOG\n" +
                                             "WBY BBW BBO BBO\n" +
                                             "    RWR\n" +
                                             "    GRW\n" +
                                             "    BBW")
        solver = Solver(cube)
        self.assertEqual(Solver.STAGE_0, solver.determine_stage())

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

    def test_determine_right_stage_1(self):
        cube = Parser().parse_string_to_cube("    GOR\n" +
                                             "    BGG\n" +
                                             "    OGY\n" +
                                             "OOB YWB RYB WGW\n" +
                                             "RRR WWW OOR YYB\n" +
                                             "RRG YWG RYB WYW\n" +
                                             "    OBY\n" +
                                             "    GBB\n" +
                                             "    GOO")
        cube.rotate_cube_right()
        solver = Solver(cube)
        self.assertEqual(Solver.STAGE_1,
                         solver.determine_stage())

    def test_determine_bottom_stage_1(self):
        cube = Parser().parse_string_to_cube("    GOR\n" +
                                             "    BGG\n" +
                                             "    OGY\n" +
                                             "OOB YWB RYB WGW\n" +
                                             "RRR WWW OOR YYB\n" +
                                             "RRG YWG RYB WYW\n" +
                                             "    OBY\n" +
                                             "    GBB\n" +
                                             "    GOO")
        cube.rotate_cube_forward()
        solver = Solver(cube)
        self.assertEqual(Solver.STAGE_1,
                         solver.determine_stage())

    def test_determine_back_stage_1(self):
        cube = Parser().parse_string_to_cube("    GOR\n" +
                                             "    BGG\n" +
                                             "    OGY\n" +
                                             "OOB YWB RYB WGW\n" +
                                             "RRR WWW OOR YYB\n" +
                                             "RRG YWG RYB WYW\n" +
                                             "    OBY\n" +
                                             "    GBB\n" +
                                             "    GOO")
        cube.rotate_cube_forward(2)
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

    def test_solve_stage_1(self):
        cube = Parser().parse_string_to_cube("    BGY\n" +
                                             "    RWG\n" +
                                             "    RYO\n" +
                                             "YBB WBG WOG OWR\n" +
                                             "WRR GBY GOW RGO\n" +
                                             "YBY BYG WYW OOR\n" +
                                             "    OOR\n" +
                                             "    WYR\n" +
                                             "    GBB")

        solver = Solver(cube)
        print("Cube before solve stage 1:")
        print(solver.cube)

        self.assertEqual(Solver.STAGE_0,
                         solver.determine_stage())
        solver.solve_stage_1()
        top = solver.cube.top
        top_complete = all(top.get_center_color() == color for color in
                           [c for row in top.cubies for c in row])
        print("Cube after solve stage 1:")
        print(solver.cube)
        self.assertTrue(top_complete)


if __name__ == '__main__':
    #logging.getLogger().setLevel(logging.DEBUG)
    #logging.basicConfig()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSolver)
    unittest.TextTestRunner(verbosity=2).run(suite)
