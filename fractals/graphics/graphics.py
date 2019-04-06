import json
from functools import partial

import bpy

from .turtle import Turtle


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
    """

    @staticmethod
    def __check_args(radius, proportion):
        if radius is not None and proportion is not None:
            raise ValueError("`radius` and `proportion` are mutually exclusive.")

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

        self.material = material
        self.radius = radius if radius is not None else 0.2
        self.proportion = proportion
        self.unit = unit
        self.angle = angle

        self.turtle = Turtle()

        self.mappings = {
            # Bind the distance and angle parameters to the turtle methods.
            "F": partial(self.turtle.move, unit),
            "G": partial(self.turtle.move, unit),
            "-": partial(self.turtle.yaw, -angle),
            "+": partial(self.turtle.yaw, +angle),
            "v": partial(self.turtle.pitch, -angle),
            "^": partial(self.turtle.pitch, +angle),
            "<": partial(self.turtle.roll, -angle),
            ">": partial(self.turtle.roll, +angle),
            "[": self.turtle.push,
            "]": self.turtle.pop,
        }

    def draw(self, commands):
        """Generate the 3D cylinders from the given graphics commands.

        :param commands: A string of successive graphics commands.
        :return: A list of cylinder dictionaries.
        """
        cylinders = []
        commands = iter(commands)
        for command in commands:
            length = 0
            start = self.turtle.position
            # Consume consecutive forward commands.
            while command in ("G", "F"):
                self.mappings[command]()
                length += self.unit
                command = next(commands)
            end = self.turtle.position

            if length > 0:
                if self.proportion is not None:
                    self.radius = self.proportion * length

                cylinders.append(
                    {
                        "from": start,
                        "to": end,
                        "radius": self.radius,
                        "material": "Branch" if length > 1 else "Leaf",
                    }
                )

            if command in self.mappings:
                self.mappings[command]()

        return cylinders

    @staticmethod
    def dump(data, path):
        """Dump the cylinder data to a JSON file."""
        if data:
            with open(path + ".json", "w") as outfile:
                json.dump(data, outfile)
