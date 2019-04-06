import numpy as np
from pyquaternion import Quaternion


class Turtle3D:
    """A 3D implementation of a turtle."""

    def __init_position(self, position, orientation):
        if isinstance(orientation, Quaternion):
            self.orientation = orientation
        elif orientation is None:
            self.orientation = Quaternion(scalar=0, vector=[0, 0, 1])
        else:
            raise ValueError("Orientation must be a pyquaternion.Quaternion object.")
        if isinstance(position, (list, tuple, np.ndarray)) and len(position) == 3:
            self.position = position if isinstance(position, np.ndarray) else np.array(position)
        elif position is None:
            self.position = np.array([0, 0, 0])
        else:
            raise ValueError("Position must be an (x, y, z) 3-tuple.")

    def __init__(self, step, angle, position=None, orientation=None):
        """Initialize a Turtle3D at the given position and orientation.

        :param position: The initial position for the turtle, defaults to None
        :param position: An (x, y, z) tuple, list, or np.array, optional
        :param orientation: The initial orientation for the turtle, defaults to None
        :param orientation: Quaternion, optional
        """
        self.step = step
        self.angle = angle
        self.position = None
        self.orientation = None
        self.__init_position(position, orientation)
        self.initial_direction = self.orientation.get_axis(undefined=[0, 0, 1])

    def forward(self):
        """Advance the turtle forward one step."""
        direction = self.orientation.rotate(self.initial_direction)
        self.position = self.position + self.step * direction

    def roll(self, cw=False):
        """Roll the turtle CCW by the configured angle.

        :param cw: Whether to roll CW instead, defaults to False
        :param cw: bool, optional
        """
        if cw:
            q = Quaternion(axis=[0, 0, 1], angle=self.angle)
        else:
            q = Quaternion(axis=[0, 0, 1], angle=-self.angle)
        self.orientation = self.orientation.rotate(q)

    def pitch(self, down=False):
        """Pitch the turtle up by the configured angle.

        :param down: Whether to pitch down instead, defaults to False
        :param down: bool, optional
        """
        # TODO: This is the rotation axis in global coordinates. We want to rotate relative to the turtle.
        if not down:
            q = Quaternion(axis=[0, 1, 0], angle=self.angle)
        else:
            q = Quaternion(axis=[0, 1, 0], angle=-self.angle)
        self.orientation = q.rotate(self.orientation)

    def yaw(self, right=False):
        """Yaw the turtle left by the configured angle.

        :param right: Whether to yaw right instead, defaults to False
        :param right: bool, optional
        """
        if right:
            q = Quaternion(axis=[0, 1, 0], angle=self.angle)
        else:
            q = Quaternion(axis=[0, 1, 0], angle=-self.angle)
        self.orientation = self.orientation.rotate(q)

    def save(self):
        """Save the turtle's state on the stack."""
        raise NotImplementedError

    def restore(self):
        """Restore the turtle's state from the stack."""
        raise NotImplementedError
