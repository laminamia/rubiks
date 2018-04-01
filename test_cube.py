import unittest
import rubiks
import logging


class TestCube(unittest.TestCase):

    def test_move_front_cw(self):

        # Make up some random sides
        front = rubiks.Side([[rubiks.YELLOW, rubiks.WHITE, rubiks.RED],
                             [rubiks.RED, rubiks.BLUE, rubiks.BLUE],
                             [rubiks.GREEN, rubiks.GREEN, rubiks.WHITE]])
        back = rubiks.Side([[rubiks.RED, rubiks.YELLOW, rubiks.ORANGE],
                            [rubiks.GREEN, rubiks.GREEN, rubiks.WHITE],
                            [rubiks.GREEN, rubiks.ORANGE, rubiks.WHITE]])
        left = rubiks.Side([[rubiks.BLUE, rubiks.GREEN, rubiks.RED],
                            [rubiks.RED, rubiks.RED, rubiks.GREEN],
                            [rubiks.RED, rubiks.BLUE, rubiks.WHITE]])
        right = rubiks.Side([[rubiks.BLUE, rubiks.ORANGE, rubiks.YELLOW],
                             [rubiks.YELLOW, rubiks.ORANGE, rubiks.WHITE],
                             [rubiks.ORANGE, rubiks.YELLOW, rubiks.ORANGE]])
        top = rubiks.Side([[rubiks.YELLOW, rubiks.ORANGE, rubiks.GREEN],
                           [rubiks.ORANGE, rubiks.WHITE, rubiks.WHITE],
                           [rubiks.BLUE, rubiks.BLUE, rubiks.WHITE]])
        bottom = rubiks.Side([[rubiks.ORANGE, rubiks.YELLOW, rubiks.BLUE],
                              [rubiks.RED, rubiks.YELLOW, rubiks.RED],
                              [rubiks.GREEN, rubiks.BLUE, rubiks.YELLOW]])

        # use copies in cube because the lists will be modified by cube manipulation
        c1 = rubiks.Cube(front=rubiks.Side.create_copy(front),
                         back=rubiks.Side.create_copy(back),
                         left=rubiks.Side.create_copy(left),
                         right=rubiks.Side.create_copy(right),
                         top=rubiks.Side.create_copy(top),
                         bottom=rubiks.Side.create_copy(bottom))

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

        self.assertEqual(c1.front, rubiks.Side([[rubiks.GREEN, rubiks.RED, rubiks.YELLOW],
                                                [rubiks.GREEN, rubiks.BLUE, rubiks.WHITE],
                                                [rubiks.WHITE, rubiks.BLUE, rubiks.RED]]))

    def test_move_front_ccw(self):

        # Make up some random sides
        front = rubiks.Side([[rubiks.YELLOW, rubiks.WHITE, rubiks.RED],
                             [rubiks.RED, rubiks.BLUE, rubiks.BLUE],
                             [rubiks.GREEN, rubiks.GREEN, rubiks.WHITE]])
        back = rubiks.Side([[rubiks.RED, rubiks.YELLOW, rubiks.ORANGE],
                            [rubiks.GREEN, rubiks.GREEN, rubiks.WHITE],
                            [rubiks.GREEN, rubiks.ORANGE, rubiks.WHITE]])
        left = rubiks.Side([[rubiks.BLUE, rubiks.GREEN, rubiks.RED],
                            [rubiks.RED, rubiks.RED, rubiks.GREEN],
                            [rubiks.RED, rubiks.BLUE, rubiks.WHITE]])
        right = rubiks.Side([[rubiks.BLUE, rubiks.ORANGE, rubiks.YELLOW],
                             [rubiks.YELLOW, rubiks.ORANGE, rubiks.WHITE],
                             [rubiks.ORANGE, rubiks.YELLOW, rubiks.ORANGE]])
        top = rubiks.Side([[rubiks.YELLOW, rubiks.ORANGE, rubiks.GREEN],
                           [rubiks.ORANGE, rubiks.WHITE, rubiks.WHITE],
                           [rubiks.BLUE, rubiks.BLUE, rubiks.WHITE]])
        bottom = rubiks.Side([[rubiks.ORANGE, rubiks.YELLOW, rubiks.BLUE],
                              [rubiks.RED, rubiks.YELLOW, rubiks.RED],
                              [rubiks.GREEN, rubiks.BLUE, rubiks.YELLOW]])

        # use copies in cube because the lists will be modified by cube manipulation
        c1 = rubiks.Cube(front=rubiks.Side.create_copy(front),
                         back=rubiks.Side.create_copy(back),
                         left=rubiks.Side.create_copy(left),
                         right=rubiks.Side.create_copy(right),
                         top=rubiks.Side.create_copy(top),
                         bottom=rubiks.Side.create_copy(bottom))

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

        self.assertEqual(c1.front, rubiks.Side([[rubiks.RED, rubiks.BLUE, rubiks.WHITE],
                                                [rubiks.WHITE, rubiks.BLUE, rubiks.GREEN],
                                                [rubiks.YELLOW, rubiks.RED, rubiks.GREEN]]))

    def test_rotate_cube_right(self):
        # Make up some random sides
        front = rubiks.Side([[rubiks.YELLOW, rubiks.WHITE, rubiks.RED],
                             [rubiks.RED, rubiks.BLUE, rubiks.BLUE],
                             [rubiks.GREEN, rubiks.GREEN, rubiks.WHITE]])
        back = rubiks.Side([[rubiks.RED, rubiks.YELLOW, rubiks.ORANGE],
                            [rubiks.GREEN, rubiks.GREEN, rubiks.WHITE],
                            [rubiks.GREEN, rubiks.ORANGE, rubiks.WHITE]])
        left = rubiks.Side([[rubiks.BLUE, rubiks.GREEN, rubiks.RED],
                            [rubiks.RED, rubiks.RED, rubiks.GREEN],
                            [rubiks.RED, rubiks.BLUE, rubiks.WHITE]])
        right = rubiks.Side([[rubiks.BLUE, rubiks.ORANGE, rubiks.YELLOW],
                             [rubiks.YELLOW, rubiks.ORANGE, rubiks.WHITE],
                             [rubiks.ORANGE, rubiks.YELLOW, rubiks.ORANGE]])
        top = rubiks.Side([[rubiks.YELLOW, rubiks.ORANGE, rubiks.GREEN],
                           [rubiks.ORANGE, rubiks.WHITE, rubiks.WHITE],
                           [rubiks.BLUE, rubiks.BLUE, rubiks.WHITE]])
        bottom = rubiks.Side([[rubiks.ORANGE, rubiks.YELLOW, rubiks.BLUE],
                              [rubiks.RED, rubiks.YELLOW, rubiks.RED],
                              [rubiks.GREEN, rubiks.BLUE, rubiks.YELLOW]])

        # use copies in cube because the lists will be modified by cube manipulation
        c1 = rubiks.Cube(front=rubiks.Side.create_copy(front),
                         back=rubiks.Side.create_copy(back),
                         left=rubiks.Side.create_copy(left),
                         right=rubiks.Side.create_copy(right),
                         top=rubiks.Side.create_copy(top),
                         bottom=rubiks.Side.create_copy(bottom))

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

        # bottom and top
        self.assertEqual(c1.front, rubiks.Side([[rubiks.RED, rubiks.BLUE, rubiks.WHITE],
                                                [rubiks.WHITE, rubiks.BLUE, rubiks.GREEN],
                                                [rubiks.YELLOW, rubiks.RED, rubiks.GREEN]]))


class TestColor(unittest.TestCase):

    def test_eq(self):

        c1 = rubiks.Color("W", None)
        c2 = rubiks.Color("W", "Something")

        self.assertEqual(c1, c2)


class TestSide(unittest.TestCase):

    def test_get_row(self):
        rows = [[rubiks.YELLOW, rubiks.WHITE, rubiks.RED],
                [rubiks.RED, rubiks.BLUE, rubiks.BLUE],
                [rubiks.GREEN, rubiks.GREEN, rubiks.WHITE]]

        s = rubiks.Side(rows)

        for i in range(len(rows)):
            self.assertEqual(rows[i], s.get_row(i))

    def test_get_column(self):
        rows = [[rubiks.YELLOW, rubiks.WHITE, rubiks.RED],
                [rubiks.RED, rubiks.BLUE, rubiks.BLUE],
                [rubiks.GREEN, rubiks.GREEN, rubiks.WHITE]]

        s = rubiks.Side(rows)

        self.assertEqual([rubiks.YELLOW, rubiks.RED, rubiks.GREEN], s.get_column(0))
        self.assertEqual([rubiks.WHITE, rubiks.BLUE, rubiks.GREEN], s.get_column(1))
        self.assertEqual([rubiks.RED, rubiks.BLUE, rubiks.WHITE], s.get_column(2))

    def test_init(self):
        try:
            rubiks.Side([[]])
            self.fail("Didn't raise AssertionError")
        except AssertionError:
            pass

    def test_eq(self):
        s1 = rubiks.Side.create_unicolor_side(rubiks.RED)
        s2 = rubiks.Side.create_unicolor_side(rubiks.RED)
        self.assertEqual(s1, s2, "Two all Red sides should be equal")

        s2 = rubiks.Side.create_unicolor_side(rubiks.BLUE)
        self.assertNotEqual(s1, s2, "Red and Blue sides should not be equal")

        s2 = rubiks.Side([[rubiks.RED, rubiks.BLUE, rubiks.GREEN],
                     [rubiks.YELLOW, rubiks.WHITE, rubiks.ORANGE],
                     [rubiks.BLUE, rubiks.GREEN, rubiks.YELLOW]])
        self.assertNotEqual(s1, s2)

        s1 = rubiks.Side([[rubiks.RED, rubiks.BLUE, rubiks.GREEN],
                     [rubiks.YELLOW, rubiks.WHITE, rubiks.ORANGE],
                     [rubiks.BLUE, rubiks.GREEN, rubiks.YELLOW]])
        self.assertEqual(s1, s2)

    def test_copy(self):
        s1 = rubiks.Side([[rubiks.RED, rubiks.BLUE, rubiks.GREEN],
                          [rubiks.YELLOW, rubiks.WHITE, rubiks.ORANGE],
                          [rubiks.BLUE, rubiks.GREEN, rubiks.YELLOW]])

        self.assertEqual(s1, rubiks.Side.create_copy(s1))
        self.assertIsNot(s1, rubiks.Side.create_copy(s1))


if __name__== '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCube)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSide)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestColor)
    unittest.TextTestRunner(verbosity=2).run(suite)