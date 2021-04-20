#!/bin/python

##
# fourier_series.py
import pygame
import math


def draw_hollow_circle(screen, color, x, y, width, height, stroke=1):
    """
    Draws a circle with its centre at the x y coordinates.
    """
    coords = (x - width/2, y - height/2)

    # Create the Rect object
    rect = pygame.Rect(coords, (width, height))

    pygame.draw.arc(screen, color, rect, 0, 2*math.pi)


def draw_radius(screen, color, radian, radius, origin_x, origin_y, return_coords=False):
    """
    Draws the radius of a circle based on the radian given and the
    original coordinates.
    Returns the coordinates in the circumference if keyword is
    given
    """
    # Get coordinates at circumference
    x = origin_x + radius * math.cos(radian)
    y = origin_y + radius * math.sin(radian)

    if return_coords:
        return (x, y)


def main():
    pygame.init()

    size = width, height = 600, 600
    color = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'light_gray': (100, 100, 100)
    }

    center_x, center_y = width/2, height/2

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill(color['white'])

        # -- Draw elements -- #

        # Graph axes
        # X
        pygame.draw.line(screen, color['light_gray'], (0, center_y), (width, center_y))

        # Y
        pygame.draw.line(screen, color['light_gray'], (center_x, 0), (center_x, height))

        draw_hollow_circle(screen, color['black'], center_x, center_y, 100, 100)
        # -- Draw end -- #

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
