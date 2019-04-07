import argparse
import itertools
import json
import sys

import bpy
from fractals.grammar import Grammar
from fractals.graphics import Graphics
from mathutils import Vector


def draw_all(cylinders):
    """Draw the given cylinders.

    Use a template cylinder for each length to avoid a scene update for each cylinder.

    c.f. https://blender.stackexchange.com/questions/7358/python-performance-with-blender-operators

    :param cylinders: A dict of (length, [{cyl}, ...]) pairs.
    """
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
    # Extensionless filename to save everything as.
    basename = args.config.replace(".json", "")

    # Run the L-system rules for the given number of iterations.
    grammar = Grammar(config["rules"])
    print("Running", config["iterations"], "iterations on axiom:", config["axiom"])
    lstrings = grammar.iapply(config["axiom"])
    # Get the nth iteration, skipping all the intermediate forms.
    lstring = next(itertools.islice(lstrings, config["iterations"], config["iterations"] + 1))
    # print("L-string:")
    # print(lstring)

    # Crunch the L-strings into a series of cylinders.
    graphics = Graphics(
        unit=config["unit"],
        angle=config["angle"],
        radius=config["radius"],
        proportion=config["proportion"],
    )
    print("Drawing the cylinders.")
    cylinders = graphics.draw(lstring)
    c_count = sum(len(clist) for clist in cylinders.values())

    print(
        "Saving",
        c_count,
        "cylinders with",
        len(cylinders),
        "different lengths to '" + basename + "-cylinders.json'",
    )
    graphics.dump(cylinders, basename + "-cylinders")
    print("Adding {} cylinders to Blender scene.".format(c_count))

    # TODO: It's possible to combine objects from multiple blender files. Split up cylinders on large fractals.
    bpy.ops.wm.read_factory_settings(use_empty=True)

    draw_all(cylinders)

    print("\nSaving scene to '" + basename + ".blend'")
    bpy.ops.wm.save_mainfile(filepath=basename + ".blend")


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
