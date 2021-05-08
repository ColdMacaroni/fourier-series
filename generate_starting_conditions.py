#!/usr/bin/env python3
# Generate starting sequences for fourier series
import math


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

    increment = 0.05
    t = -increment
    while t <= 1:
        points.append(cubic_bezier(*control_points, t))

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
    with open('constants', 'a') as file:
        if num.imag < 0:
            line = "{}{}j".format(num.real, num.imag)
        else:
            line = "{}+{}j".format(num.real, num.imag)

        file.write(line + ';')


def coords_to_complex(coords):
    num = coords[0] + coords[1] * 1j
    return num

cps = 

# This will sequentially create all points.
# They'll be one after the other
points = []
for cp in cps:
    points += generate_points(cp)

points = [coords_to_complex(x) for x in points]



# Now we have the points in order and in imaginary plane
constants = []
numbers = 50
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
#
for i in range(len(constants)):
    print(i, constants[i])
    write_complex(constants[i])
