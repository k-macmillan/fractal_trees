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

    parser.add_argument(
        "--config",
        type=str,
        default="data/default.json",
        help="The config JSON file to use. If not provided, draw the default tree.",
    )

    return parser.parse_args(argv)


def parse_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def main(args):
    # TODO: Validate the JSON file.
    config = parse_json(args.config)

    # Run the L-system rules for the given number of iterations.
    grammar = Grammar(config["rules"])
    print("Running", config["iterations"], "iterations on axiom:", config["axiom"])
    lstrings = grammar.iapply(config["axiom"])
    lstring = next(itertools.islice(lstrings, config["iterations"], config["iterations"] + 1))
    print("L-string:")
    print(lstring)

    # Crunch the L-strings into a series of cylinders.
    graphics = Graphics(
        unit=config["unit"],
        angle=config["angle"],
        radius=config["radius"],
        proportion=config["proportion"],
    )
    print("Drawing the cylinders.")
    cylinders = graphics.draw(lstring)
    print("Saving", len(cylinders), "cylinders to 'data/lstring.json'")
    graphics.dump(cylinders, "data/lstring")

    print("Adding cylinders to Blender scene.")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for cylinder in cylinders:
        draw(cylinder)

    print("Saving scene to 'data/lstring.blend'")
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
