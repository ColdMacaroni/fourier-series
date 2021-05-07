#!/usr/bin/env python3

##
# fourier_series.py
# coords = coordinates
import pygame
import math


class Circle:
    def __init__(self, screen, coords, radius, const, radian,
                 circle_color=(0, 0, 0), radius_color=(255, 0, 0),
                 show_circumference=True, show_radius=True, stroke=1):
        """
        :param screen: Pygame screen
        :param coords: Coordinates for the circle's centre (x, y)
        :param radius: Length of the radius (px)
        :param const: The constant for the fourier formula. Float
        :param radian: The radian at which the radius will be drawn

        defaults:
        :param circle_color: Color for the circle circumference. rgb
               default=(0, 0, 0)

        :param radius_color: Color for the radius. rgb
               default=(255, 0, 0)

        :param show_circumference: If the circumference should be drawn. Bool
               default=True

        :param show_radius: If the radius should be draw. Bool
               default=True

        :param stroke: Stroke used for the circle and the radius.
               default=1
        """

        # Start the boy up
        self.screen = screen
        self.center_coords = coords
        self.radius = radius
        self.const = const
        self.radian = radian

        # Keywords
        self.circle_color = circle_color
        self.radius_color = radius_color
        self.show_circumference = show_circumference
        self.show_radius = show_radius
        self.stroke = stroke

        # Default
        self.attached = None

    def config(self, show_circumference=None, show_radius=None):
        """
        Change visibility settings during runtime
        :param show_circumference: Bool
        :param show_radius: Bool
        """
        if show_circumference is not None:
            self.show_circumference = show_circumference

        if show_radius is not None:
            self.show_radius = show_radius

    def attach(self, attached):
        self.attached = attached

    def update(self, increment, new_center_coords=None):
        if new_center_coords is not None:
            self.center_coords = new_center_coords

        # Get new radian
        self.radian = self.radian + self.const * increment

        # Make radian a smaller number
        # This will hopefully make it more efficient as the memory used
        # for the variable will not increase past a certain point
        if self.radian >= math.pi * 2:
            self.radian = self.radian % (math.pi * 2)

        print(self.radian)

        self.draw_circumference()
        self.draw_radius()

        if self.attached is not None:
            self.attached.update(increment, new_center_coords=self.coords_at_circumference())

    def draw_circumference(self):
        """
        Draws the circumference
        """
        # Same width and height. i.e. perfect circle.
        height = width = self.radius * 2

        # -- Create a rectangle object for the circle.
        # Shift the rect so the centre of the circle is at the given coordinates
        x = self.center_coords[0] - width / 2
        y = self.center_coords[1] - height / 2

        # Create the rectangle object
        rect = pygame.Rect((x, y), (width, height))

        # -- Draw the circle
        pygame.draw.arc(self.screen, self.circle_color, rect, 0, 2 * math.pi)

    def draw_radius(self):
        """
        Draws the radius of a circle based on the radian given and the
        original coordinates.
        """
        # Get coordinates at circumference
        x, y = self.coords_at_circumference()

        pygame.draw.line(self.screen, self.radius_color, self.center_coords, (x, y))

    def coords_at_circumference(self):
        """
        :return: int
        The coordinates at the circumference at the given radian
        """
        # Turn pygame cords to normal coords (center = 0,0)
        normal_coords = un_xy(*self.center_coords)

        x = normal_coords[0] + self.radius * math.cos(self.radian)
        y = normal_coords[1] + self.radius * math.sin(self.radian)

        # Return the coords back to pygame coords
        return xy(x, y)


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

    test_circle = Circle(screen, xy(0, 0), 50, 1, 0)

    # Increment is how much the radian will change per time unit
    # At an increment of 2*math.pi/120, the radian will go through a
    # full rotation after 120 time units. (2s if running at 60fps)
    time = 0
    increment = 2*math.pi / 120

    # dp = 5
    # dots = []
    # first = None
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        time += 1

        screen.fill(color['white'])

        # -- Draw elements -- #
        # When `counter` reaches `time` a circle with a constant of one
        # Would have done a full revolution
        # e.g. if time=120, the const is 1, and clock.tick is 60 it
        # will take 2 seconds to do a full revolution
        # counter += 1

        # Graph axes
        # X
        pygame.draw.line(screen, color['light_gray'], xy(-width/2, 0), xy(width/2, 0))

        # Y
        pygame.draw.line(screen, color['light_gray'], xy(0, height/2), xy(0, -height/2))

        # # Circles
        # draw_hollow_circle(screen, color['black'], xy(0, 0), 50)
        # new_x, new_y = draw_radius(screen, color['red'], xy(0, 0), 50, 1 * counter * increment, True)
        #
        # draw_hollow_circle(screen, color['black'], xy(new_x, new_y), 50)
        # new_x, new_y = draw_radius(screen, color['red'], xy(new_x, new_y), 50, -0.8 * counter * increment, True)
        #
        # point = (round(new_x, dp), round(new_y, dp))
        #
        # if point not in dots:
        #     dots.append(point)
        #
        # if first is None:
        #     prev = first = point
        #
        # # TODO: Find out why the last dot connects to the first always
        # for dot in dots:
        #     pygame.draw.line(screen, color['green'], xy(*prev), xy(*dot))
        #
        #     pygame.draw.circle(screen, color['blue'], xy(*dot), 1)
        #     prev = dot

        # print(len(dots))
        # -- Draw end -- #

        test_circle.update(increment)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
