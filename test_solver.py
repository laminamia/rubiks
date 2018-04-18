import unittest
from rubiks import *
from solver import *
import logging
import sys


class TestStageEvaluator(unittest.TestCase):

    def setUp(self):
        self.solved_cube = Cube.create_solved_cube()

    def test_is_solved(self):
        evaluator = StageEvaluator(self.solved_cube)

        # rotations of a solved cube should not change its state
        self.assertTrue(evaluator.is_solved())
        self.solved_cube.rotate_cube_right()
        self.assertTrue(evaluator.is_solved())
        self.solved_cube.rotate_cube_left()
        self.assertTrue(evaluator.is_solved())
        self.solved_cube.rotate_cube_forward(2)
        self.assertTrue(evaluator.is_solved())
        self.solved_cube.rotate_cube_backward()
        self.assertTrue(evaluator.is_solved())

        cube = self.solved_cube
        cube.rotate_top_right()
        cube.rotate_right_backward()
        cube.rotate_bottom_left()
        cube.rotate_right_backward()
        cube.rotate_left_backward()
        cube.rotate_front_cw()

        self.assertFalse(StageEvaluator(cube).is_solved())

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
        evaluator = StageEvaluator(cube)
        self.assertEqual(StageEvaluator.STAGE_0, evaluator.determine_stage())

    def test_determine_state_solved(self):
        evaluator = StageEvaluator(self.solved_cube)
        self.assertEqual(StageEvaluator.STAGE_SOLVED,
                         evaluator.determine_stage())

    def test_determine_state_0(self):
        cube = Parser().parse_string_to_cube("    OOG\n" +
                                             "    BWG\n" +
                                             "    GYY\n" +
                                             "GRR WGR GWW OYY\n" +
                                             "ROO GGB WRO WBW\n" +
                                             "YYB ORW OGW BBB\n" +
                                             "    YYB\n" +
                                             "    BYR\n" +
                                             "    ROR")
        evaluator = StageEvaluator(cube)
        self.assertEqual(StageEvaluator.STAGE_0,
                         evaluator.determine_stage())

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
        evaluator = StageEvaluator(cube)
        self.assertEqual(StageEvaluator.STAGE_TOP_CROSS_SOLVED,
                         evaluator.determine_stage())
        self.assertEqual(1, len(evaluator.stage_1_candidates))
        self.assertEqual(Cube.TOP, evaluator.stage_1_candidates[0])

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
        evaluator = StageEvaluator(cube)
        self.assertEqual(StageEvaluator.STAGE_TOP_CROSS_SOLVED,
                         evaluator.determine_stage())

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
        evaluator = StageEvaluator(cube)
        self.assertEqual(StageEvaluator.STAGE_TOP_CROSS_SOLVED,
                         evaluator.determine_stage())

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
        evaluator = StageEvaluator(cube)
        self.assertEqual(StageEvaluator.STAGE_TOP_CROSS_SOLVED,
                         evaluator.determine_stage())

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
        evaluator = StageEvaluator(cube)
        self.assertEqual(StageEvaluator.STAGE_TOP_CROSS_SOLVED,
                         evaluator.determine_stage())

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
        evaluator = StageEvaluator(cube)
        self.assertEqual(StageEvaluator.STAGE_TOP_CROSS_SOLVED,
                         evaluator.determine_stage())
        self.assertEqual(1, len(evaluator.stage_1_candidates))
        self.assertEqual(Cube.LEFT, evaluator.stage_1_candidates[0])

class TestTopCrossSolver(unittest.TestCase):

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

        evaluator = StageEvaluator(cube)
        print("Cube before solve stage 1:")
        print(evaluator.cube)

        self.assertEqual(StageEvaluator.STAGE_0,
                         StageEvaluator(evaluator.cube).determine_stage())
        evaluator.solve_stage_1()
        top = evaluator.cube.top
        top_complete = all(top.get_center_color() == color for color in
                           [c for row in top.cubies for c in row])
        print("Cube after solve stage 1:")
        print(evaluator.cube)
        self.assertTrue(top_complete)


if __name__ == '__main__':
    #logging.getLogger().setLevel(logging.DEBUG)
    #logging.basicConfig()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestStageEvaluator)
    unittest.TextTestRunner(verbosity=2).run(suite)
