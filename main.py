
import rubiks


front = rubiks.Side.create_unicolor_side(rubiks.BLUE)
back = rubiks.Side.create_unicolor_side(front.center_color().opposite())

left = rubiks.Side.create_unicolor_side(rubiks.RED)
right = rubiks.Side.create_unicolor_side(left.center_color().opposite())

top = rubiks.Side.create_unicolor_side(rubiks.WHITE)
bottom = rubiks.Side.create_unicolor_side(top.center_color().opposite())

print(front)
print(back)
print(left)
print(right)
print(top)
print(bottom)

cube = rubiks.Cube(front, back, left, right, top, bottom)

print(cube)
