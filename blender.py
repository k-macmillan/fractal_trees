import argparse
import itertools
import json
import sys

import numpy as np

import bpy
from fractals.grammar import Grammar
from fractals.graphics import Graphics
from mathutils import Vector


def draw(cylinder):
    """Add the given cylinder to the scene.

    Cylinder should be a dictionary with keys
    'from' & 'to' - The 3D coordinates to draw the cylinder from -> to.
    'radius' - The cylinder radius.
    'material' - The blender material to set the cylinder as.
    """
    center = tuple((c1 + c2) / 2 for c1, c2 in zip(cylinder["from"], cylinder["to"]))
    v = Vector(tuple(c1 - c2 for c1, c2 in zip(cylinder["from"], cylinder["to"])))
    u = Vector((0, 0, v.magnitude))
    q = u.rotation_difference(v)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=cylinder["radius"], depth=v.magnitude, location=center
    )
    bpy.ops.object.shade_smooth()
    bpy.context.active_object.rotation_mode = "QUATERNION"
    bpy.context.active_object.rotation_quaternion = (q.w, q.x, q.y, q.z)
    # TODO: Set cylinder material.
    # TODO: Join cylinder to existing cylinders?


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Draw a collection of cylinders on Blender.")

    # parser.add_argument("lstring", type=str, help="The lstring to draw and render.")

    return parser.parse_args(argv)


def parse_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def main(args):
    # TODO: Read in the config from a json file.
    config = {
        "unit": 2,
        "angle": np.pi / 4,
        "axiom": "F",
        "iterations": 5,
        "rules": {"F": "G[-F][F][+F]", "G": "GG"},
    }
    grammar = Grammar(config["rules"])

    print("Running", config["iterations"], "iterations on axiom:", config["axiom"])
    lstrings = grammar.iapply(config["axiom"])
    lstring = next(itertools.islice(lstrings, config["iterations"], config["iterations"] + 1))
    print("L-string:")
    print(lstring)

    graphics = Graphics(unit=config["unit"], angle=config["angle"])
    cylinders = graphics.draw(lstring)
    print("Saving", len(cylinders), "cylinders to 'data/lstring.json'")
    # graphics.dump(cylinders, "data/lstring")

    bpy.ops.wm.read_factory_settings(use_empty=True)

    for cylinder in cylinders:
        draw(cylinder)

    print("Rendering cylinders to 'data/lstring.blend'")
    bpy.ops.wm.save_mainfile(filepath="data/lstring.blend")


if __name__ == "__main__":
    argv = sys.argv
    if "--" not in argv:
        print("Use '--' to separate Blender args from script args.")
        print("Example: `blender --python script.py -- args`")
        print("Example: `blender --background --python script.py -- args`")
        argv = []
    else:
        argv = argv[argv.index("--") + 1 :]

    main(parse_args(argv))
