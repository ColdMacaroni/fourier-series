#!/usr/bin/env python3
# Generate starting sequences for fourier series
import math


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


# The average of the points
# See https://github.com/ColdMacaroni/pygame-bezier
avg_pt = (-13.399837757, 25.824553376666657)

# Calculate the value c0
static = coords_to_complex(avg_pt)

constants = []

# Amount of circles
amount = 10
for n in range(0, amount + 1):
    const = static * pow(math.e, (n * -1) * 2 * math.pi * 1j)
    constants.append(const)

for i in range(len(constants)):
    print(i, constants[i])
    write_complex(constants[i])
