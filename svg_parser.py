#!/usr/bin/env python3
# svg_parser.py
# A python program to generate points from and svg file
import bs4 as bs
from sys import argv


def get_d(filename):
    """
    Gets the contents of the attribute d of the first path
    it finds in the given svg file
    """
    source = open(filename, 'r')

    soup = bs.BeautifulSoup(source, 'xml')

    # This doesnt have support for multiple d or paths
    path = soup.find('path')

    ctrl_points = path.get('d')

    return ctrl_points


def tuplify_coords(ls):
    """
    Converts strings like "print(processed_list)0.4,-34" to (0.4, -34)
    """
    # Processed items will go in here
    new_ls = []

    items = ls.split(" ")
    for item in items:
        # Leave string items as they are
        if item.isalpha():
            new_ls.append(item)

        # Convert to tuple
        else:
            try:
                x, y = item.split(",")

                # Convert to a tuple with actual nums
                coordinate = float(x.strip()), float(y.strip())

            # There will be a value error if the item is just a number
            # without commas
            # This will happen when the value is from a horizontal or
            # vertical lineto
            except ValueError:
                coordinate = float(item.strip())

            new_ls.append(coordinate)
    return new_ls


def main(filename):
    # Get the content of d
    d_markers = get_d(filename)

    # Convert d to actual, usable data types
    processed_list = tuplify_coords(d_markers)




if __name__ == "__main__":
    main(argv[1])
