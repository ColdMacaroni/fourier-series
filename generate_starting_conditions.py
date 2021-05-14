#!/usr/bin/env python3
# Generate starting sequences for fourier series
import math
import time
from sys import argv
import svg_parser


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
        svg_filename = argv[1]
    except IndexError:
        svg_filename = input("Filename of svg file: ")

    # Backup value
    resolution = 40

    try:
        resolution = float(argv[2])

    except IndexError:
        resolution = float(input("Enter a resolution, the higher the better: ").strip())

    raw_points = svg_parser.main(svg_filename, resolution)

    # Flip y axis, svgs are upside down for some reason
    points = [(coord[0], coord[1] * -1) for coord in raw_points]

    # Normalize points
    points = normalize_coords(points)

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
    start_time = time.time()
    for n in range(0, numbers + 1):
        # Generate the circles
        constants.append(integral(complex_points, n))

        # Create an "opposite" circle right next to
        # the current one
        if n != 0:
            constants.append(integral(complex_points, n * -1))
        if (timeout_time := time.time() - start_time) >= 60:
            print(f'timed out after {timeout_time*100:.7f}ms')
            break
    final_time = time.time() - start_time
    print(f'Circles created in {final_time*100:.7f}ms')

    # By the end, the values would look like
    # 0
    # 1
    # -1
    # 2
    # -2
    # etc.s

    # Clear file
    writing_filename = 'constants'
    with open(writing_filename, 'w') as file:
        file.write('')

    for i in range(len(constants)):
        print(i, constants[i])
        write_complex(constants[i], writing_filename)


if __name__ == "__main__":
    main()