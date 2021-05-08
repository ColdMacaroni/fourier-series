#!/usr/bin/env python3
# Generate starting sequences for fourier series

def write_complex(file, num):
    if num.imag < 0:
        line = "{}{}j".format(num.real, num.imag)
    else:
        line = "{}+{}j".format(num.real, num.imag)

    file.write(line)


def coords_to_complex(coords):
    num = coords[0] + coords[1] * 1j
    return num

file = open('constants', 'a')

avg_pt = (-13.399837757, 25.824553376666657)

first = coords_to_complex(avg_pt)

write_complex(file, first)


