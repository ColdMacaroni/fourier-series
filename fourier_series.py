#!/usr/bin/env python3

##
# fourier_series.py
# coords = coordinates
import pygame
import math


class FirstArm:

    def __init__(self, screen, color, counter, increment, radius, dp):
        self.color = color
        self.screen = screen
        self.counter = counter
        self.increment = increment
        self.radius = radius
        self.dp = dp

        self.dots = []
        self.first = None


        self.children = []

        self.new_x = {}
        self.new_y = {}
        draw_hollow_circle(screen, color['black'], xy(0, 0), 50)

    def update(self):
        self.new_x[1], self.new_y[1] = draw_radius(self.screen, self.color['red'], xy(0, 0),
                                   self.radius, 1 * self.counter * self.increment, True)
        for child in self.children:
            child.update()
            new_x = self.new_x[child.id]
            new_y = self.new_y[child.id]

            self.point = (round(new_x, self.dp), round(new_y, self.dp))

            if self.point not in self.dots:
                self.dots.append(self.point)

            if self.first is None:
                self.prev = self.first = self.point

        # TODO: Find out why the last dot connects to the first always
        for dot in self.dots:
            pygame.draw.line(self.screen, self.color['green'], xy(*self.prev), xy(*dot))

            pygame.draw.circle(self.screen, self.color['blue'], xy(*dot), 1)
            self.prev = dot



class arm:

    def __init__(self, parent, radius, id):
        self.parent = parent
        self.radius = radius
        self.id = id
        self.parent.children.append(self)

    def update(self):
        self.parent.new_x[self.id+1], self.parent.new_y[self.id+1] = draw_radius(self.parent.screen, self.parent.color['red'], xy(0, 0),
                                   self.radius, 1 * self.parent.counter * self.parent.increment, True)

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

    time = 100
    counter = 0
    pi_t = math.pi / time

    dp = 5

    arm0 = FirstArm(screen=screen, color=color, counter=counter, increment=(10*pi_t), radius=100, dp=dp)
    arm1 =arm(arm0, 50, 1)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill(color['white'])

        # -- Draw elements -- #
        counter += 1

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
        clock.tick(time)


if __name__ == "__main__":
    main()
