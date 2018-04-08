from rubiks import *
import re

Color.initialize(True)

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
cube = Cube(front=front, back=back, left=left, right=right, top=top, bottom=bottom)

print(cube)

s = "    YOG\n"+\
    "    OWW\n"+\
    "    BBW\n"+\
    "BGR YWR BOY RYO\n"+\
    "RRG RBB YOW GGW\n"+\
    "RBW GGW OYO GOW\n"+\
    "    OYB\n"+\
    "    RYR\n"+\
    "    GBY"

expr = re.compile("(\s*[yrbgwo]{3}[ \t]*\n){3}" +
                  "((\s*[yrbgwo]{3}[ \t]){4}\n){3}" +
                  "(\s*[yrbgwo]{3}\n){3}\s*", re.IGNORECASE)
print(expr.match(s))

lines = s.splitlines()
lines = [line.strip().upper() for line in lines]
print(lines)

top_lines = lines[:3]
print(top_lines)