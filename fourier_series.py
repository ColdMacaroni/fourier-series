#!/usr/bin/env python3

##
# fourier_series.py
# coords = coordinates
import pygame
import math

class Circle:
    def __init__(self):
        # HELP
        pass

def xy(x, y):
    """
    A shortcut to center_coords and py_coords.
    """
    return py_coords(center_coords((x, y)))


def un_xy(x, y):
    """
    does the opposite of xy
    """
    return un_center_coords(py_coords((x, y)))


def center_coords(coords, plane=None):
    """
    Repositions coords to the centre of the given plane
    """
    if plane is None:
        width, height = screen_size()
    else:
        width, height = plane[0], plane[1]

    return (width/2 + coords[0], height/2 + coords[1])


def un_center_coords(coords, plane=None):
    """
    Repositions coords to the bottom left of the plane
    """
    if plane is None:
        width, height = screen_size()
    else:
        width, height = plane[0], plane[1]

    return (coords[0] - width/2, coords[1] - height/2)


def py_coords(coords):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    height = screen_size()[1]
    return (coords[0], height - coords[1])


def un_py_coords(coords):
    """Convert coordinates into cardinal coordinates (top-left => lower left)."""
    height = screen_size()[1]
    return (coords[0], height + coords[1])


def draw_hollow_circle(screen, color, coords, radius, height=None, stroke=1):
    """
    Draws a circle with its centre at the x y coordinates.
    """
    width = radius * 2

    if height is None:
        height = width

    # Make center at the given coordinates
    x = coords[0] - width/2
    y = coords[1] - height/2

    # Create the Rect object
    rect = pygame.Rect((x, y), (width, height))

    pygame.draw.arc(screen, color, rect, 0, 2*math.pi)


def draw_radius(screen, color, coords, radius, radian, return_coords=False):
    """
    Draws the radius of a circle based on the radian given and the
    original coordinates.
    Returns the coordinates in the circumference if keyword is
    given
    """
    # The radian has to be negative to make it go the right way
    # I have no idea why but there it is.
    # Probably something to do with the pygame coordinates
    radian *= -1

    # Get coordinates at circumference
    x = coords[0] + radius * math.cos(radian)
    y = coords[1] + radius * math.sin(radian)

    # y is negative because y coordinates in pygame go the other way
    pygame.draw.line(screen, color, coords, (x, y))

    if return_coords:
        return un_xy(x, y)


def screen_size():
    """
    Set screen size
    """
    return 600, 600


def main():
    pygame.init()

    size = width, height = screen_size()

    color = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'light_gray': (100, 100, 100),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255)
    }

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    time = 120
    counter = 0
    increment = 2*math.pi / time

    dp = 5
    dots = []
    first = None
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill(color['white'])

        # -- Draw elements -- #
        # When `counter` reaches `time` a circle with a constant of one
        # Would have done a full revolution
        # e.g. if time=120, the const is 1, and clock.tick is 60 it
        # will take 2 seconds to do a full revolution
        counter += 1

        # Graph axes
        # X
        pygame.draw.line(screen, color['light_gray'], xy(-width/2, 0), xy(width/2, 0))

        # Y
        pygame.draw.line(screen, color['light_gray'], xy(0, height/2), xy(0, -height/2))

        # Circles
        draw_hollow_circle(screen, color['black'], xy(0, 0), 50)
        new_x, new_y = draw_radius(screen, color['red'], xy(0, 0), 50, 1 * counter * increment, True)

        draw_hollow_circle(screen, color['black'], xy(new_x, new_y), 50)
        new_x, new_y = draw_radius(screen, color['red'], xy(new_x, new_y), 50, -0.8 * counter * increment, True)

        point = (round(new_x, dp), round(new_y, dp))

        if point not in dots:
            dots.append(point)

        if first is None:
            prev = first = point

        # TODO: Find out why the last dot connects to the first always
        for dot in dots:
            pygame.draw.line(screen, color['green'], xy(*prev), xy(*dot))

            pygame.draw.circle(screen, color['blue'], xy(*dot), 1)
            prev = dot

        # print(len(dots))
        # -- Draw end -- #

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
