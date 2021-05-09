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


def write_complex(num, filename):
    with open(filename, 'a') as file:
        if num.imag < 0:
            line = "{}{}j".format(num.real, num.imag)
        else:
            line = "{}+{}j".format(num.real, num.imag)

        file.write(line + ';')


def coords_to_complex(coords):
    num = coords[0] + coords[1] * 1j
    return num


def split_xy(pts):
    """
    Returns all x points in one list and all y points in one list
    """
    x_points = [x[0] for x in pts]
    y_points = [y[1] for y in pts]
    return x_points, y_points


def move_to_target(pts, target=(0, 0)):
    """
    This function changes a set of points' center to the
    target coordinates
    """
    # -- Move points to 0, 0 -- #
    # Split list into x and y
    x_points, y_points = split_xy(pts)

    # Get average
    x_avg = sum(x_points) / len(x_points)
    y_avg = sum(y_points) / len(y_points)

    # Find diff from 0,0
    x_diff = target[0] - x_avg
    y_diff = target[1] - y_avg

    new_x = [coord + x_diff for coord in x_points]
    new_y = [coord + y_diff for coord in y_points]

    return list(zip(new_x, new_y))


def get_biggest_range(*values):
    """
    Returns the biggest range from the list of values.
    """
    ranges = []
    for value in values:
        ranges.append(max(value) - min(value))

    return max(ranges)


def normalize_coords(pts):
    """
    Normalizes a bunch of points
    """
    x_points, y_points = split_xy(pts)
    distance = get_biggest_range(x_points, y_points)

    # Theres probably a better way to do this. Too bad!

    # Start with x values
    new_x = []
    min_x = min(x_points)
    max_x = min_x + distance

    for x in x_points:
        new_x.append((x-min_x)/(max_x-min_x))

    # Continue with y values
    new_y = []
    min_y = min(y_points)
    max_y = min_y + distance

    for y in y_points:
        new_y.append((y - min_y) / (max_y - min_y))

    return list(zip(new_x, new_y))


def normalize(min_val, max_val, value):
    return (value - min_val) / (max_val - min_val)


def main():
    try:
        filename = argv[1]
    except IndexError:
        filename = input("Filename of svg file: ")

    # The pt_type will specific if to call cubic_bezier or linear
    # quadratic beziers not yet supported
    cps, pt_type = svg_to_readable.main(filename)

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

    # Flip y axis, svgs are upside down for some reason
    points = [(coord[0], coord[1] * -1) for coord in raw_points]

    # Normalize points
    points = normalize_coords(points)

    print(points)

    # Move it to 0, 0
    points = [(coord[0] - .5, coord[1] - .5) for coord in points]

    # Convert the coordinates to complex numbers
    complex_points = [coords_to_complex(x) for x in points]

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
        constants.append(integral(complex_points, n))

        # Create an "opposite" circle right next to
        # the current one
        if n != 0:
            constants.append(integral(complex_points, n * -1))

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
        write_complex(constants[i], filename)


if __name__ == "__main__":
    main()