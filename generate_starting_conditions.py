#!/usr/bin/env python3
# Generate starting sequences for fourier series
import math
from sys import argv
import svg_to_readable


def cubic_bezier(arg_points, t):
    """
    Returns the point
    """
    coords = []
    p0, p1, p2, p3 = arg_points
    # for x and then y
    for i in [0, 1]:
        # Equation from
        # https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Cubic_B%C3%A9zier_curves
        num = (((1 - t)**3) * p0[i])\
             + (3 * t * ((1 - t)**2) * p1[i])\
             + (3 * (t**2) * (1 - t) * p2[i])\
             + ((t**3) * p3[i])

        coords.append(num)

    return tuple(coords)


def generate_points(control_points, increment):
    _points = []

    t = -increment
    while t <= 1:
        _points.append(cubic_bezier(control_points, t))

        t += increment

    return _points


def integral(pts, n):
    new_pts = []

    inc = 1 / len(pts)

    # To make first val 0
    t = -inc

    # Multiply the formula for every circle we want the constant for
    # with each value of pts
    for pt in pts:
        t += inc
        new_pts.append(
            pt * pow(math.e, n * -1 * 2 * math.pi * 1j * t)
        )

    # To get the average we dont divide because its from values 0 to 1. x/1 = x
    c = sum(new_pts)
    return c


def write_complex(num):
    with open(filename, 'a') as file:
        if num.imag < 0:
            line = "{}{}j".format(num.real, num.imag)
        else:
            line = "{}+{}j".format(num.real, num.imag)

        file.write(line + ';')


def coords_to_complex(coords):
    num = coords[0] + coords[1] * 1j
    return num


# TODO: Normalize values
try:
    filename = argv[1]
except IndexError:
    filename = input("Filename of svg file: ")

cps = svg_to_readable.main(filename)

try:
    # Try to read the increment from args
    resolution = abs(float(argv[4])) ** -1

# Sorry for weird formatting, pep8
except IndexError:
    resolution = abs(
        float(
            input("Enter the resolution. "
                  "A higher number is better, but slower: ").strip()
        )
    ) ** -1

except ValueError:
    resolution = abs(
        float(
            input("Enter the resolution. "
                  "A higher number is better, but slower. "
                  "It should be a positive number: ").strip()
        )
    ) ** -1

# This will sequentially create all points.
# They'll be one after the other
raw_points = []
for cp in cps:
    raw_points += generate_points(cp, resolution)

# NOTE: This will be removed once normalizing values is implemented
# The size handling and all that should be done form the
# fourier_series.py file

# Scale the svg
try:
    factor = float(argv[3])
except IndexError:
    factor = float(input("Enter a scale factor for the svg: "))

except ValueError:
    print("Make sure the factor is a float. E.g. 0.7")
    factor = input("Scale factor: ")

# Flip y axis, svgs are upside down for some reason
points = [(coord[0] * factor, coord[1] * -factor) for coord in raw_points]

# -- Move points to 0, 0 -- #
target = (0, 0)

# Split list into x and y
x_points = [x[0] for x in points]
y_points = [y[1] for y in points]

# Get average
x_avg = sum(x_points) / len(x_points)
y_avg = sum(y_points) / len(y_points)

# Find diff from 0,0
x_diff = target[0] - x_avg
y_diff = target[1] - y_avg

new_x = [coord + x_diff for coord in x_points]

# Apply that diff to all points

# profit

# --

exit()

points = [coords_to_complex(x) for x in points]

# Now we have the points in order and in imaginary plane
constants = []
try:
    numbers = int(argv[2])

except IndexError:
    numbers = abs(int(input("Enter the amount of pairs of circles: ")))

except ValueError:
    numbers = abs(int(input("Enter the amount of pairs of circles. "
                            "Must be an integer: ")))

for n in range(0, numbers + 1):
    # Generate the circles
    constants.append(integral(points, n))

    # Create an "opposite" circle right next to
    # the current one
    if n != 0:
        constants.append(integral(points, n * -1))

# By the end, the values would look like
# 0
# 1
# -1
# 2
# -2
# etc.s

# Clear file
filename = 'constants'
with open(filename, 'w') as file:
    file.write('')

for i in range(len(constants)):
    print(i, constants[i])
    write_complex(constants[i])
