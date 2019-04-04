import itertools
import json
import numpy as np

from fractals.graphics import Turtle3D

class Lstr2json:
    """Apply production rules to strings."""

    def __init__(self, string="", path='dat/output'):
        """Init class.
        """
        self.string = string
        self.path = path
        self.data = []
        self.__convert()

    def __convert(self):
        """Convert the input string into a .json file"""
        i = 0
        turtle = Turtle3D(step=1, angle=0)

        while i < len(self.string):
            length = 0
            start = turtle.position
            # Combine G and F?
            if self.string[i] == 'G':
                while self.string[i] == 'G':
                    # turtle.forward(self.string[i])
                    # turtle.forward()
                    length += 1
                    i += 1
                end =turtle.position
            elif self.string[i] == 'F':
                while self.string[i] == 'F':
                    # turtle.forward(self.string[i])
                    # turtle.forward()
                    length += 1
                    i += 1
            elif self.string[i] == '-':
                turtle.yaw()
            elif self.string[i] == '+':
                turtle.yaw(right=True)

            if length > 0:
                self.__append_cylinder(start, turtle.position, length * 0.1)
            else:
                i += 1


        if len(self.data) > 0:
            with open(self.path + '.json', 'w') as outfile:
                json.dump(self.data, outfile)

    def __append_cylinder(self, start=[0,0,0], end=[0,0,0], radius=0.5, material='null'):
        """Appends cylinder to self.data
        """
        self.data.append({'from': start.tolist(), 'to': end.tolist(), 'radius':radius, 'material': material})

