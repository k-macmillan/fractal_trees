import sys

import numpy as np

import bpy
from mathutils import Matrix, Vector


def matmul(left, right):
    if sys.version_info[0] == 3 and sys.version_info[1] >= 6:
        return left @ right
    else:
        return left * right


class Turtle:
    """This is the base class of the turtle that does not create any objects, but can be used to perform a dry-run interpretation to query the turtle state at different moments"""

    def __init__(self):
        # turtle state consists of a 4x4 matrix and some drawing attributes
        self.mat = Matrix()
        # stack to save and restore turtle state
        self.stack = []
        # rotate such that heading is in +Z (we want to grow upwards in blender)
        # we thus have heading = +Z, left = -Y, up = +X
        self.mat = matmul(self.mat, Matrix.Rotation(3 * np.pi / 2, 4, "Y"))

    @property
    def position(self):
        return self.mat.col[3].xyz

    def push(self):
        """Push turtle state to stack"""
        # push state to stack
        self.stack.append(self.mat.copy())

    def pop(self):
        """Pop last turtle state from stack and use as current"""
        self.mat = self.stack.pop()

    def move(self, stepsize):
        """Move turtle in its heading direction."""
        vec = matmul(self.mat, Vector((stepsize, 0, 0, 0)))
        self.mat.col[3] += vec

    def yaw(self, angle):
        self.mat = matmul(self.mat, Matrix.Rotation(angle, 4, "Z"))

    def pitch(self, angle):
        self.mat = matmul(self.mat, Matrix.Rotation(angle, 4, "Y"))

    def roll(self, angle):
        self.mat = matmul(self.mat, Matrix.Rotation(angle, 4, "X"))

    def look_at(self, target):
        """
        Let turtle look at a given 3D targed vector point.
        The heading vector will point toward x, y, z
        and the heading, up, and left vectors will have the same
        relative orientation (handedness) as before.
        """
        turtle_pos = self.mat.col[3].xyz
        turtle_to_target = target - turtle_pos
        turtle_to_target.normalize()
        result_mat = Matrix()

        # position stays same
        result_mat.col[3] = self.mat.col[3]

        # heading towards target
        result_mat.col[0] = turtle_to_target.resized(4)

        # use old up vector to compute orthogonal left vector
        # the cross product defaults to right hand order but we store a left vector
        # thus we negate the cross product vector
        old_up = self.mat.col[1].xyz.normalized()
        left = Vector.cross(old_up, turtle_to_target).normalized()
        result_mat.col[2] = left.resized(4)

        # compute new up vector from left and heading vector
        # since the left and new up vectors were constructed using the same left hand order
        # the left hand order is preserved.
        result_mat.col[1] = Vector.cross(left, turtle_to_target).normalized().resized(4)

        self.mat = result_mat
