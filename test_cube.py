import unittest
from rubiks import *
import logging


class TestCube(unittest.TestCase):

    def setUp(self):

        # Make up some random sides
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
        self.cube = Cube(front=Side.create_copy(self.front),
                  back=Side.create_copy(self.back),
                  left=Side.create_copy(self.left),
                  right=Side.create_copy(self.right),
                  top=Side.create_copy(self.top),
                  bottom=Side.create_copy(self.bottom))


    def test_move_front_cw(self):
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

    def test_move_front_ccw(self):
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

    def test_rotate_cube_back(self):
        expected = Cube(top=self.front,
                        front=self.bottom,
                        back=self.top.copy().inverse(),
                        bottom=self.back.copy().inverse(),
                        left=self.left.copy().rotate_face_colors_ccw(),
                        right=self.right.copy().rotate_face_colors_cw())

        self.run_test_manipulation(self.cube.rotate_cube_back, expected)

    def run_test_manipulation(self, manipulation_fn, expected_cube):

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

        manipulation_fn()

        logging.getLogger().debug("Cube after manipulation\n\n")
        logging.getLogger().debug("Right\n%r", self.cube.right)
        logging.getLogger().debug("Bottom\n%r", self.cube.bottom)
        logging.getLogger().debug("Left\n%r", self.cube.left)
        logging.getLogger().debug("Top\n%r", self.cube.top)
        logging.getLogger().debug("Front\n%r", self.cube.front)
        logging.getLogger().debug("Back\n%r", self.cube.back)

        self.assertEqual(expected_cube.front, self.cube.front, "Front not as expected")
        self.assertEqual(expected_cube.back, self.cube.back, "Back not as expected")
        self.assertEqual(expected_cube.left, self.cube.left, "Left not as expected")
        self.assertEqual(expected_cube.right, self.cube.right, "Right not as expected")
        self.assertEqual(expected_cube.top, self.cube.top, "Top not as expected")
        self.assertEqual(expected_cube.bottom, self.cube.bottom, "Bottom not as expected")


class TestColor(unittest.TestCase):

    def test_eq(self):
        c1 = Color("W", None)
        c2 = Color("W", "Something")

        self.assertEqual(c1, c2)


class TestSide(unittest.TestCase):

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

        self.assertEqual(s1, Side.create_copy(s1))
        self.assertIsNot(s1, Side.create_copy(s1))
        self.assertEqual(s1, s1.copy())
        self.assertIsNot(s1, s1.copy())

    def test_inverse(self):
        s1 = Side([[RED, BLUE, GREEN],
                   [YELLOW, WHITE, ORANGE],
                   [BLUE, GREEN, YELLOW]])
        s2 = Side([[YELLOW, GREEN, BLUE],
                   [ORANGE, WHITE, YELLOW],
                   [GREEN, BLUE, RED]])
        self.assertEqual(s2, s1.inverse())

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


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCube)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSide)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestColor)
    unittest.TextTestRunner(verbosity=2).run(suite)
