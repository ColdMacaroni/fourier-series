#!/usr/bin/env python3

##
# fourier_series.py
# coords = coordinates
from typing import final
import pygame
import math
import random


class FirstArm:

    def __init__(self, screen, color=(255, 0, 0), counter=0,
                 increment=0, radius=50, constant=1, start_angle=0,
                 image_rot=0, line_color=(0, 0, 0), show_radii=True,
                 show_circumferences=True):
        """Creates a FirstArm object

        Args:
            screen (PyGame Screen variable): Variable for determining the
            Pygame window the arms are drawn on.

            color (tuple, optional): Determins the color of the arm in RGB
            form.
            Defaults to Red (255, 0, 0).

            counter (int, optional): I have no clue.
            Defaults to 0.

            increment (float): [description]. Defaults to 0.

            radius (float, optional): the length of the arm in px.
            Defaults to 50.

            constant (float, optional): .
            Defaults to 1.

            start_angle (int, optional): teh angle the arm starts at
            (in degrees).
            Defaults to 0.

            image_rot (int, optional): the amount you want to rotate the
            whole image by (in degrees).
            Defaults to 0.

            line_color (tuple, optional): Color of the line created in RGB
            form.
            Defaults to black (0, 0, 0).

            show_radii (bool, optional): whether or not teh arms themselves
            will be shown.
            Defaults to True.

            show_circumferences (bool, optional): whether or not the
            circumferences of this arm and all children arms will be shown.
            Defaults to True.
        """
        self.color = color
        self.screen = screen
        self.counter = counter
        self.increment = increment
        self.radius = radius
        self.constant = constant
        self.dots = []
        self.start_angle = deg_to_rads(start_angle)
        self.image_rot = deg_to_rads(image_rot)
        self.line_color = line_color
        self.show_radii = show_radii
        self.show_circumpferences = show_circumferences


        self.children = []

        self.new_x = {}
        self.new_y = {}

    def update(self):
        """Updates this arm and all child arms
        """
        self.new_x[1], self.new_y[1] = draw_radius(self.screen,
                                                   (255, 0, 0), xy(0, 0),
                                                   self.radius,
                                                   self.constant *
                                                   self.counter *
                                                   self.increment
                                                   + self.start_angle
                                                   + self.image_rot, True,
                                                   self.show_radii)
        if self.show_circumpferences:
            draw_hollow_circle(self.screen, (0, 0, 0), xy(0, 0), self.radius)
        self.counter += 1
        for child in self.children:
            child.update()
            new_x = self.new_x[child.id]
            new_y = self.new_y[child.id]





class arm:

    def __init__(self, parent, radius=50, dp=2, id=1, last=False, constant=1,
                 color=(255, 0, 0), start_angle=0):
        """[summary]

        Args:
            parent (FirstArm): Parent object of this arm must be a first arm.

            radius (int, optional): the length of the arm.
            Defaults to 50.

            dp (int, optional): Decimal places to round to.
            Defaults to 2.

            id (int, optional): Id of this arm minimum of 1.
            Defaults to 1.

            last (bool, optional): Is this the last arm of the chain.
            Defaults to False.

            constant (int, optional): The rotational constant of this arm.
            Defaults to 1.

            color (tuple, optional): Color of this arm.
            Defaults to Red (255, 0, 0).

            start_angle (int, optional): Angle this arm starts at(in degrees).
            Defaults to 0.
        """
        self.parent = parent
        self.radius = radius
        self.id = id
        self.parent.children.append(self)
        self.dp = dp
        self.last = last
        self.constant = constant
        self.prev = None
        self.color = color
        self.start_angle = deg_to_rads(start_angle)

    def update(self):
        """Updates this arm
        """
        new_x = self.parent.new_x
        new_y = self.parent.new_y
        id = self.id

        if self.parent.show_circumpferences:
            draw_hollow_circle(self.parent.screen, (0, 0, 0), xy(new_x[id],
                                                                 new_y[id]),
                               self.radius)
        new_x[id+1], new_y[id+1] = draw_radius(self.parent.screen, self.color,
                                               xy(new_x[id], new_y[id]),
                                               self.radius, self.constant *
                                               self.parent.counter *
                                               self.parent.increment +
                                               self.start_angle +
                                               self.parent.image_rot, True,
                                               self.parent.show_radii)
        if self.last:
            self.point = (round(new_x[id+1], self.dp), round(new_y[id+1], self.dp))

            if self.point not in self.parent.dots:
                self.parent.dots.append(self.point)
            dots = self.parent.dots
            for dot in dots:
                self.next = None
                try:
                    self.next = dots[dots.index(dot)+1]
                except IndexError:
                    continue
                if self.next is not None:
                    pygame.draw.line(self.parent.screen, self.parent.line_color, xy(*dot), xy(*self.next))


def units_to_pixels(units) -> int:
    """Converts given units to pixels
    each units is equal to 50 pixels

    Args:
        units (int): The amount of units to convert to pixels

    Returns:
        int: the amount of pixels converted from given amount of units
    """
    pixels = 50*units
    return pixels


def deg_to_rads(degs) -> float:
    """Converts a given amount of degrees to radians

    Args:
        degs (float): a given amount of degrees

    Returns:
        float: the amount of degrees converted to radians
    """
    rads = (math.pi/180) * degs
    print(rads)
    return rads


def rads_to_degs(rads) -> float:
    """Converts radians to degrees

    Args:
        rads (float): a given amount of radians

    Returns:
        float: the amount of radians converted to degreesx
    """
    degs = 180/math.pi * rads
    return degs


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


def draw_radius(screen, color, coords, radius, radian, return_coords=False, show_radius=True):
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
    if show_radius:
        pygame.draw.line(screen, color, coords, (x, y))

    if return_coords:
        return un_xy(x, y)


def screen_size():
    """
    Set screen size
    """
    return 1500, 1000


def main():
    pygame.init()

    size = width, height = screen_size()

    color = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'light_gray': (100, 100, 100),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'purp': (100, 0, 60)
    }

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    detail_level = 600
    counter = 0
    increment = 2*math.pi / detail_level

    dp = 5

    arm0 = FirstArm(screen=screen, color=color, counter=counter,
                    increment=increment, radius=200, constant=1,
                    start_angle=0, image_rot=90, line_color=(100, 0, 60),
                    show_circumferences=True, show_radii=True)
    arm1 = arm(arm0, radius=100, dp=dp, id=1, last=False, constant=2,
               start_angle=0)
    arm2 = arm(arm0, radius=100, dp=dp, id=2, last=True, constant=-2,
               start_angle=0)


    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill(color['white'])

        # -- Draw elements -- #

        # Graph axes
        # X
        pygame.draw.line(screen, color['light_gray'], xy(-width/2, 0), xy(width/2, 0))

        # Y
        pygame.draw.line(screen, color['light_gray'], xy(0, height/2), xy(0, -height/2))

        # Circles
        arm0.update()


        # print(len(dots))
        # -- Draw end -- #

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
