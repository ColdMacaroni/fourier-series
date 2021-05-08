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
    c = sum(new_pts)
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

cps = [[(0, 0), (4.68822, -9.06797), (-2.60655, -10.18185), (-0.86152, -14.39585)],
       [(-0.86152, -14.39585), (0.8835100000000001, -18.609859999999998), (8.46781, -15.32504), (10.4117, -25.99175)],
       [(10.4117, -25.99175), (11.38365, -31.32511), (-1.7129100000000008, -33.283), (-6.197120000000002, -33.69267)],
       [(-6.197120000000002, -33.69267), (-8.024570000000002, -33.72337), (-1.3975600000000021, -41.27619), (-3.4131400000000016, -41.8501)],
       [(-3.4131400000000016, -41.8501), (-5.391580000000001, -42.413439999999994), (-8.796000000000001, -33.98813), (-9.790690000000001, -34.42445)],
       [(-9.790690000000001, -34.42445), (-11.541890000000002, -35.19261), (-8.633310000000002, -44.75384), (-11.418510000000001, -44.5681)],
       [(-11.418510000000001, -44.5681), (-14.203710000000001, -44.38237), (-10.0447, -34.64056), (-13.802760000000001, -35.66668)],
       [(-13.802760000000001, -35.66668), (-17.07917, -36.53915), (-21.80949, -48.9543), (-31.314968, -44.86435)],
       [(-31.314968, -44.86435), (-40.820442, -40.77441), (-30.980815, -26.08339), (-33.413413, -22.514460000000003)],
       [(-33.413413, -22.514460000000003), (-35.846016, -18.945530000000005), (-46.755883999999995, -19.800270000000005), (-42.848062, -7.631140000000004)],
       [(-42.848062, -7.631140000000004), (-38.940239999999996, 4.537989999999995), (-22.777549999999998, -8.283880000000003), (-18.48756, -5.400100000000004)],
       [(-18.48756, -5.400100000000004), (-14.197569999999999, -2.516320000000004), (-5.773999999999999, 9.133679999999996), (0.0, 2.9999999996199733e-05)]]

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
