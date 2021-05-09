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


def list_d(ls):
    """
    Turns d into a list
    """
    # Processed items will go in here
    new_ls = []

    # Support for when the coordinates are divided by commas
    ls = ls.replace(",", " ")
    items = ls.split(" ")

    for item in items:
        # Leave string items as they are
        if item.isalpha():
            new_ls.append(item)

        # Convert nums to actual nums
        else:
            coordinate = float(item.strip())

            new_ls.append(coordinate)

    return new_ls


def tuplify_d(ls):
    """
    Convert a list given by sep_commands into using coordinates
    in tuples instead of standalone
    """
    new_ls = []
    for item in ls:
        print(item)
        new_item = [item[0]]

        # Go 2 by 2 to add the coords together
        for pos in range(1, len(item), 2):
            # Convert to tuple
            coord = item[pos], item[pos + 1]

            new_item.append(coord)

        print(new_item)
        print()

        new_ls.append(new_item)
    return new_ls


def sep_commands(ls):
    """
    Creates 2D lists for each svg command
    """
    new_ls = []
    last = 0
    for i in range(len(ls)):
        # When it encounters a string, it will add the previous
        # section to the new list
        if isinstance(ls[i], str):
            to_append = ls[last:i]
            # Only add if the list is not empty
            if to_append:
                new_ls.append(to_append)
                last = i

    print(new_ls, "sep_commands")
    return new_ls


def relative_to_absolute(sep_ls):
    """
    Taking a list generated from sep_commands(), convert
    the values to absolute ones
    """
    pass


def separate_points(sep_ls):
    """
    Taking a list generated from sep_commands(), it'll convert
    the commands to separate continuous ones
    """
    # Shortcuts
    horiz = lambda x: ['l', [(x, 0)]]
    verti = lambda y: ['l', [(0, y)]]

    # The minimum amount of attributes each has
    # coms is short for commands
    coms = {
        "m": 1,  # Move

        "l": 1,  # Line to
        "h": 1,  # Horizontal
        "v": 1,  # Vertical

        "c": 3,  # Cubic bezier
        "s": 2,  # Smooth cubic bezier

        "q": 2,  # Quadratic bezier
    }

    new_ls = []
    for item in sep_ls:
        com = item[0].lower()
        start = coms[com]
        for i in range(1, len(item), coms[com]):
            # Do this to avoid appending empty lists
            to_append = item[start:i]
            if to_append:
                new_ls.append([item[0], to_append])

            start = i

    return new_ls


def main(filename):
    # Get the content of d
    d_markers = get_d(filename)

    # Hehe
    d_list = list_d(d_markers)

    # Group per command type
    separated_list = sep_commands(d_list)

    # Convert coordinates to tuples
    processed_list = tuplify_d(separated_list)

    # Convert shorthand commands to full ones
    command_list = separate_points(processed_list)

    # Convert relative values to absolute ones


    return command_list


if __name__ == "__main__":
    print(main(argv[1]))
