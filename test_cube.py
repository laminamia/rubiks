import unittest
import rubiks
import logging


class TestCube(unittest.TestCase):

    def test_move_front_cw(self):

        c1 = rubiks.Cube.create_solved_cube()
        c1.rotate_front_cw()
        logging.getLogger().warning("Right\n%r", c1.right)
        logging.getLogger().warning("Bottom\n%r", c1.bottom)
        logging.getLogger().warning("Left\n%r", c1.left)
        logging.getLogger().warning("Top\n%r", c1.top)

        for row in c1.right.cubies:
            self.assertEquals(row[0], rubiks.WHITE)

        for color in c1.bottom.cubies[0]:
            self.assertEquals(color, rubiks.ORANGE)

        for row in c1.left.cubies:
            self.assertEquals(row[2], rubiks.YELLOW)

        for color in c1.top.cubies[2]:
            self.assertEquals(color, rubiks.RED)

        # todo: test front rotation


class TestColor(unittest.TestCase):

    def test_eq(self):

        c1 = rubiks.Color("W", None)
        c2 = rubiks.Color("W", "Something")

        self.assertEqual(c1, c2)


class TestSide(unittest.TestCase):

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


if __name__== '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCube)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSide)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestColor)
    unittest.TextTestRunner(verbosity=2).run(suite)