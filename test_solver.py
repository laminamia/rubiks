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
        self.solved_cube.rotate_cube_ccw()
        self.assertTrue(evaluator.is_solved())
        self.solved_cube.rotate_cube_cw()
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

    def test_is_solved_2(self):
        cube = Parser().parse_string_to_cube("    OGY\n" +
                                             "    OOY\n" +
                                             "    OOG\n" +
                                             "WWW BGY RRO BRG\n" +
                                             "WWW BBY GYO BGG\n" +
                                             "WWW BOB YBG YBG\n" +
                                             "    RYR\n" +
                                             "    RRR\n" +
                                             "    RYO")
        cube.rotate_cube_ccw(2)
        evaluator = StageEvaluator(cube)
        self.assertFalse(evaluator.is_solved())

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

    def test_determine_top_top_cross_solved(self):
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
        self.assertEqual(1, len(evaluator.top_cross_candidates))
        self.assertEqual(Cube.TOP, evaluator.top_cross_candidates[0])

    def test_determine_front_top_cross_solved(self):
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

    def test_determine_right_top_cross_solved(self):
        cube = Parser().parse_string_to_cube("    GOR\n" +
                                             "    BGG\n" +
                                             "    OGY\n" +
                                             "OOB YWB RYB WGW\n" +
                                             "RRR WWW OOR YYB\n" +
                                             "RRG YWG RYB WYW\n" +
                                             "    OBY\n" +
                                             "    GBB\n" +
                                             "    GOO")
        cube.rotate_cube_ccw()
        evaluator = StageEvaluator(cube)
        self.assertEqual(StageEvaluator.STAGE_TOP_CROSS_SOLVED,
                         evaluator.determine_stage())

    def test_determine_bottom_top_cross_solved(self):
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

    def test_determine_back_top_cross_solved(self):
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

    def test_determine_left_top_cross_solved(self):
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
        self.assertEqual(1, len(evaluator.top_cross_candidates))
        self.assertEqual(Cube.LEFT, evaluator.top_cross_candidates[0])

    def test_determine_left_top_solved(self):
        cube = Parser().parse_string_to_cube("    OGY\n" +
                                             "    OOY\n" +
                                             "    OOG\n" +
                                             "WWW BGY RRO BRG\n" +
                                             "WWW BBY GYO BGG\n" +
                                             "WWW BOB YBG YBG\n" +
                                             "    RYR\n" +
                                             "    RRR\n" +
                                             "    RYO")
        evaluator = StageEvaluator(cube)
        stage = evaluator.determine_stage()
        self.assertEqual(StageEvaluator.STAGE_TOP_SOLVED, stage)
        self.assertEqual(1, len(evaluator.top_cross_candidates))
        self.assertEqual(Cube.LEFT, evaluator.top_cross_candidates[0])

    def test_determine_right_top_solved(self):
        # testing left at stage_top_solved
        cube = Parser().parse_string_to_cube("    OGY\n" +
                                             "    OOY\n" +
                                             "    OOG\n" +
                                             "WWW BGY RRO BRG\n" +
                                             "WWW BBY GYO BGG\n" +
                                             "WWW BOB YBG YBG\n" +
                                             "    RYR\n" +
                                             "    RRR\n" +
                                             "    RYO")
        cube.rotate_cube_ccw(2)

        evaluator = StageEvaluator(cube)
        stage = evaluator.determine_stage()
        self.assertEqual(StageEvaluator.STAGE_TOP_SOLVED, stage)
        self.assertEqual(1, len(evaluator.top_cross_candidates))
        self.assertEqual(Cube.RIGHT, evaluator.top_cross_candidates[0])

    def test_determine_front_top_solved(self):
        # testing left at stage_top_solved
        cube = Parser().parse_string_to_cube("    OGY\n" +
                                             "    OOY\n" +
                                             "    OOG\n" +
                                             "WWW BGY RRO BRG\n" +
                                             "WWW BBY GYO BGG\n" +
                                             "WWW BOB YBG YBG\n" +
                                             "    RYR\n" +
                                             "    RRR\n" +
                                             "    RYO")
        cube.rotate_cube_ccw()

        evaluator = StageEvaluator(cube)
        stage = evaluator.determine_stage()
        self.assertEqual(StageEvaluator.STAGE_TOP_SOLVED, stage)
        self.assertEqual(1, len(evaluator.top_cross_candidates))
        self.assertEqual(Cube.FRONT, evaluator.top_cross_candidates[0])

    def test_determine_back_top_solved(self):
        # testing left at stage_top_solved
        cube = Parser().parse_string_to_cube("    OGY\n" +
                                             "    OOY\n" +
                                             "    OOG\n" +
                                             "WWW BGY RRO BRG\n" +
                                             "WWW BBY GYO BGG\n" +
                                             "WWW BOB YBG YBG\n" +
                                             "    RYR\n" +
                                             "    RRR\n" +
                                             "    RYO")
        cube.rotate_cube_cw()

        evaluator = StageEvaluator(cube)
        stage = evaluator.determine_stage()
        self.assertEqual(StageEvaluator.STAGE_TOP_SOLVED, stage)
        self.assertEqual(1, len(evaluator.top_cross_candidates))
        self.assertEqual(Cube.BACK, evaluator.top_cross_candidates[0])

    def test_determine_bottom_top_solved(self):
        # testing left at stage_top_solved
        cube = Parser().parse_string_to_cube("    OGY\n" +
                                             "    OOY\n" +
                                             "    OOG\n" +
                                             "WWW BGY RRO BRG\n" +
                                             "WWW BBY GYO BGG\n" +
                                             "WWW BOB YBG YBG\n" +
                                             "    RYR\n" +
                                             "    RRR\n" +
                                             "    RYO")
        cube.rotate_cube_ccw()
        cube.rotate_cube_forward()

        evaluator = StageEvaluator(cube)
        stage = evaluator.determine_stage()
        self.assertEqual(StageEvaluator.STAGE_TOP_SOLVED, stage)
        self.assertEqual(1, len(evaluator.top_cross_candidates))
        self.assertEqual(Cube.BOTTOM, evaluator.top_cross_candidates[0])

    def test_determine_top_top_solved(self):
        # testing left at stage_top_solved
        cube = Parser().parse_string_to_cube("    OGY\n" +
                                             "    OOY\n" +
                                             "    OOG\n" +
                                             "WWW BGY RRO BRG\n" +
                                             "WWW BBY GYO BGG\n" +
                                             "WWW BOB YBG YBG\n" +
                                             "    RYR\n" +
                                             "    RRR\n" +
                                             "    RYO")
        cube.rotate_cube_ccw()
        cube.rotate_cube_backward()

        evaluator = StageEvaluator(cube)
        stage = evaluator.determine_stage()
        self.assertEqual(StageEvaluator.STAGE_TOP_SOLVED, stage)
        self.assertEqual(1, len(evaluator.top_cross_candidates))
        self.assertEqual(Cube.TOP, evaluator.top_cross_candidates[0])


class TestTopCrossSolver(unittest.TestCase):

    def test_count_completed(self):
        cube = Parser().parse_string_to_cube("    YWB\n" +
                                             "    WWW\n" +
                                             "    YWG\n" +
                                             "BRG OBY ROR YGO\n" +
                                             "ORR GBB YOY GGB\n" +
                                             "ORR GOO BRB ROG\n" +
                                             "    WYW\n" +
                                             "    BYY\n" +
                                             "    WGW")
        solver = TopCrossSolver(cube)
        self.assertEquals(4, solver.count_completed())

        cube = Parser().parse_string_to_cube("    BGY\n" +
                                             "    RWG\n" +
                                             "    RYO\n" +
                                             "YBB WBG WOG OWR\n" +
                                             "WRR GBY GOW RGO\n" +
                                             "YBY BYG WYW OOR\n" +
                                             "    OOR\n" +
                                             "    WYR\n" +
                                             "    GBB")
        solver = TopCrossSolver(cube)
        self.assertEqual(0, solver.count_completed())

    def test_is_done(self):
        cube = Parser().parse_string_to_cube("    YWB\n" +
                                             "    WWW\n" +
                                             "    YWG\n" +
                                             "BRG OBY ROR YGO\n" +
                                             "ORR GBB YOY GGB\n" +
                                             "ORR GOO BRB ROG\n" +
                                             "    WYW\n" +
                                             "    BYY\n" +
                                             "    WGW")
        solver = TopCrossSolver(cube)
        self.assertTrue(solver.is_done())
        cube.rotate_cube_forward()
        self.assertTrue(solver.is_done())

    def test_find_candidate_1(self):
        cube = Parser().parse_string_to_cube("    BGY\n" +
                                             "    RWG\n" +
                                             "    RYO\n" +
                                             "YBB WBG WOG OWR\n" +
                                             "WRR GBY GOW RGO\n" +
                                             "YBY BYG WYW OOR\n" +
                                             "    OOR\n" +
                                             "    WYR\n" +
                                             "    GBB")
        solver = TopCrossSolver(cube)
        side_name, coordinates = solver.find_candidate()
        self.assertIn((side_name, coordinates),
                      {(Cube.LEFT, (1, 0)),
                       (Cube.RIGHT, (1, 2)),
                       (Cube.BACK, (0, 1)),
                       (Cube.BOTTOM, (1, 0))})

    def test_is_top_candidate_solved(self):
        cube = Parser().parse_string_to_cube("    RWY\n" +
                                             "    WWW\n" +
                                             "    WWB\n" +
                                             "YGO GBW RRO BOG\n" +
                                             "BRB OBG YOB YGR\n" +
                                             "ROY ORR BGW OOW\n" +
                                             "    GYY\n" +
                                             "    YYR\n" +
                                             "    GGB")
        solver = TopCrossSolver(cube)

        self.assertEquals(1, solver.count_completed())

        self.assertFalse(solver.is_top_candidate_solved((0, 1)))
        self.assertFalse(solver.is_top_candidate_solved((1, 0)))
        self.assertFalse(solver.is_top_candidate_solved((1, 2)))
        self.assertTrue(solver.is_top_candidate_solved((2, 1)))

    def test_find_candidate_2(self):
        cube = Parser().parse_string_to_cube("    WWG\n" +
                                             "    BWO\n" +
                                             "    OOW\n" +
                                             "OYB YGG RWW OBB\n" +
                                             "YRB RBR WOG RGR\n" +
                                             "GBR WWY OYB YOY\n" +
                                             "    BGG\n" +
                                             "    OYG\n" +
                                             "    RYR")
        solver = TopCrossSolver(cube)
        side_name, coordinates = solver.find_candidate()
        self.assertIn((side_name, coordinates),
                      {(Cube.FRONT, (2, 1)),
                       (Cube.RIGHT, (0, 1)),
                       (Cube.TOP, (0, 1)),
                       (Cube.RIGHT, (1, 0))})

    def test_solve_top_cross_1(self):
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

        self.assertEqual(StageEvaluator.STAGE_0,
                         StageEvaluator(evaluator.cube).determine_stage())

        top_cross_solver = TopCrossSolver(cube)
        top_cross_solver.solve()
        top = top_cross_solver.cube.top
        top_cross_complete = all(top.get_center_color() == color for color in
                           [top.cubies[0][1], top.cubies[1][0], top.cubies[1][2], top.cubies[2][1]])
        top_cross_complete = top_cross_complete and all(side.get_center_color() == side.cubies[0][1]
                                                        for side in [top_cross_solver.cube.front,
                                                                     top_cross_solver.cube.left,
                                                                     top_cross_solver.cube.right,
                                                                     top_cross_solver.cube.back])
        self.assertTrue(top_cross_complete)

        self.assertTrue(top_cross_solver.is_done())
        self.assertEquals((None, None), top_cross_solver.find_candidate())
        self.assertEquals(4, top_cross_solver.count_completed())

    def test_solve_top_cross_2(self):
        cube = Parser().parse_string_to_cube("    WWG\n" +
                                             "    BWO\n" +
                                             "    OOW\n" +
                                             "OYB YGG RWW OBB\n" +
                                             "YRB RBR WOG RGR\n" +
                                             "GBR WWY OYB YOY\n" +
                                             "    BGG\n" +
                                             "    OYG\n" +
                                             "    RYR")

        evaluator = StageEvaluator(cube)

        self.assertEqual(StageEvaluator.STAGE_0,
                         StageEvaluator(evaluator.cube).determine_stage())

        top_cross_solver = TopCrossSolver(cube)
        top_cross_solver.solve()
        top = top_cross_solver.cube.top
        top_cross_complete = all(top.get_center_color() == color for color in
                           [top.cubies[0][1], top.cubies[1][0], top.cubies[1][2], top.cubies[2][1]])
        top_cross_complete = top_cross_complete and all(side.get_center_color() == side.cubies[0][1]
                                                        for side in [top_cross_solver.cube.front,
                                                                     top_cross_solver.cube.left,
                                                                     top_cross_solver.cube.right,
                                                                     top_cross_solver.cube.back])
        self.assertTrue(top_cross_complete)

        self.assertTrue(top_cross_solver.is_done())
        self.assertEquals((None, None), top_cross_solver.find_candidate())
        self.assertEquals(4, top_cross_solver.count_completed())

    def test_solve_top_cross_3(self):
        cube = Parser().parse_string_to_cube("    RWY\n" +
                                             "    WWW\n" +
                                             "    WWB\n" +
                                             "YGO GOW RRO BBG\n" +
                                             "BRB OBG YOB YGR\n" +
                                             "ROY ORR BGW OOW\n" +
                                             "    GYY\n" +
                                             "    YYR\n" +
                                             "    GGB")

        evaluator = StageEvaluator(cube)

        self.assertEqual(StageEvaluator.STAGE_0,
                         StageEvaluator(evaluator.cube).determine_stage())

        top_cross_solver = TopCrossSolver(cube)
        top_cross_solver.solve()
        top = top_cross_solver.cube.top
        top_cross_complete = all(top.get_center_color() == color for color in
                           [top.cubies[0][1], top.cubies[1][0], top.cubies[1][2], top.cubies[2][1]])
        top_cross_complete = top_cross_complete and all(side.get_center_color() == side.cubies[0][1]
                                                        for side in [top_cross_solver.cube.front,
                                                                     top_cross_solver.cube.left,
                                                                     top_cross_solver.cube.right,
                                                                     top_cross_solver.cube.back])
        self.assertTrue(top_cross_complete)

        self.assertTrue(top_cross_solver.is_done())
        self.assertEquals((None, None), top_cross_solver.find_candidate())
        self.assertEquals(4, top_cross_solver.count_completed())


class TestTopSolver(unittest.TestCase):

    def test_init_raises_assertion(self):
        cube = Parser().parse_string_to_cube("    OOG\n" +
                                             "    BWG\n" +
                                             "    GYY\n" +
                                             "GRR WGR GWW OYY\n" +
                                             "ROO GGB WRO WBW\n" +
                                             "YYB ORW OGW BBB\n" +
                                             "    YYB\n" +
                                             "    BYR\n" +
                                             "    ROR")
        with self.assertRaises(AssertionError) as context:
            TopCornerSolver(cube)
        self.assertTrue("Top cross not solved" in str(context.exception))

    def test_is_done(self):
        cube = Parser().parse_string_to_cube("    OGY\n" +
                                             "    OOY\n" +
                                             "    OOG\n" +
                                             "WWW BGY RRO BRG\n" +
                                             "WWW BBY GYO BGG\n" +
                                             "WWW BOB YBG YBG\n" +
                                             "    RYR\n" +
                                             "    RRR\n" +
                                             "    RYO")
        solver = TopCornerSolver(cube, WHITE)
        done = solver.is_done()
        self.assertTrue(done)

    def test_solve_1(self):
        cube = Parser().parse_string_to_cube("    YWB\n" +
                                             "    WWW\n" +
                                             "    YWG\n" +
                                             "BRG OBY ROR YGO\n" +
                                             "ORR GBB YOY GGB\n" +
                                             "ORR GOO BRB ROG\n" +
                                             "    WYW\n" +
                                             "    BYY\n" +
                                             "    WGW")
        solver = TopCornerSolver(cube, WHITE)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_2(self):
        cube = Parser().parse_string_to_cube("    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "BRO GBG ROB OGR\n" +
                                             "BRB RBY ROG YGY\n" +
                                             "RGY BYR BOG YBG\n" +
                                             "    OOY\n" +
                                             "    RYG\n" +
                                             "    YOO")
        solver = TopCornerSolver(cube, WHITE)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_3(self):
        cube = Parser().parse_string_to_cube("    BWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "YGG RRR BBB OOR\n" +
                                             "GGR BRG OBY ROY\n" +
                                             "BOY YBG YOG OGY\n" +
                                             "    GYO\n" +
                                             "    BYY\n" +
                                             "    ORW")
        solver = TopCornerSolver(cube, WHITE)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_count_complete_corners(self):
        cube = Parser().parse_string_to_cube("    YWB\n" +
                                             "    WWW\n" +
                                             "    YWG\n" +
                                             "BRG OBY ROR YGO\n" +
                                             "ORR GBB YOY GGB\n" +
                                             "ORR GOO BRB ROG\n" +
                                             "    WYW\n" +
                                             "    BYY\n" +
                                             "    WGW")
        solver = TopCornerSolver(cube, WHITE)
        self.assertEquals(0, solver.count_completed_corners())

        cube = Parser().parse_string_to_cube("    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "ORR BBG ROB OGG\n" +
                                             "BRB RBY ROG YGY\n" +
                                             "RGY BYR BOG YBG\n" +
                                             "    OOY\n" +
                                             "    RYG\n" +
                                             "    YOO")
        solver = TopCornerSolver(cube, WHITE)
        self.assertEquals(1, solver.count_completed_corners())

        cube = Parser().parse_string_to_cube("    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "BRO GBG ROB OGR\n" +
                                             "BRB RBY ROG YGY\n" +
                                             "RGY BYR BOG YBG\n" +
                                             "    OOY\n" +
                                             "    RYG\n" +
                                             "    YOO")
        solver = TopCornerSolver(cube, WHITE)
        solver.solve()
        self.assertEquals(4, solver.count_completed_corners())

    def test_find_candidate_1(self):
        cube = Parser().parse_string_to_cube("    YWB\n" +
                                             "    WWW\n" +
                                             "    YWG\n" +
                                             "BRG OBY ROR YGO\n" +
                                             "ORR GBB YOY GGB\n" +
                                             "ORR GOO BRB ROG\n" +
                                             "    WYW\n" +
                                             "    BYY\n" +
                                             "    WGW")
        solver = TopCornerSolver(cube, WHITE)
        side_name, coords = solver.find_candidate()
        # test that we got back a valid candidate, order independent
        self.assertIn((side_name, coords), {(Cube.BOTTOM, (0, 0)),
                                            (Cube.BOTTOM, (0, 2)),
                                            (Cube.BOTTOM, (2, 0)),
                                            (Cube.BOTTOM, (2, 2))})

    def test_find_candidate_2(self):
        cube = Parser().parse_string_to_cube("    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "BRO GBG ROB OGR\n" +
                                             "BRB RBY ROG YGY\n" +
                                             "RGY BYR BOG YBG\n" +
                                             "    OOY\n" +
                                             "    RYG\n" +
                                             "    YOO")
        solver = TopCornerSolver(cube, WHITE)
        side_name, coords = solver.find_candidate()
        # test that we got back a valid candidate, order independent
        self.assertIn((side_name, coords), {(Cube.TOP, (0, 0)),
                                            (Cube.TOP, (0, 2)),
                                            (Cube.TOP, (2, 0)),
                                            (Cube.TOP, (2, 2))})

    def test_find_candidate_3(self):
        cube = Parser().parse_string_to_cube("    YWY\n" +
                                             "    WWW\n" +
                                             "    YWR\n" +
                                             "BRB RBW GOR GGO\n" +
                                             "BRG RBO YOR BGY\n" +
                                             "ORW BOO BOO WGY\n" +
                                             "    RBW\n" +
                                             "    YYG\n" +
                                             "    GYG")
        solver = TopCornerSolver(cube, WHITE)
        side_name, coords = solver.find_candidate()
        # test that we got back a valid candidate, order independent
        self.assertIn((side_name, coords), {(Cube.LEFT, (2, 0)),
                                            (Cube.FRONT, (0, 2)),
                                            (Cube.BACK, (2, 0)),
                                            (Cube.BOTTOM, (0, 2))})

    def test_find_candidate_4(self):
        cube = Parser().parse_string_to_cube("    WWG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "BBB OOO GGY RRR\n" +
                                             "BBB OOR GGO GRY\n" +
                                             "OBW RYR BYO GYB\n" +
                                             "    GOY\n" +
                                             "    RYG\n" +
                                             "    YRY")
        solver = TopCornerSolver(cube, WHITE)
        side_name, coords = solver.find_candidate()
        # test that we got back a valid candidate, order independent
        self.assertIn((side_name, coords), {(Cube.LEFT, (2, 2))})
        self.assertEquals(3, solver.count_completed_corners())

    def test_find_candidate_excludes_solved_corners(self):
        cube = Parser().parse_string_to_cube("    OGY\n" +
                                             "    OOY\n" +
                                             "    OOG\n" +
                                             "WWW BGY RRO BRG\n" +
                                             "WWW BBY GYO BGG\n" +
                                             "WWW BOB YBG YBG\n" +
                                             "    RYR\n" +
                                             "    RRR\n" +
                                             "    RYO")
        solver = TopCornerSolver(cube, WHITE)
        # should not return a candidate if all corners are done
        side_name, coords = solver.find_candidate()
        self.assertIsNone(side_name)
        self.assertIsNone(coords)

    def test_is_top_corner_solved(self):
        cube = Parser().parse_string_to_cube("    OGY\n" +
                                             "    OOY\n" +
                                             "    OOG\n" +
                                             "WWW BGY RRO BRG\n" +
                                             "WWW BBY GYO BGG\n" +
                                             "WWW BOB YBG YBG\n" +
                                             "    RYR\n" +
                                             "    RRR\n" +
                                             "    RYO")
        solver = TopCornerSolver(cube, WHITE)
        # should be true if top corner is in correct position
        self.assertTrue(solver.is_top_corner_solved((0, 0)))
        self.assertTrue(solver.is_top_corner_solved((0, 2)))
        self.assertTrue(solver.is_top_corner_solved((2, 0)))
        self.assertTrue(solver.is_top_corner_solved((2, 2)))

        cube = Parser().parse_string_to_cube("    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "BRO GBG ROB OGR\n" +
                                             "BRB RBY ROG YGY\n" +
                                             "RGY BYR BOG YBG\n" +
                                             "    OOY\n" +
                                             "    RYG\n" +
                                             "    YOO")

        solver = TopCornerSolver(cube, WHITE)
        # should be true if top corner is in correct position
        self.assertFalse(solver.is_top_corner_solved((0, 0)))
        self.assertFalse(solver.is_top_corner_solved((0, 2)))
        self.assertFalse(solver.is_top_corner_solved((2, 0)))
        self.assertFalse(solver.is_top_corner_solved((2, 2)))

        # should only consider solved if it is actually the top color
        cube = Parser().parse_string_to_cube("    OGY\n" +
                                             "    OOY\n" +
                                             "    OOG\n" +
                                             "WWB BGY RRO WRG\n" +
                                             "WWW BBY GYO BGG\n" +
                                             "WWW BOB YBG YBG\n" +
                                             "    RYR\n" +
                                             "    RRR\n" +
                                             "    RYO")

        solver = TopCornerSolver(cube, WHITE)
        # should be true if top corner is in correct position
        self.assertTrue(solver.is_top_corner_solved((0, 0)))
        self.assertFalse(solver.is_top_corner_solved((0, 2)))
        self.assertTrue(solver.is_top_corner_solved((2, 0)))
        self.assertTrue(solver.is_top_corner_solved((2, 2)))


class TestSecondRowSolver(unittest.TestCase):

    def test_init_raises_assertion(self):
        cube = Parser().parse_string_to_cube("    OOG\n" +
                                             "    BWG\n" +
                                             "    GYY\n" +
                                             "GRR WGR GWW OYY\n" +
                                             "ROO GGB WRO WBW\n" +
                                             "YYB ORW OGW BBB\n" +
                                             "    YYB\n" +
                                             "    BYR\n" +
                                             "    ROR")
        with self.assertRaises(AssertionError) as context:
            TopCornerSolver(cube)
        self.assertTrue("not solved" in str(context.exception))

    def test_is_done_1(self):
        cube = Parser().parse_string_to_cube("    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "RRR BBB OOO GGG\n" +
                                             "YRY GBB OOB RGB\n" +
                                             "RRY BGY GGG YYY\n" +
                                             "    ORR\n" +
                                             "    YYO\n" +
                                             "    BOO")
        solver = SecondRowSolver(cube, WHITE)
        self.assertFalse(solver.is_done())

    def test_is_done_2(self):
        cube = Parser().parse_string_to_cube("    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "RRR BBB OOO GGG\n" +
                                             "RRR BBB OOO GGG\n" +
                                             "YYB OYY OGB YRR\n" +
                                             "    YBG\n" +
                                             "    OYY\n" +
                                             "    GYR")
        solver = SecondRowSolver(cube, WHITE)
        self.assertTrue(solver.is_done())

    def test_count_completed_1(self):
        cube = Parser().parse_string_to_cube("    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "RRR BBB OOO GGG\n" +
                                             "YRY GBB OOB RGB\n" +
                                             "RRY BGY GGG YYY\n" +
                                             "    ORR\n" +
                                             "    YYO\n" +
                                             "    BOO")
        solver = SecondRowSolver(cube, WHITE)
        self.assertEquals(1, solver.count_completed())

    def test_count_completed_2(self):
        cube = Parser().parse_string_to_cube("    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "RRR BBB OOO GGG\n" +
                                             "RRR BBB OOO GGG\n" +
                                             "YYB OYY OGB YRR\n" +
                                             "    YBG\n" +
                                             "    OYY\n" +
                                             "    GYR")
        solver = SecondRowSolver(cube, WHITE)
        self.assertEquals(4, solver.count_completed())

    def test_find_candidate(self):
        # cube will be flipped if yellow is not already
        # on top, so flipping beforehand to simplify my
        # thinkin as i build test cases
        cube = Parser().parse_string_to_cube("    ROY\n" +
                                             "    YYG\n" +
                                             "    YRG\n" +
                                             "YRO BGO YYB RBG\n" +
                                             "OOY BBO YRB RGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW")
        solver = SecondRowSolver(cube, WHITE)
        candidate = solver.find_candidate()
        self.assertIn(candidate,
                      [{Cube.RIGHT, Cube.BACK},
                       {Cube.FRONT, Cube.TOP},
                       {Cube.TOP, Cube.BACK}])

    def test_solve_1(self):
        # cube will be flipped if yellow is not already
        # on top, so flipping beforehand to simplify my
        # thinking as i build test cases
        cube = Parser().parse_string_to_cube("    ROY\n" +
                                             "    YYG\n" +
                                             "    YRG\n" +
                                             "YRO BGO YYB RBG\n" +
                                             "OOY BBO YRB RGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW")
        solver = SecondRowSolver(cube, WHITE)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_2(self):
        # cube will be flipped if yellow is not already
        # on top, so flipping beforehand to simplify my
        # thinking as i build test cases
        cube = Parser().parse_string_to_cube("    RYY\n" +
                                             "    YYY\n" +
                                             "    OBO\n" +
                                             "BOB YOY GGR GRY\n" +
                                             "ROG RBB YRO GGB\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW")
        solver = SecondRowSolver(cube, WHITE)
        solver.solve()
        self.assertTrue(solver.is_done())


class TestBottomCrossSolver(unittest.TestCase):

    def test_is_done(self):
        cube = Parser().parse_string_to_cube("    BYB\n" +
                                             "    YYR\n" +
                                             "    RGG\n" +
                                             "YBG YYO YYY OOR\n" +
                                             "BBB RRR GGG OOO\n" +
                                             "BBB RRR GGG OOO\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW")
        solver = BottomCrossSolver(cube)
        self.assertFalse(solver.is_done())

        cube = Parser().parse_string_to_cube("       OOY\n" +
                                             "       YYB\n" +
                                             "       YYY\n" +
                                             "   GGR GRO BYB RYY\n" +
                                             "   GGG OOO BBB RRR\n" +
                                             "   GGG OOO BBB RRR\n" +
                                             "       WWW\n" +
                                             "       WWW\n" +
                                             "       WWW\n")
        solver = BottomCrossSolver(cube)
        self.assertFalse(solver.is_done())

        cube = Parser().parse_string_to_cube("       YYR\n" +
                                             "       YYY\n" +
                                             "       YYY\n" +
                                             "   BBR GGG OOY BRO\n" +
                                             "   GGG OOO BBB RRR\n" +
                                             "   GGG OOO BBB RRR\n" +
                                             "       WWW\n" +
                                             "       WWW\n" +
                                             "       WWW\n")
        solver = BottomCrossSolver(cube)
        self.assertTrue(solver.is_done())

    def test_solve_1(self):
        cube = Parser().parse_string_to_cube("    BYB\n" +
                                             "    YYR\n" +
                                             "    RGG\n" +
                                             "YBG YYO YYY OOR\n" +
                                             "BBB RRR GGG OOO\n" +
                                             "BBB RRR GGG OOO\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW")
        solver = BottomCrossSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_2(self):
        cube = Parser().parse_string_to_cube("       YYR\n" +
                                             "       YYY\n" +
                                             "       YYY\n" +
                                             "   BBR GGG OOY BRO\n" +
                                             "   GGG OOO BBB RRR\n" +
                                             "   GGG OOO BBB RRR\n" +
                                             "       WWW\n" +
                                             "       WWW\n" +
                                             "       WWW\n")
        solver = BottomCrossSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_3(self):
        cube = Parser().parse_string_to_cube("       YYR\n" +
                                             "       YYY\n" +
                                             "       YYY\n" +
                                             "   BBR GGG OOY BRO\n" +
                                             "   GGG OOO BBB RRR\n" +
                                             "   GGG OOO BBB RRR\n" +
                                             "       WWW\n" +
                                             "       WWW\n" +
                                             "       WWW\n")
        solver = BottomCrossSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_4(self):
        cube = Parser().parse_string_to_cube("       OOY\n" +
                                             "       YYB\n" +
                                             "       YYY\n" +
                                             "   GGR GRO BYB RYY\n" +
                                             "   GGG OOO BBB RRR\n" +
                                             "   GGG OOO BBB RRR\n" +
                                             "       WWW\n" +
                                             "       WWW\n" +
                                             "       WWW\n")
        solver = BottomCrossSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())


class TestBottomCornerSolver(unittest.TestCase):

    def test_is_done(self):
        cube = Parser().parse_string_to_cube("    GYR\n" +
                                             "    YYY\n" +
                                             "    BYR\n" +
                                             "YOY ORY BGG YBO\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        self.assertFalse(solver.is_done())

        cube = Parser().parse_string_to_cube("    BYO\n" +
                                             "    YYY\n" +
                                             "    YYG\n" +
                                             "YRR GBO YGB YOR\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        self.assertFalse(solver.is_done())

        cube = Parser().parse_string_to_cube("    YYY\n" +
                                             "    YYY\n" +
                                             "    YYY\n" +
                                             "OGO BBB ROR GRG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        self.assertTrue(solver.is_done())

    def test_count_corners_complete(self):
        cube = Parser().parse_string_to_cube("    GYR\n" +
                                             "    YYY\n" +
                                             "    BYR\n" +
                                             "YOY ORY BGG YBO\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        self.assertEquals(0, solver.count_corners_complete())

        cube = Parser().parse_string_to_cube("    BYO\n" +
                                             "    YYY\n" +
                                             "    YYG\n" +
                                             "YRR GBO YGB YOR\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        self.assertEquals(1, solver.count_corners_complete())

        cube = Parser().parse_string_to_cube("    YYY\n" +
                                             "    YYY\n" +
                                             "    YYY\n" +
                                             "OGO BBB ROR GRG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        self.assertEquals(4, solver.count_corners_complete())

        cube = Parser().parse_string_to_cube("    OYR\n" +
                                             "    YYY\n" +
                                             "    BYB\n" +
                                             "GBY OGR YRG YOY\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        self.assertEquals(0, solver.count_corners_complete())

        cube = Parser().parse_string_to_cube("    RYY\n" +
                                             "    YYY\n" +
                                             "    RYY\n" +
                                             "BRG YBG OGO BOY\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        self.assertEquals(2, solver.count_corners_complete())

    def test_solve_1(self):
        cube = Parser().parse_string_to_cube("    GYR\n" +
                                             "    YYY\n" +
                                             "    BYR\n" +
                                             "YOY ORY BGG YBO\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_2(self):
        cube = Parser().parse_string_to_cube("    BYO\n" +
                                             "    YYY\n" +
                                             "    YYG\n" +
                                             "YRR GBO YGB YOR\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_3(self):
        cube = Parser().parse_string_to_cube("    YYY\n" +
                                             "    YYY\n" +
                                             "    YYY\n" +
                                             "OGO BBB ROR GRG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_4(self):
        cube = Parser().parse_string_to_cube("    OYR\n" +
                                             "    YYY\n" +
                                             "    BYB\n" +
                                             "GBY OGR YRG YOY\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_5(self):
        cube = Parser().parse_string_to_cube("    RYY\n" +
                                             "    YYY\n" +
                                             "    RYY\n" +
                                             "BRG YBG OGO BOY\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())


class TestBottomCornerPositionSolver(unittest.TestCase):

    def test_is_done(self):
        cube = Parser().parse_string_to_cube("    YYY\n" +
                                             "    YYY\n" +
                                             "    YYY\n" +
                                             "RGO BBR GOG ORB\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerPositionSolver(cube)
        self.assertFalse(solver.is_done())

        cube = Parser().parse_string_to_cube("    YYY\n" +
                                             "    YYY\n" +
                                             "    YYY\n" +
                                             "OOO BRB RGR GBG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerPositionSolver(cube)
        self.assertTrue(solver.is_done())

    def test_solve_1(self):
        cube = Parser().parse_string_to_cube("    YYY\n" +
                                             "    YYY\n" +
                                             "    YYY\n" +
                                             "RGO BBR GOG ORB\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerPositionSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_2(self):
        cube = Parser().parse_string_to_cube("    YYY\n" +
                                             "    YYY\n" +
                                             "    YYY\n" +
                                             "ROO BRR GGG OBB\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerPositionSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_2(self):
        cube = Parser().parse_string_to_cube("    YYY\n" +
                                             "    YYY\n" +
                                             "    YYY\n" +
                                             "ROO BRR GGG OBB\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerPositionSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_3(self):
        cube = Parser().parse_string_to_cube("    YYY\n" +
                                             "    YYY\n" +
                                             "    YYY\n" +
                                             "GOB RRO BGG OBR\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerPositionSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_4(self):
        cube = Parser().parse_string_to_cube("    YYY\n" +
                                             "    YYY\n" +
                                             "    YYY\n" +
                                             "RRO BGG OBR GOB\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerPositionSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())

    def test_solve_5(self):
        cube = Parser().parse_string_to_cube("    YYY\n" +
                                             "    YYY\n" +
                                             "    YYY\n" +
                                             "OBB ROO BRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "OOO BBB RRR GGG\n" +
                                             "    WWW\n" +
                                             "    WWW\n" +
                                             "    WWW\n")
        solver = BottomCornerPositionSolver(cube)
        solver.solve()
        self.assertTrue(solver.is_done())


if __name__ == '__main__':
    # logging.getLogger().setLevel(logging.DEBUG)
    # logging.basicConfig()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestStageEvaluator)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTopCrossSolver)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTopSolver)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSecondRowSolver)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBottomCrossSolver)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBottomCornerSolver)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBottomCornerPositionSolver)
    unittest.TextTestRunner(verbosity=2).run(suite)
