#!/usr/bin/env python3
# Generate starting sequences for fourier series
import math
from sys import argv
import svg_to_readable


def cubic_bezier(p0, p1, p2, p3, t):
    """
    Returns the point
    """
    coords = []
    # twice for x and then y
    for i in [0, 1]:
        # https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Cubic_B%C3%A9zier_curves
        num = (((1 - t)**3) * p0[i])\
             + (3 * t * ((1 - t)**2) * p1[i])\
             + (3 * (t**2) * (1 - t) * p2[i])\
             + ((t**3) * p3[i])

        coords.append(num)

    return tuple(coords)


def generate_points(control_points):
    _points = []

    try:
        increment = abs(float(argv[4]))

    except IndexError:
        print('Argument 4 should be the resolution for the bezier curve. '+
              'The closer to 0 the better.')
        exit(0)

    except ValueError:
        print('Argument 4 must be a float')
        exit(0)

    t = -increment
    while t <= 1:
        _points.append(cubic_bezier(*control_points, t))

        t += increment

    return _points


def integral(pts, n):
    new_pts = []

    inc = 1 / len(pts)

    # To make first val 0
    t = -inc
    for pt in pts:
        t += inc
        new_pts.append(
            pt * pow(math.e, n * -1 * 2 * math.pi * 1j * t)
        )
    c = sum(new_pts)/len(new_pts)
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


try:
    cps = svg_to_readable.main(argv[1])
except IndexError:
    print('Argument 1 should be an svg file')
    exit(0)


# This will sequentially create all points.
# They'll be one after the other
raw_points = []
for cp in cps:
    raw_points += generate_points(cp)

# Scale the svg
try:
    factor = float(argv[3])
except IndexError:
    print('Argument 3 should be the scaling factor for the points')
    exit(0)

except ValueError:
    print('Argument 3 must be a float')
    exit(0)

points = [(y[0] * factor, y[1] * -factor) for y in raw_points]

points = raw_points

points = [coords_to_complex(x) for x in points]

# Now we have the points in order and in imaginary plane
constants = []
try:
    numbers = int(argv[2])

except IndexError:
    print('Argument 2 should be half the amount of circles')
    exit(0)

except ValueError:
    print('Argument 2 must be an int')
    exit(0)

for n in range(0, numbers + 1):
    constants.append(integral(points, n))

    if n != 0:
        constants.append(integral(points, n * -1))

#for j in constants:
#    print(j)


# # The average of the points
# # See https://github.com/ColdMacaroni/pygame-bezier
# avg_pt = (0.5593747196325674, 0.5946344182531562)
#
# # Calculate the value c0
# static = coords_to_complex(avg_pt)
#
# constants = []
#
# # Amount of circles
# amount = 400
# for n in range(0, amount + 1):
#     const = static * pow(math.e, (n * -1) * 2 * math.pi * 1j)
#     constants.append(const)

# Clear file
filename = 'constants'
with open(filename, 'w') as file:
    file.write('')

for i in range(len(constants)):
    print(i, constants[i])
    write_complex(constants[i])
