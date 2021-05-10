#!/usr/bin/env python3
# fourier_series.py
# Create circles from complex numbers
# coords = coordinates

import pygame
import math
from sys import argv


class Circle:
    # Values are all normal within calculations.
    # This will be used for drawing in pygame
    try:
        unit = float(argv[1])  # px

    except ValueError:
        unit = float(input("Enter the value of 1 unit. "
                           "Number can be a float: "))

    except IndexError:
        unit = float(input("Enter the value of 1 unit: "))

    unit /= 10

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

        # -- Values that'll change but still need a pre-set
        # Math
        self.t = 0
        self.origin = 0j
        self.e_result = self.equation()

        self.attached_object = None
        # --

        # Do some trig to ge the radius
        self.radius = math.sqrt(pow(self.e_result.real - self.origin.real, 2)
                                + pow(self.e_result.imag - self.origin.imag, 2))

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

    # -- Utility methods -- #
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

    def equation(self):
        """
        0 <= t <= 1
        self.constant * e^(self.pos * 2 * π * 1j * t)
        :return: complex number
        """
        return self.origin + (self.constant * pow(math.e, (self.pos * 2 * math.pi * 1j * self.t)))

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
            self.draw_radius()

        if self.attached_object is not None:
            self.attached_object.update(t, self.e_result)

    # -- Get & Set methods -- #

    def attach(self, obj):
        """
        Attaches an object to the end of the radius
        """
        if "update" not in dir(obj):
            raise Exception('Object must have a .update() method')

        else:
            self.attached_object = obj

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

    def get_radian(self):
        """
        Gets the radian from the current t value
        """
        point = self.e_result

        rad = math.acos((point.real - self.origin.real) / self.radius)

        return rad

    # -- PyGame oriented methods -- #

    def pygame_coords(self, complex_num):
        """
        Turns complex number into coords that can be used in pygame
        """
        x, y = complex_num.real * self.unit, complex_num.imag * self.unit

        return xy(x, y)

    def draw_radius(self):
        """
        Draws the radius of a circle based on the equation and the
        origin coordinates.
        """
        # Get coordinates at circumference
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


class DrawDots:
    def __init__(self, screen, dot_color, line_color,
                 precision=2, dots=None, dot_size=1,
                 show_dot=True, show_line=True):
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
        self.show_dot = show_dot
        self.show_line = show_line

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

    def update(self, t, complex=None):
        """
        Adds the given dot to the objects list of dots and draws them
        """
        # This variable is not useful
        del t

        if complex is not None:
            coords = complex.real * Circle.unit, complex.imag * Circle.unit
            new_coords = xy(*coords)

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
            for dot in range(len(self.dots)-1):
                if self.show_line:
                    self.draw_line(self.dots[dot], self.dots[dot+1])

                if self.show_dot:
                    self.draw_dot(self.dots[dot])

            del dot


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


def create_circles(screen, filename, draw=True, dot_color=(0, 0, 255), line_color=(0, 255, 0)):
    # Read the consts from file
    with open(filename, 'r') as file:
        constants_str = file.readline().replace('\n', '')

    # Turn into list
    constants_ls = constants_str.split(';')

    # Remove empty strings
    constants_ls = list(filter(None, constants_ls))

    # Convert to numbers
    constants = [complex(x) for x in constants_ls]

    # Get numbers for the following sequence
    actual_nums = int((len(constants) - 1) / 2)

    # This generates a sequence of 0, 1, -1, 2, -2, etc
    nums = []
    for i in range(0, actual_nums + 1):
        nums.append(i)

        if i != 0:
            nums.append(i * -1)

    # Start making objects
    circles = []
    for const in range(0, len(constants)):
        circles.append(Circle(screen, constants[const], nums[const], show_circumference=False, r_stroke=1))

    # Reverse the list for attaching
    circles.reverse()

    # Attach a DrawDot object if requested
    if draw:
        circles[0].attach(DrawDots(screen, dot_color, line_color))
        dots_obj = circles[0].attached_object
    # Starting at one so i can attach the *previous* obj to
    # the current one
    for obj in range(1, len(circles)):
        circles[obj].attach(circles[obj - 1])

    # Return the static circle
    if draw:
        return circles[-1], dots_obj

    else:
        return circles[-1]


def main():
    pygame.init()

    size = width, height = screen_size()

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    circle, drawdots_obj = create_circles(screen, "constants", draw=True)

    # This value will increase by increment each loop
    increment = 0.001
    t = 0

    # TODO: Add shortcuts to pygame window to edit runtime stuff
    # Like show radii circumference
    # Zoom
    # Move
    # Speed

    # Variable used for messing with draw dots obj
    # resize = False

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # Reset t
        if not 0 <= t <= 1:
            t = 0
            # resize = True

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

        # pygame.draw.line(screen,
        #                  color['light_gray'],
        #                  xy(20, height / 2),
        #                  xy(20, -height / 2))

        # Circles
        # circle.update(increment)

        # --
        # Update the circle
        circle.update(t)

        # Mess with the DrawDots obj
        # drawdots_obj.dots = []  # This will clear the dots

        # This will decrease the drawing by 0.5 each time (accumulative)
        # without passing it through xy

        # if resize:
        #     drawdots_obj.dots = [(i[0] * 0.5, i[1] * 0.5) for i in drawdots_obj.dots]  # Make the figure twice as small
        #     resize = False

        t += increment

        pygame.display.flip()
        clock.tick(120)


if __name__ == "__main__":
    color = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'light_gray': (100, 100, 100),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255)
    }
    main()
