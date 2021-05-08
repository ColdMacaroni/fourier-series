#!/usr/bin/env python3

##
# fourier_series.py
# Create circles from complex numbers
# coords = coordinates

import pygame
import math


class Circle:
    # Values are all normal within calculations.
    # This will be used for drawing in pygame
    unit = 50  # px

    def __init__(self, screen, constant, pos,
                 circle_color=(0, 0, 0), radius_color=(255, 0, 0),
                 show_circumference=True, show_radius=True,
                 c_stroke=1, r_stroke=1):
        """
        Generate a circle based on c * e^(n * 2 * π * 1j * t)
        :param screen: Pygame screen
        :param constant: c. A complex number
        :param pos: The position in a series of Circles. int
        :param circle_color: rgb value of circumference
        :param radius_color: rgb value of radius
        :param show_circumference: Boolean for drawing circumference
        :param show_radius: Boolean for drawing radius
        :param c_stroke: Stroke size for the circumference
        :param r_stroke: Stroke size for the radius
        """
        # Parameters
        self.screen = screen
        self.constant = constant
        self.pos = pos

        # Keywords
        self.circle_color = circle_color
        self.radius_color = radius_color
        self.show_circumference = show_circumference
        self.show_radius = show_radius
        self.c_stroke = c_stroke
        self.r_stroke = r_stroke

        # Values that'll change
        self.t = 0
        self.radius = self.constant.real
        self.origin = 0j
        self.attached_object = None
        self.e_result = self.equation()
        # NOTE: Centre of the circle is parent's equation result

        # Circles will need the following parameters
        # n
        # c
        # Starting coords
        # They will need a method to get the result of the equation
        # from a given t

        # Attach method and such will still work.
        # Radians and all that would be kinda useless

        # c.real = radius

        # NOTE: The formula for the circle is
        # c * e^(n * 2 * π * 1j * t)
        # n determines how many revolutions per second
        # t is a normal number that'll denote the point in the circle's
        # circumference. 0 <= t <= 1

        # c is a constant that will determine the circle's nature
        # Its real part will determine the size and its complex part
        # will determine the revolutions per second

        # Send the coordinates given by the equation above to the child
        # Child will add those to its own to get origin (0,0 + parent)
        # and radius point (equation + parent). Then send the radius
        # point to its own child

    def config(self, show_circumference=None, show_radius=None,
               c_stroke=None, r_stroke=None):
        """
        Change visibility settings during runtime
        :param show_circumference: Bool
        :param show_radius: Bool
        :param r_stroke: int
        :param c_stroke: int
        """
        if show_circumference is not None:
            self.show_circumference = show_circumference

        if show_radius is not None:
            self.show_radius = show_radius

        if c_stroke is not None:
            self.c_stroke = c_stroke

        if r_stroke is not None:
            self.r_stroke = r_stroke

    def set_origin(self, origin):
        self.origin = origin

    def set_t(self, t):
        """
        Updates t value and equation result
        :param t: float 0 <= t <= 1
        """
        if 0 <= t <= 1:
            # Update t
            self.t = t

            # This is done to avoid multiple method calls
            self.e_result = self.equation()
        else:
            raise ValueError('t must be between 0 and 1 (inclusive)')

    def equation(self):
        """
        0 <= t <= 1
        self.constant * e^(self.pos * 2 * π * 1j * t)
        :return: complex number
        """
        return self.origin + (self.constant * math.e ** (self.pos * 2 * math.pi * 1j * self.t))

    def get_radian(self):
        """
        Gets the radian from the current t value
        """
        point = self.e_result

        rad = math.acos((point.real - self.origin.real) / self.radius)

        return rad

    def pygame_coords(self, complex_num):
        """
        Turns complex number into coords that can be used in pygame
        """
        x, y = complex_num.real * self.unit, complex_num.imag * self.unit

        return xy(x, y)

    def update(self, t, new_origin=None):
        """
        Update the circle with a new t value
        :param t: float
        :param new_origin:
        :return:
        """
        # Change origin
        if new_origin is not None:
            self.origin = new_origin

        # Update t value
        self.set_t(t)

        # Draw circumference
        if self.show_circumference:
            self.draw_circumference()

        # Draw radius
        if self.show_radius:
            self.draw_circumference()

        if self.attached_object is not None:
            self.attached_object.update(t, self.e_result)

    def draw_radius(self):
        """
        Draws the radius of a circle based on the equation and the
        origin coordinates.
        """
        # Get coordinates at circumference
        if self.show_radius:
            pt = self.e_result

            pygame.draw.line(self.screen,
                             self.radius_color,
                             self.pygame_coords(self.origin),
                             self.pygame_coords(pt),
                             width=self.r_stroke)

    def draw_circumference(self):
        """
        Draws the circumference of the circle around the origin
        """
        if self.show_circumference:
            # Same width and height. i.e. perfect circle.
            height = width = self.radius * 2 * self.unit

            # -- Create a rectangle object for the circle.

            x, y = self.pygame_coords(self.origin)

            # Shift the rect so the center of the circle is at given coordinates
            x = x - width / 2
            y = y - height / 2

            # Create the rectangle object
            rect = pygame.Rect((x, y), (width, height))

            # -- Draw the circle
            pygame.draw.arc(self.screen,
                            self.circle_color,
                            rect, 0, 2 * math.pi, width=self.c_stroke)


class OldCircle:
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

        # Circles will need the following parameters
        # n
        # c
        # Starting coords
        # They will need a method to get the result of the equation
        # from a given t

        # Attach method and such will still work.
        # Radians and all that would be kinda useless

        # c.real = radius

        # NOTE: The formula for the circle is
        # c * e^(n * 2 * π * 1j * t)
        # n determines how many revolutions per second
        # t is a normal number that'll denote the point in the circle's
        # circumference. 0 <= t <= 1

        # c is a constant that will determine the circle's nature
        # Its real part will determine the size and its complex part
        # will determine the revolutions per second

        # Send the coordinates given by the equation above to the child
        # Child will add those to its own to get origin (0,0 + parent)
        # and radius point (equation + parent). Then send the radius
        # point to its own child

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
        self.attached_object = None

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
        self.attached_object = attached

    def update(self, increment, new_coords=None):
        if new_coords is not None:
            self.center_coords = new_coords

        # Get new radian
        self.radian = self.radian + self.const * increment

        # Make radian a smaller number
        # This will hopefully make it more efficient as the memory used
        # for the variable will not increase past a certain point
        # The second if is necessary to support negative radians
        if self.radian >= math.pi * 2:
            self.radian = self.radian % (math.pi * 2)

        elif self.radian <= math.pi * -2:
            self.radian = 0 - (abs(self.radian) % (math.pi * 2))

        self.draw_circumference()
        self.draw_radius()

        if self.attached_object is not None:
            coords_param = self.coords_at_circumference()
            self.attached_object.update(increment, new_coords=coords_param)

    def draw_circumference(self):
        """
        Draws the circumference
        """
        # Same width and height. i.e. perfect circle.
        height = width = self.radius * 2

        # -- Create a rectangle object for the circle.
        # Shift the rect so the center of the circle is at given coordinates
        x = self.center_coords[0] - width / 2
        y = self.center_coords[1] - height / 2

        print(x, y, "", width, height)

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

        pygame.draw.line(self.screen,
                         self.radius_color,
                         self.center_coords,
                         (x, y))

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


class DrawDots:
    def __init__(self, screen, dot_color, line_color,
                 precision=2, dots=None, dot_size=1):
        """
        :param screen: Pygame screen
        :param dot_color: Color for each dot
        :param line_color: Color for the line that connects the dots
        :param precision: The decimal points to round each point
        :param dots: The location for each dot.
        :param dot_size: The size for the dots
        """
        # A dot is merele an x,y coordinate
        self.screen = screen
        self.dot_color = dot_color
        self.line_color = line_color

        # Keywords
        self.precision = precision
        self.dots = dots
        self.dot_size = dot_size

        if self.dots is None:
            self.dots = []

    def append_dot(self, new_dot):
        """
        Adds a dot to the list of dots
        :param new_dot: (x, y) coordinate
        """
        new_dot = self.round_dot(new_dot)
        if new_dot not in self.dots:
            self.dots.append(new_dot)

    def round_dot(self, dot):
        """
        Rounds a dot to the current object's precision
        if self.precision=2
        (2.4345, 5.4534) -> (2.43, 5.45)
        :param dot: (x, y) coordinate
        :return (x, y) coordinate
        """
        rounded_dot = (round(dot[0], self.precision),
                       round(dot[1], self.precision))
        return rounded_dot

    def update(self, increment, new_coords):
        """
        Adds the given dot to the objects list of dots and draws them
        """
        # This variable is not useful
        del increment

        self.append_dot(new_coords)
        self.graph()

    def draw_dot(self, dot):
        pygame.draw.circle(self.screen, self.dot_color, dot, self.dot_size)

    def draw_line(self, dot1, dot2):
        pygame.draw.line(self.screen, self.line_color, dot1, dot2)

    def graph(self):
        """
        Draws the list of dots and connects them with a line
        """
        # Do not draw line if there is only one dot
        if len(self.dots) == 1:
            self.draw_dot(self.dots[0])

        else:
            for dot in range(len(self.dots)):
                self.draw_line(self.dots[dot-1], self.dots[dot])
                self.draw_dot(self.dots[dot])


def i_xy(num):
    """
    turns an imaginary number to x, y coordinates
    y=i
    """
    return num.real, num.imag


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

    return width/2 + coords[0], height/2 + coords[1]


def un_center_coords(coords, plane=None):
    """
    Repositions coords to the bottom left of the plane
    """
    if plane is None:
        width, height = screen_size()
    else:
        width, height = plane[0], plane[1]

    return coords[0] - width/2, coords[1] - height/2


def py_coords(coords):
    """
    Convert coordinates into pygame coordinates (lower-left => top left).
    """
    height = screen_size()[1]
    return coords[0], height - coords[1]


def un_py_coords(coords):
    """
    Convert coordinates into cardinal coordinates (top-left => lower left).
    """
    height = screen_size()[1]
    return coords[0], height + coords[1]


def screen_size():
    """
    Set screen size
    """
    return 600, 600


def create_circles(root_circle_parameters, circle_parameters,
                   dotdraw_parameters=None, draw=True):

    # TODO: Turn this into  a for loop. e.g. range(-2, 5). Will take a list of constants (c) and will use the i for (n)
    # Start initial object
    # This is done so we are able to replace the
    # coordinates for the next objects
    objects = [OldCircle(*root_circle_parameters)]

    for i in range(len(circle_parameters)):
        parameter = circle_parameters[i]

        # Replace previous coordinates for the ones of the previous object
        parameter[1] = objects[i - 1].coords_at_circumference()

        objects.append(OldCircle(*parameter))

    # Start attaching the objects from the end to the start
    objects.reverse()

    if draw:
        objects[0].attach(DrawDots(*dotdraw_parameters))

    # Attach all of them to each other
    for circle in range(1, len(objects)):
        objects[circle].attach(objects[circle - 1])

    # Return the root object
    return objects[-1]


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

    # Generate circle series
    circle = create_circles([screen, xy(0, 0), 50, 0.1, 2], [
        [screen, None, 35, -1, 0],
        [screen, None, 10, 2, 0.5],
        [screen, None, 15, -3, math.pi],
    ], [screen, color['blue'], color['green']])

    # Increment is how much the radian will change per time unit
    # At an increment of 2*math.pi/120, the radian will go through a
    # full rotation after 120 time units. (2s if running at 60fps)

    increment = 2*math.pi / 220

    test = Circle(screen, 1+1j, 1)

    # This value will increase by increment each loop
    increment = 0.01
    t = 0

    # dp = 5
    # dots = []
    # first = None
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # Reset t
        if not 0 <= t <= 1:
            t = 0

        screen.fill(color['white'])

        # -- Draw elements -- #
        # Graph axes
        # X
        pygame.draw.line(screen,
                         color['light_gray'],
                         xy(-width/2, 0),
                         xy(width/2, 0))

        # Y
        pygame.draw.line(screen,
                         color['light_gray'],
                         xy(0, height/2),
                         xy(0, -height/2))

        # Circles
        # circle.update(increment)

        # --
        test.update(t)

        t += increment

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
