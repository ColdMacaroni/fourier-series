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

    paths = soup.findAll('path')

    ctrl_points = []
    for path in paths:
        ctrl_points.append(path.get('d'))

    return ctrl_points


def list_d(ls):
    """
    Turns d into a list
    """
    # Processed items will go in here
    new_ls = []

    # Support for when the coordinates are divided by commas
    # Z's are useless! (for our purpose)
    ls = ls.replace(",", " ").replace("z", "").replace("Z", "")
    items = list(ls)

    # "M0" -> "M 0"
    spaced_items = []

    # Add a space after each letter
    for item in items:
        spaced_items.append(item)
        if item.isalpha():
            spaced_items.append(" ")

    # Join and then split again to remove duplicate spaces
    items = ''.join(spaced_items).split()

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

    # horiz = lambda x: ['l', [(x, 0)]]
    # verti = lambda y: ['l', [(0, y)]]

    new_ls = []
    for item in ls:
        new_item = [item[0]]

        # There is probably a better way to do this but my brain power
        # has gone into the imaginary plane. (It's not real)
        if new_item[0].lower() == "h":
            for pos in range(1, len(item)):
                coord = (item[pos], 0)
                new_item.append(coord)

        elif new_item[0].lower() == "v":
            for pos in range(1, len(item)):
                coord = (0, item[pos])
                new_item.append(coord)

        else:
            # Horizontal and vertical need special handling
            # Go 2 by 2 to add the coords together
            for pos in range(1, len(item), 2):
                # Convert to tuple
                coord = item[pos], item[pos + 1]

                new_item.append(coord)

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

    # The last to_append doesnt usually get added at the end of the loop
    # unless the last item is a char
    # In case it does, the if should stop repeats hopefully
    if ls[last:i] != new_ls[-1]:
        new_ls.append(ls[last:i + 1])

    return new_ls


def add_xy(coord1, coord2):
    """
    Add two coordinates together
    """
    return coord1[0] + coord2[0], coord1[1] + coord2[1]


def relative_to_absolute(ls):
    """
    Taking a list generated from sep_commands(), convert
    the values to absolute ones. These include the current point
    as index 0
    """
    # ls will look like
    # [["m", [(0, 0)]], ["c", [(1, 1), (2, 2), (3, 3), (4, 4)]]
    # ls[0][0] = "m"
    # ls[0][1] = [(0, 0)]
    # ls[0][1][0] = (0, 0)

    new_ls = []

    #
    # # Set the current position to the one it was moved to
    # if ls[0][0].lower() == "m":
    #     current = ls[0][1][0]
    #
    #     # After getting this value, the move part is useless
    #     del ls[0]

    current = (0, 0)

    for i in range(0, len(ls)):
        # M/m requires special handling
        # If the move is absolute
        if ls[i][0] == "M":
            # Set coords for the point it was moved to
            current = ls[i][1][0]

        # Relative
        elif ls[i][0] == "m":
            current = add_xy(current, ls[i][1][0])

        # Hh/Vv also requires special handling
        # It will convert the command to a Lineto instead
        elif ls[i][0].lower() in ["h", "v"]:
            new_coords = [current]

            # Horizontals (x, 0)
            if ls[i][0] == "H":
                # Yes, a 4D list. I couldnt think of anything else
                # its accessing the x value of the horizontal line

                # Replace the y value for the current one
                coord = (ls[i][1][0][0], current[1])

            elif ls[i][0] == "V":
                # Replace x for current one
                coord = (current[0], ls[i][1][0][1])

            else:
                # Replace the 0 value AND make specified absolute
                coord = (add_xy(ls[i][1][0], current))
            # Verticals (0, y)

            new_coords.append(coord)

            new_ls.append(['l', new_coords])

            # Set current to latest coordinate
            current = new_ls[-1][1][-1]

        else:
            # Set the first value to
            new_coords = [current]

            # lower case are relatives. Upper are absolute
            if ls[i][0].islower():

                # Add the current value to each coordinate
                for coord in ls[i][1]:
                    new_coords.append(add_xy(current, coord))

            else:
                # Item is already absolute, no changes needed
                new_coords += ls[i][1]

            # Add the new values, including the command char
            # Command char's case doesnt matter now so it is turned to
            # lower for ease of use
            new_ls.append([ls[i][0].lower(), new_coords])

            # Set current to latest coordinate
            current = new_ls[-1][1][-1]

    return new_ls


def separate_points(sep_ls):
    """
    Taking a list generated from sep_commands(), it'll convert
    the commands to separate continuous ones
    """
    # NOTE: This can be used for h and v support
    # Shortcuts
    # horiz = lambda x: ['l', [(x, 0)]]
    # verti = lambda y: ['l', [(0, y)]]

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
        "t": 1,  # Smooth quadratic bezier
    }

    new_ls = []
    for item in sep_ls:
        # Z doesnt really matter!
        if item[0].lower() == "z":
            continue

        com = item[0].lower()

        # Start is one to avoid the command character
        start = 1
        # Get sections of length coms[com]
        for i in range(0, (len(item) - 1) // coms[com]):
            to_append = item[start: start + coms[com]]

            new_ls.append([item[0], to_append])

            start += coms[com]

    return new_ls


# -- Equations -- #
def line(arg_points, t):
    """
    Returns the point according to t
    """
    # Wanted a useful docstring? Too bad!
    coords = []
    p0, p1 = arg_points

    # for x and then y
    # What's programming without a little mischief?
    for i in [0, 1]:
        # https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Linear_B%C3%A9zier_curves
        num = p0[i] + t * (p1[i] - p0[i])

        coords.append(num)

    return tuple(coords)


def cubic_bezier(arg_points, t):
    """
    Returns the point according to t
    """
    coords = []
    p0, p1, p2, p3 = arg_points

    # for x and then y
    for i in [0, 1]:
        # Equation from
        # https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Cubic_B%C3%A9zier_curves

        # TODO: Change these to pow()
        num = (((1 - t) ** 3) * p0[i]) \
              + (3 * t * ((1 - t) ** 2) * p1[i]) \
              + (3 * (t ** 2) * (1 - t) * p2[i]) \
              + ((t ** 3) * p3[i])

        coords.append(num)

    return tuple(coords)


def quadratic_bezier(arg_points, t):
    """
    Returns the point according to t
    """
    coords = []
    p0, p1, p2 = arg_points

    # For x and then y
    for i in [0, 1]:
        # https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Quadratic_B%C3%A9zier_curves
        num = (pow(1 - t, 2) * p0[i])\
              + (2 * (1 - t) * t * p1[i])\
              + (pow(t, 2) * p2[i])

        coords.append(num)

    return tuple(coords)

# --


def not_supported(*args):
    """
    Sorry!!
    """
    raise Exception('Sorry!! There is not support for this '
                    f'svg command yet!! ({args[0]}) Please create an '
                    'issue on github.')


def main(filename, resolution):
    # Get the content of d
    all_d_points = get_d(filename)

    abs_points = []
    for d_markers in all_d_points:
        # Hehe
        d_list = list_d(d_markers)

        # Group per command type
        separated_list = sep_commands(d_list)

        # Convert coordinates to tuples
        processed_list = tuplify_d(separated_list)

        # Convert shorthand commands to full ones
        command_list = separate_points(processed_list)

        # Convert relative values to absolute ones
        absolute_list = relative_to_absolute(command_list)

        abs_points.append(absolute_list)

    all_points = []
    for control_points in abs_points:
        for control_point in control_points:
            all_points.append(control_point)

    # im tired

    # If i want to support s or t, id have to make a function to
    # convert them to c/q
    # https://www.w3.org/TR/SVG/paths.html#PathDataLinetoCommands
    # What equation to use for each

    equations = {
        # Line
        "l": line,
        "h": not_supported,
        "v": not_supported,

        # Cubic bezier
        "c": cubic_bezier,
        "s": not_supported,

        # Quadratic bezier
        "q": quadratic_bezier,
        "t": not_supported,
    }

    # Start calculating values
    points = []

    increment = pow(resolution, -1)
    for command in all_points:
        # Get relevant equation
        eq, args = command

        equation = equations[eq]

        # Calculate values
        t = 0
        while 0 <= t <= 1:
            points.append(equation(args, t))
            t += increment

    return points


if __name__ == "__main__":
    # A default value
    res = 20

    try:
        res = float(argv[2])

    # PEP 8: E722 do not use bare 'except'
    # Too bad!
    except:
        print("Using", res, "as resolution.")

    print(main(argv[1], res))
