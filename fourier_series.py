#!/usr/bin/env python3

##
# fourier_series.py
# coords = coordinates
import pygame
import math
import random

from pygame import time


class FirstArm:

    def __init__(self, screen=any, color=(255, 0, 0), counter=int, increment=float, radius=int, constant=int, start_angle=0, image_rot=0):
        self.color = color
        self.screen = screen
        self.counter = counter
        self.increment = increment
        self.radius = radius
        self.constant = constant
        self.dots = []
        self.first=None
        self.start_angle = deg_to_rads(start_angle)
        self.image_rot = deg_to_rads(image_rot)


        self.children = []

        self.new_x = {}
        self.new_y = {}

    def update(self):
        self.new_x[1], self.new_y[1] = draw_radius(self.screen, (255, 0, 0), xy(0, 0),
                                   self.radius, self.constant * self.counter * self.increment + self.start_angle + self.image_rot, True)
        draw_hollow_circle(self.screen, (0, 0, 0), xy(0, 0), self.radius)
        self.counter += 1
        for child in self.children:
            child.update()
            new_x = self.new_x[child.id]
            new_y = self.new_y[child.id]





class arm:

    def __init__(self, parent, radius, dp, id, last, constant, color=(random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)), start_angle=0):
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
        new_x = self.parent.new_x
        new_y = self.parent.new_y
        id = self.id
        draw_hollow_circle(self.parent.screen, (0, 0, 0), xy(new_x[id], new_y[id]), self.radius)
        new_x[id+1], new_y[id+1] = draw_radius(self.parent.screen, self.color, xy(new_x[id], new_y[id]),
                                   self.radius, self.constant * self.parent.counter * self.parent.increment + self.start_angle + self.parent.image_rot, True)
        if self.last:
            self.point = (round(new_x[id+1], self.dp), round(new_y[id+1], self.dp))

            if self.point not in self.parent.dots:
                self.parent.dots.append(self.point)

            if self.parent.first is None:
                self.prev = self.parent.first = self.point
                print(self.point)

            # TODO: Find out why the last dot connects to the first always
            for dot in self.parent.dots:
                if self.prev is not None:
                    pygame.draw.line(self.parent.screen, self.parent.color['green'], xy(*self.prev), xy(*dot))

                pygame.draw.circle(self.parent.screen, self.parent.color['blue'], xy(*dot), 1)
                self.prev = dot


def deg_to_rads(degs):
    rads = (math.pi/180) * degs
    print(rads)
    return rads


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

    time = 600
    counter = 0
    increment = 2*math.pi / time

    dp = 5

    arm0 = FirstArm(screen=screen, color=color, counter=counter, increment=increment, radius=100, constant=0, start_angle=30, image_rot=0)
    # for arm_num in range(1, 5):
    arm1 = arm(arm0, radius=50, dp=dp, id=1, last=False, constant=1, start_angle=80)
    arm2 = arm(arm0, radius=150, dp=dp, id=2, last=False, constant=-1, start_angle=-30)
    arm3 = arm(arm0, radius=200, dp=dp, id=3, last=True, constant=2, start_angle=90)

    arm4 = FirstArm(screen=screen, color=color, counter=counter, increment=increment, radius=100, constant=0, start_angle=-150, image_rot=0)
    # for arm_num in range(1, 5):
    arm5 = arm(arm4, radius=25, dp=dp, id=1, last=False, constant=1, start_angle=-100)
    arm6 = arm(arm4, radius=50, dp=dp, id=2, last=False, constant=-1, start_angle=-50)
    arm7 = arm(arm4, radius=75, dp=dp, id=3, last=True, constant=2, start_angle=0)

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
        arm4.update()


        # print(len(dots))
        # -- Draw end -- #

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
