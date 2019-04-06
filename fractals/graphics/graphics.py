import json

import numpy as np

from fractals.turtle import Turtle


class Graphics:
    """Interprets Lindenmayer graphics command strings to generate 3D cylinders.

    Command strings are composed of the following symbols.

    F,G - Advance in the current direction one unit while drawing.
    <,> - Roll CCW or CW, respectively, by one unit.
    ^,v - Pitch up or down, respectively, by one unit.
    -,+ - Yaw left or right, respectively, by one unit.
    c,C - Decrement or increment, respectively, the current color by one unit.

    TODO: I'm not sure how to do this with Blender. I know we can set the cylinder's material
    (Provided the material exists before the cylinders are drawn). And I know we can set the
    cylinder's color, but when I tried, the colors did not display. I think I'd prefer setting a
    material over the color, but then we'd need a material map (similar to a matplotlib colormap).
    The choice of color vs. material will also be influenced by whether or not we render the scene
    after generating it (something I don't know much about).

    r,R - Decrement or increment, respectively, the current cylinder radius.
    [,] - Save or restore, respectively, the current state on the stack. Note that the saved state
          includes the color (or material), direction, pen up/down state, and cylinder radius.

    TODO: Add 2D stdlib turtle mode?
    """

    symbols = frozenset("FG-+<>^vcCrR[]")
    unhandled = frozenset("<>^vcCrR[]")

    SYMBOLS = {'F' : 0.5, 'G' : 1.0, '-' : 0, '+' : 0}

    @staticmethod
    def __check_args(radius, proportion):
        if radius is not None and proportion is not None:
            raise ValueError("`radius` and `proportion` are mutually exclusive.")

    def __validate(self, commands):
        # The command strings are likely to be huge, so convert to set.
        commands = set(commands)

        for command in commands:
            if command not in Graphics.symbols:
                raise ValueError("Unknown command: '{}'.".format(command))
            # TODO: This is temporary, until we figure out how to handle these.
            if command in Graphics.unhandled:
                raise NotImplementedError("Command: '{}' not yet implemented.".format(command))

        if self.proportion is not None and ("r" in commands or "R" in commands):
            raise ValueError("Cannot modify cylinder radius in proportional mode.")

    def __init__(self, unit, angle, material=None, radius=None, proportion=None):
        """Initialize a Graphics object to draw command strings for fractals.

        If neither a radius or a proportionality constant is given, default to a constant radius
        of 0.2.

        :param unit: The length of each 'forward' command.
        :param angle: The angle of each 'rotate' and 'bend' command. In radians.
        :param material: The Blender material to make each cylinder object with, defaults to None.
        :param radius: The radius of each cylinder. Mutually exclusive with `proportion`.
        :param proportion: Make each cylinder's radius proportional to its length. Mutually
        exclusive with `radius`.
        """
        self.__check_args(radius, proportion)

        self.unit = unit
        self.angle = angle
        self.SYMBOLS['-'] = -angle
        self.SYMBOLS['+'] = angle
        self.material = material
        self.radius = radius if radius is not None else 0.2
        self.proportion = 1.0

        self.turtle = Turtle()

    def draw(self, commands):
        """Generate the 3D cylinders from the given graphics commands.

        :param commands: A string of successive graphics commands.
        :return: A list of cylinder dictionaries.
        """
        self.__validate(commands)
        i = 0
        data = []

        while i < len(commands):
            length = 0
            start = self.turtle.position
            # Combine G and F?
            if commands[i] == "G":
                while i < len(commands) and commands[i] == "G":
                    # self.turtle.forward(commands[i])
                    self.turtle.move(self.SYMBOLS[commands[i]])
                    length += 1
                    i += 1
            elif commands[i] == "F":
                while i < len(commands) and commands[i] == "F":
                    # self.turtle.forward(commands[i])
                    self.turtle.move(self.SYMBOLS[commands[i]])
                    length += 1
                    i += 1
            elif commands[i] == "-":
                self.turtle.yaw(self.SYMBOLS[commands[i]])
            elif commands[i] == "+":
                self.turtle.yaw(self.SYMBOLS[commands[i]])

            if length > 0:
                end = self.turtle.position
                data.append(
                    {
                        "from": list(start.to_tuple()),
                        "to": list(end.to_tuple()),
                        "radius": self.radius * self.proportion,
                        "material": self.material,
                    }
                )
            else:
                i += 1

        return data

    def dump(self, data, path):
        if len(data) > 0:
            with open(path + ".json", "w") as outfile:
                json.dump(data, outfile)
