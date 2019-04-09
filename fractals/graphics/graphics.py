import json

import numpy as np

import bpy
from mathutils import Vector

from .turtle import Turtle


class Graphics:
    """Interprets Lindenmayer graphics command strings to generate 3D cylinders.

    Command strings are composed of the following symbols.

    F,G - Advance in the current direction one unit while drawing.
    <,> - Roll CCW or CW, respectively, by one unit.
    ^,v - Pitch up or down, respectively, by one unit.
    -,+ - Yaw left or right, respectively, by one unit.
    [,] - Save or restore, respectively, the current state on the stack. Note that the saved state
          includes the color (or material), direction, pen up/down state, and cylinder radius.
    """

    @staticmethod
    def __check_args(radius, proportion):
        if radius is not None and proportion is not None:
            raise ValueError("`radius` and `proportion` are mutually exclusive.")

    def __init__(self, unit, angle, material=None, radius=None, proportion=None, randomness=None):
        """Initialize a Graphics object to draw command strings for fractals.

        If neither a radius or a proportionality constant is given, default to a constant radius
        of 0.2.

        :param unit: The length of each 'forward' command.
        :param angle: The angle of each 'rotate' and 'bend' command. In radians.
        :param material: The Blender material to make each cylinder object with, defaults to None.
        :param radius: The radius of each cylinder. Mutually exclusive with `proportion`.
        :param proportion: Make each cylinder's radius proportional to its length. Mutually
        exclusive with `radius`.
        :param randomness: If not None, the std deviation to randomly apply to each turtle move.
        """
        self.__check_args(radius, proportion)

        self.material = material
        self.radius = radius if radius is not None else 0.2
        self.proportion = proportion
        # TODO: Should the same amount of randomness be applied to the angles as the linear steps?
        self.randomness = randomness
        self.unit = unit
        self.angle = angle

        self.turtle = Turtle()

        self.mappings = {
            # Bind the distance and angle parameters to the turtle methods.
            "F": self.turtle.move,
            "G": self.turtle.move,
            "f": self.turtle.move,
            "g": self.turtle.move,
            "-": self.turtle.yaw,
            "+": self.turtle.yaw,
            "v": self.turtle.pitch,
            "^": self.turtle.pitch,
            "<": self.turtle.roll,
            ">": self.turtle.roll,
            "[": self.turtle.push,
            "]": self.turtle.pop,
        }

    def compute(self, commands):
        """Generate the 3D cylinders from the given graphics commands.

        :param commands: A string of successive graphics commands.
        :returns: A dictionary of (length, [{cyl 1}, {cyl 2}, ...]) pairs.
        """
        cylinders = []
        commands = iter(commands)
        for command in commands:
            perturbation = (
                np.random.normal(scale=self.randomness) if self.randomness is not None else 0
            )

            length = 0
            start = self.turtle.position
            # Consume consecutive forward commands.
            while command in ("G", "F"):
                self.mappings[command](self.unit + perturbation)
                length += self.unit
                try:
                    command = next(commands)
                except StopIteration:
                    # We've consumed the last command.
                    break
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
                        "length": length,
                    }
                )

            if command in self.mappings and command not in ("G", "F"):
                if command in ("+", "^", ">"):
                    self.mappings[command](+self.angle + perturbation)
                elif command in ("-", "v", "<"):
                    self.mappings[command](-self.angle + perturbation)
                else:
                    self.mappings[command]()

        return cylinders

    @staticmethod
    def dump(data, path):
        """Dump the cylinder data to a JSON file."""
        if data:
            with open(path + ".json", "w") as outfile:
                json.dump(data, outfile)

    @staticmethod
    def draw(cylinders, filename):
        """Draw the given cylinders.

        Use a template cylinder for each length to avoid a scene update for each cylinder.

        c.f. https://blender.stackexchange.com/questions/7358/python-performance-with-blender-operators

        :param cylinders: A dict of (length, [{cyl}, ...]) pairs.
        """
        bpy.ops.wm.read_factory_settings(use_empty=True)
        objs = []
        count = 1

        c_count = sum(len(clist) for clist in cylinders.values())

        # The cylinders dict has form {length: [cylinders]}
        for length, cylinder_list in cylinders.items():
            # Generate ONE cylinder to duplicate in the appropriate position.
            template_dict = cylinder_list[0]

            v = Vector(tuple(c1 - c2 for c1, c2 in zip(template_dict["from"], template_dict["to"])))

            # The primitive_cylinder_add forces a scene update.
            bpy.ops.mesh.primitive_cylinder_add(
                radius=template_dict["radius"], depth=v.magnitude, location=(10.0, 10.0, 10.0)
            )
            if template_dict["material"] == "Leaf":
                mat = bpy.data.materials.new("material_leaf")
                mat.diffuse_color = (0.0, 102 / 255, 0.0)
            elif template_dict["material"] == "Branch":
                mat = bpy.data.materials.new("material_branch")
                mat.diffuse_color = (51 / 255, 26 / 255, 0.0)

            template = bpy.context.active_object
            template.name = "template_" + str(length)
            # print("Template name: ", template.name)
            template.active_material = mat
            template.rotation_mode = "QUATERNION"
            template.rotation_quaternion = (1, 0, 0, 0)

            # Copy it for the number of items in the dictionary list
            for cylinder in cylinder_list:
                duplicate = template.copy()
                # also duplicate mesh, remove for linked duplicate
                duplicate.data = duplicate.data.copy()

                center = Vector(
                    tuple((c1 + c2) / 2 for c1, c2 in zip(cylinder["from"], cylinder["to"]))
                )
                v = Vector(tuple(c1 - c2 for c1, c2 in zip(cylinder["from"], cylinder["to"])))
                u = Vector((0, 0, v.magnitude))
                q = u.rotation_difference(v)
                duplicate.location = center
                duplicate.rotation_quaternion = (q.w, q.x, q.y, q.z)
                objs.append(duplicate)

                print("\rprogress: {}% ({})".format(100 * count // c_count, count), end="")
                count += 1

                # Every so often, add the objects to the scene and join them together.
                if count % 200 == 0:
                    bpy.ops.object.select_all(action="DESELECT")
                    # Add the objects to the scene and join them together.
                    for obj in objs:
                        bpy.context.scene.objects.link(obj)
                        obj.select = True
                    bpy.context.scene.objects.active = objs[0]
                    bpy.ops.object.join()
                    bpy.ops.object.select_all(action="DESELECT")
                    objs.clear()

            # Delete the template cylinder.
            template.select = True
            bpy.ops.object.delete()

        print("\nLinking remaining objects.")
        # Add any remaining objects to the scene.
        for obj in objs:
            bpy.context.scene.objects.link(obj)

        # Join the objects together, update the scene, and smooth the cylinders.
        bpy.context.scene.objects.active = objs[0]
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.join()
        bpy.context.scene.update()
        bpy.ops.object.shade_smooth()
        bpy.ops.object.select_all(action="DESELECT")

        print("\nSaving scene to '" + filename + "'")
        bpy.ops.wm.save_mainfile(filepath=filename)
