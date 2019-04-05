import unittest

import numpy as np
from pyquaternion import Quaternion

from fractals.graphics import Turtle3D


class TestTurtle3D(unittest.TestCase):
    def setUp(self):
        self.start_position = np.array([0, 0, 0])
        self.start_orientation = Quaternion(axis=[0, 0, 1], angle=0)

        self.step = 1
        self.angle = np.radians(90)

    def test_init(self):
        self.assertRaises(
            ValueError, Turtle3D, step=self.step, angle=self.angle, position={1, 2, 3}
        )
        self.assertRaises(ValueError, Turtle3D, step=self.step, angle=self.angle, orientation=42)
        self.assertRaises(
            ValueError,
            Turtle3D,
            step=self.step,
            angle=self.angle,
            position={1, 2, 3},
            orientation=42,
        )

        self.assertRaises(ValueError, Turtle3D, step=self.step, angle=self.angle, position=(0, 0))
        self.assertRaises(
            ValueError, Turtle3D, step=self.step, angle=self.angle, position=(0, 0, 0, 0)
        )

        t = Turtle3D(step=self.step, angle=self.angle)

        self.assertTrue(isinstance(t.position, np.ndarray))
        self.assertTrue(isinstance(t.orientation, Quaternion))
        self.assertTrue(np.all(t.position == self.start_position))
        self.assertEqual(t.orientation, self.start_orientation)

        t = Turtle3D(step=self.step, angle=self.angle, position=(1, 1, 1))

        self.assertTrue(isinstance(t.position, np.ndarray))
        self.assertTrue(isinstance(t.orientation, Quaternion))
        self.assertTrue(np.all(t.position == np.array([1, 1, 1])))
        self.assertEqual(t.orientation, self.start_orientation)

        t = Turtle3D(
            step=self.step, angle=self.angle, orientation=Quaternion(axis=[1, 0, 0], angle=np.pi)
        )

        self.assertTrue(isinstance(t.position, np.ndarray))
        self.assertTrue(isinstance(t.orientation, Quaternion))
        self.assertTrue(np.all(t.position == self.start_position))
        self.assertEqual(t.orientation, Quaternion(axis=[1, 0, 0], angle=np.pi))

    def test_forward(self):
        t = Turtle3D(step=self.step, angle=self.angle)

        self.assertTrue(np.all(t.position == np.array([0, 0, 0])))
        t.forward()
        self.assertTrue(np.all(t.position == np.array([0, 0, 1])))
        t.forward()
        self.assertTrue(np.all(t.position == np.array([0, 0, 2])))
        t.forward()
        self.assertTrue(np.all(t.position == np.array([0, 0, 3])))
        t.forward()
        self.assertTrue(np.all(t.position == np.array([0, 0, 4])))

    def test_pitch(self):
        t = Turtle3D(step=self.step, angle=self.angle)
        self.assertTrue(np.all(t.position == np.array([0, 0, 0])))
        # The starting orientation should be the turtle facing straight up with
        # its back towards the x axis.
        self.assertEqual(t.orientation, Quaternion(axis=[0, 0, 1], angle=0))

        t.pitch()
        # Should not move.
        self.assertTrue(np.all(t.position == np.array([0, 0, 0])))
        # Should be oriented in the x direction.
        self.assertEqual(t.orientation, Quaternion(axis=[1, 0, 0], angle=np.pi / 2))

        t.forward()
        self.assertTrue(np.all(t.position == np.array([1, 0, 0])))

        t.pitch(down=True)
        self.assertTrue(np.all(t.position == np.array([1, 0, 0])))
        self.assertEqual(t.orientation, Quaternion(axis=[0, 0, 1], angle=0))

        t.forward()
        self.assertTrue(np.all(t.position == np.array([1, 0, 1])))

        t = Turtle3D(step=self.step, angle=self.angle)
        t.pitch(down=True)
        self.assertEqual(t.orientation, Quaternion(axis=[-1, 0, 0], angle=0))
        t.forward()
        self.assertTrue(np.all(t.position == np.array([-1, 0, 0])))

    @unittest.skip("TODO: Write this test.")
    def test_yaw(self):
        self.fail()

    @unittest.skip("TODO: Write this test.")
    def test_roll(self):
        self.fail()

    @unittest.skip("TODO: Write this test.")
    def test_save(self):
        self.fail()

    @unittest.skip("TODO: Write this test.")
    def test_restore(self):
        self.fail()
