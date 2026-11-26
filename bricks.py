import math
from cadquery import func as cf

def clutch_brick(length, width, height, stud_d, stud_h, spacing):
    body = cf.box(length, width, height)

    brick = body

    # 2 × 4 studs
    for row in range(2):
        for col in range(4):
            stud = cf.cylinder(d=stud_d, h=stud_h)

            x = (col - 1.5) * spacing      # 4 columns
            y = (row - 0.5) * spacing      # 2 rows

            brick = brick + stud.moved(x=x, y=y, z=height)

    return brick


brick = clutch_brick(
    length=31.2,   # 4 studs long
    width=15.6,    # 2 studs wide
    height=9.6,
    stud_d=4.8,
    stud_h=1.7,
    spacing=8.0
)

# Volume = body volume + volume of 8 studs
expected = (
    31.2 * 15.6 * 9.6
    + 8 * math.pi * (4.8 / 2) ** 2 * 1.7
)

assert abs(brick.Volume() - expected) < 0.5

brick.exportStl("brick.stl")

print("2x4 brick created successfully