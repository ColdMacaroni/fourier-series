#!/bin/python

##
# fourier_series.py
# coords = coordinates
import pygame
import math


def xy(x, y):
    """
    A shortcut to center_coords and py_coords.
    """
    return py_coords(center_coords((x, y)))


def center_coords(coords, plane=None):
    """
    Repositions coords to the centre of the given plane
    """
    if plane is None:
        width, height = screen_size()
    else:
        width, height = plane[0], plane[1]

    return width/2 + coords[0], height/2 + coords[1]


def py_coords(coords):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    height = screen_size()[1]
    return (coords[0], height - coords[1])


def draw_hollow_circle(screen, color, coords, width, height, stroke=1):
    """
    Draws a circle with its centre at the x y coordinates.
    """
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
    # TODO: Make the anchor or something start from the centre
    pygame.draw.line(screen, color, coords, (x, y))

    if return_coords:
        return x, y


def screen_size():
    """
    Set screen size
    """
    return 600, 600


def main():
    pygame.init()

    time = 60

    size = width, height = screen_size()

    color = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'light_gray': (100, 100, 100),
        'red': (255, 0, 0)
    }

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    counter = 0
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill(color['white'])

        # -- Draw elements -- #
        if counter > 100:
            counter = 0
        else:
            counter += 1
        # Graph axes
        # X
        pygame.draw.line(screen, color['light_gray'], xy(-width/2, 0), xy(width/2, 0))

        # Y
        pygame.draw.line(screen, color['light_gray'], xy(0, height/2), xy(0, -height/2))

        draw_hollow_circle(screen, color['black'], xy(0, 0), 100, 100)

        draw_radius(screen, color['red'], xy(0, 0), 50, counter * 0.06283)
        # -- Draw end -- #

        pygame.display.flip()
        clock.tick(time)


if __name__ == "__main__":
    main()
