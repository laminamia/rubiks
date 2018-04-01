import unittest
from rubiks import *
import logging


class TestCube(unittest.TestCase):

    def test_move_front_cw(self):
        # Make up some random sides
        front = Side([[YELLOW, WHITE, RED],
                      [RED, BLUE, BLUE],
                      [GREEN, GREEN, WHITE]])
        back = Side([[RED, YELLOW, ORANGE],
                     [GREEN, GREEN, WHITE],
                     [GREEN, ORANGE, WHITE]])
        left = Side([[BLUE, GREEN, RED],
                     [RED, RED, GREEN],
                     [RED, BLUE, WHITE]])
        right = Side([[BLUE, ORANGE, YELLOW],
                      [YELLOW, ORANGE, WHITE],
                      [ORANGE, YELLOW, ORANGE]])
        top = Side([[YELLOW, ORANGE, GREEN],
                    [ORANGE, WHITE, WHITE],
                    [BLUE, BLUE, WHITE]])
        bottom = Side([[ORANGE, YELLOW, BLUE],
                       [RED, YELLOW, RED],
                       [GREEN, BLUE, YELLOW]])

        # use copies in cube because the lists will be modified by cube manipulation
        c1 = Cube(front=Side.create_copy(front),
                  back=Side.create_copy(back),
                  left=Side.create_copy(left),
                  right=Side.create_copy(right),
                  top=Side.create_copy(top),
                  bottom=Side.create_copy(bottom))

        c1.rotate_front_cw()

        logging.getLogger().warning("Right\n%r", c1.right)
        logging.getLogger().warning("Bottom\n%r", c1.bottom)
        logging.getLogger().warning("Left\n%r", c1.left)
        logging.getLogger().warning("Top\n%r", c1.top)
        logging.getLogger().warning("Front\n%r", c1.front)
        logging.getLogger().warning("Back\n%r", c1.back)

        self.assertEqual(top.get_row(2), c1.right.get_column(0))
        self.assertEqual(bottom.get_row(0), c1.left.get_column(2))
        self.assertEqual(right.get_column(0), c1.bottom.get_row(0))
        self.assertEqual(left.get_column(2), c1.top.get_row(2))
        self.assertEqual(back, c1.back)

        self.assertEqual(c1.front, Side([[GREEN, RED, YELLOW],
                                         [GREEN, BLUE, WHITE],
                                         [WHITE, BLUE, RED]]))

    def test_move_front_ccw(self):
        # Make up some random sides
        front = Side([[YELLOW, WHITE, RED],
                      [RED, BLUE, BLUE],
                      [GREEN, GREEN, WHITE]])
        back = Side([[RED, YELLOW, ORANGE],
                     [GREEN, GREEN, WHITE],
                     [GREEN, ORANGE, WHITE]])
        left = Side([[BLUE, GREEN, RED],
                     [RED, RED, GREEN],
                     [RED, BLUE, WHITE]])
        right = Side([[BLUE, ORANGE, YELLOW],
                      [YELLOW, ORANGE, WHITE],
                      [ORANGE, YELLOW, ORANGE]])
        top = Side([[YELLOW, ORANGE, GREEN],
                    [ORANGE, WHITE, WHITE],
                    [BLUE, BLUE, WHITE]])
        bottom = Side([[ORANGE, YELLOW, BLUE],
                       [RED, YELLOW, RED],
                       [GREEN, BLUE, YELLOW]])

        # use copies in cube because the lists will be modified by cube manipulation
        c1 = Cube(front=Side.create_copy(front),
                  back=Side.create_copy(back),
                  left=Side.create_copy(left),
                  right=Side.create_copy(right),
                  top=Side.create_copy(top),
                  bottom=Side.create_copy(bottom))

        c1.rotate_front_ccw()

        logging.getLogger().warning("Right\n%r", c1.right)
        logging.getLogger().warning("Bottom\n%r", c1.bottom)
        logging.getLogger().warning("Left\n%r", c1.left)
        logging.getLogger().warning("Top\n%r", c1.top)
        logging.getLogger().warning("Front\n%r", c1.front)
        logging.getLogger().warning("Back\n%r", c1.back)

        self.assertEqual(top.get_row(2), c1.left.get_column(2))
        self.assertEqual(bottom.get_row(0), c1.right.get_column(0))
        self.assertEqual(right.get_column(0), c1.top.get_row(2))
        self.assertEqual(left.get_column(2), c1.bottom.get_row(0))
        self.assertEqual(back, c1.back)

        self.assertEqual(c1.front, Side([[RED, BLUE, WHITE],
                                         [WHITE, BLUE, GREEN],
                                         [YELLOW, RED, GREEN]]))

    def test_rotate_cube_right(self):
        # Make up some random sides
        front = Side([[YELLOW, WHITE, RED],
                      [RED, BLUE, BLUE],
                      [GREEN, GREEN, WHITE]])
        back = Side([[RED, YELLOW, ORANGE],
                     [GREEN, GREEN, WHITE],
                     [GREEN, ORANGE, WHITE]])
        left = Side([[BLUE, GREEN, RED],
                     [RED, RED, GREEN],
                     [RED, BLUE, WHITE]])
        right = Side([[BLUE, ORANGE, YELLOW],
                      [YELLOW, ORANGE, WHITE],
                      [ORANGE, YELLOW, ORANGE]])
        top = Side([[YELLOW, ORANGE, GREEN],
                    [ORANGE, WHITE, WHITE],
                    [BLUE, BLUE, WHITE]])
        bottom = Side([[ORANGE, YELLOW, BLUE],
                       [RED, YELLOW, RED],
                       [GREEN, BLUE, YELLOW]])

        # use copies in cube because the lists will be modified by cube manipulation
        c1 = Cube(front=Side.create_copy(front),
                  back=Side.create_copy(back),
                  left=Side.create_copy(left),
                  right=Side.create_copy(right),
                  top=Side.create_copy(top),
                  bottom=Side.create_copy(bottom))

        c1.rotate_cube_right()

        logging.getLogger().warning("Right\n%r", c1.right)
        logging.getLogger().warning("Bottom\n%r", c1.bottom)
        logging.getLogger().warning("Left\n%r", c1.left)
        logging.getLogger().warning("Top\n%r", c1.top)
        logging.getLogger().warning("Front\n%r", c1.front)
        logging.getLogger().warning("Back\n%r", c1.back)

        self.assertEqual(front, c1.right)
        self.assertEqual(right, c1.back)
        self.assertEqual(back, c1.left)
        self.assertEqual(left, c1.front)
        self.assertEqual(Side([[GREEN, WHITE, WHITE],
                               [ORANGE, WHITE, BLUE],
                               [YELLOW, ORANGE, BLUE]]), c1.top)
        self.assertEqual(Side([[GREEN, RED, ORANGE],
                               [BLUE, YELLOW, YELLOW],
                               [YELLOW, RED, BLUE]]), c1.bottom)

    def test_rotate_cube_left(self):
        # Make up some random sides
        front = Side([[YELLOW, WHITE, RED],
                      [RED, BLUE, BLUE],
                      [GREEN, GREEN, WHITE]])
        back = Side([[RED, YELLOW, ORANGE],
                     [GREEN, GREEN, WHITE],
                     [GREEN, ORANGE, WHITE]])
        left = Side([[BLUE, GREEN, RED],
                     [RED, RED, GREEN],
                     [RED, BLUE, WHITE]])
        right = Side([[BLUE, ORANGE, YELLOW],
                      [YELLOW, ORANGE, WHITE],
                      [ORANGE, YELLOW, ORANGE]])
        top = Side([[YELLOW, ORANGE, GREEN],
                    [ORANGE, WHITE, WHITE],
                    [BLUE, BLUE, WHITE]])
        bottom = Side([[ORANGE, YELLOW, BLUE],
                       [RED, YELLOW, RED],
                       [GREEN, BLUE, YELLOW]])

        # use copies in cube because the lists will be modified by cube manipulation
        c1 = Cube(front=Side.create_copy(front),
                  back=Side.create_copy(back),
                  left=Side.create_copy(left),
                  right=Side.create_copy(right),
                  top=Side.create_copy(top),
                  bottom=Side.create_copy(bottom))

        c1.rotate_cube_left()

        logging.getLogger().warning("Right\n%r", c1.right)
        logging.getLogger().warning("Bottom\n%r", c1.bottom)
        logging.getLogger().warning("Left\n%r", c1.left)
        logging.getLogger().warning("Top\n%r", c1.top)
        logging.getLogger().warning("Front\n%r", c1.front)
        logging.getLogger().warning("Back\n%r", c1.back)

        self.assertEqual(front, c1.left)
        self.assertEqual(left, c1.back)
        self.assertEqual(back, c1.right)
        self.assertEqual(right, c1.front)

        self.assertEqual(Side([[BLUE, ORANGE, YELLOW],
                               [BLUE, WHITE, ORANGE],
                               [WHITE, WHITE, GREEN]]), c1.top)
        self.assertEqual(Side([[BLUE, RED, YELLOW],
                               [YELLOW, YELLOW, BLUE],
                               [ORANGE, RED, GREEN]]), c1.bottom)


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


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCube)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSide)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestColor)
    unittest.TextTestRunner(verbosity=2).run(suite)
