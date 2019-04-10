import sys

import numpy as np

import bpy
from mathutils import Matrix, Vector


def __matmul35(left, right):
    return left * right


def __matmul36(left, right):
    return left @ right


matmul = __matmul36 if sys.version_info[0] == 3 and sys.version_info[1] >= 6 else __matmul35


class Turtle:
    """A Turtle object that swims around in 3D space.

    Shamelessly and thankfully stolen from https://github.com/lemurni/lpy-lsystems-blender-addon.
    """

    def __init__(self):
        """Initialize a Turtle."""
        # turtle state consists of a 4x4 matrix and some drawing attributes
        self.mat = Matrix()
        # stack to save and restore turtle state
        self.stack = []
        # rotate such that heading is in +Z (we want to grow upwards in blender)
        # we thus have heading = +Z, left = -Y, up = +X
        self.mat = matmul(self.mat, Matrix.Rotation(3 * np.pi / 2, 4, "Y"))

    @property
    def position(self):
        """Get the Turtle's current position."""
        return self.mat.col[3].xyz.to_tuple()

    def push(self):
        """Push turtle state to stack."""
        self.stack.append(self.mat.copy())

    def pop(self):
        """Pop and restore last turtle state from stac."""
        self.mat = self.stack.pop()

    def move(self, stepsize):
        """Move turtle in its heading direction."""
        vec = matmul(self.mat, Vector((stepsize, 0, 0, 0)))
        self.mat.col[3] += vec

    def yaw(self, angle):
        """Yaw the Turtle around its local Z axis."""
        self.mat = matmul(self.mat, Matrix.Rotation(angle, 4, "Z"))

    def pitch(self, angle):
        """Pitch the Turtle around its local Y axis."""
        self.mat = matmul(self.mat, Matrix.Rotation(angle, 4, "Y"))

    def roll(self, angle):
        """Roll the Turtle around its local X axis."""
        self.mat = matmul(self.mat, Matrix.Rotation(angle, 4, "X"))
