import argparse
import itertools
import json
import sys

import bpy
from fractals.grammar import Grammar
from fractals.graphics import Graphics
from mathutils import Vector


def draw_all(cylinders, c_count):
    """Inspiration: 
       https://blender.stackexchange.com/questions/7358/python-performance-with-blender-operators
    """
    sce = bpy.context.scene
    obs = []
    count = 1

    # cylinders are in the form [{"length": [cylinders]}]
    for clist in cylinders:
        # Generate ONE cylinder
        length, clist = next(iter(clist.items()))
        template = clist[0]

        v = Vector(tuple(c1 - c2 for c1, c2 in zip(template["from"], template["to"])))
        u = Vector((0, 0, v.magnitude))
        q = u.rotation_difference(v)
        
        bpy.ops.mesh.primitive_cylinder_add(
            radius=template["radius"],
            depth=v.magnitude,
            location=(0.0, 0.0, 0.0))
        if template["material"] == "Leaf":
            mat = bpy.data.materials.new("material_leaf")
            mat.diffuse_color = (0.0, 102 / 255, 0.0)
        elif template["material"] == "Branch":
            mat = bpy.data.materials.new("material_leaf")
            mat.diffuse_color = (51 / 255, 26 / 255, 0.0)

        ob = bpy.context.active_object
        ob.name = "template_" + length
        # print("Template name: ", ob.name)
        ob.active_material = mat
        ob.rotation_mode = "QUATERNION"
        ob.rotation_quaternion = (1, 0, 0, 0)

        # Copy it for the number of items in the dictionary list
        for cylinder in clist:
            duplicate = ob.copy()
            duplicate.data = duplicate.data.copy() # also duplicate mesh, remove for linked duplicate

            c = tuple((c1 + c2) / 2 for c1, c2 in zip(cylinder["from"], cylinder["to"]))
            v = Vector(tuple(c1 - c2 for c1, c2 in zip(cylinder["from"], cylinder["to"])))
            u = Vector((0, 0, v.magnitude))
            q = u.rotation_difference(v)
            duplicate.location = Vector((c[0], c[1], c[2]))
            duplicate.rotation_quaternion = (q.w, q.x, q.y, q.z)
            obs.append(duplicate)

            print("\rprogress: {}% : {}     ".format(100 * count // c_count, count), end="")
            count += 1

            # Perform join 
            if count % 200 == 0:
                bpy.ops.object.select_all(action='DESELECT')
                for thing in obs:
                    sce.objects.link(thing)
                    thing.select = True
                bpy.context.scene.objects.active = obs[0]
                bpy.ops.object.join()
                bpy.ops.object.select_all(action='DESELECT')
                obs.clear()

        # Cleanup
        bpy.ops.object.delete()

    # Link and update
    for thing in obs:
        sce.objects.link(thing)
    sce.update()

    # Join remainder
    bpy.context.scene.objects.active = obs[0]
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()
    bpy.ops.object.shade_smooth()
    bpy.ops.object.select_all(action='DESELECT')

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

    cylinder_count = 0
    for c in cylinders:
        cylinder_count += len(next(iter(c.values())))

    # print("Saving", len(cylinders), "cylinders to '" + basename + "-cylinders.json'")
    # graphics.dump(cylinders, basename + "-cylinders")
    print("Adding {} cylinders to Blender scene.".format(cylinder_count))

    # TODO: It's possible to combine objects from multiple blender files. Split up cylinders on large fractals.
    bpy.ops.wm.read_factory_settings(use_empty=True)

    draw_all(cylinders, cylinder_count)

    # for i, cylinder in enumerate(cylinders, start=1):
    #     print("\rprogress: {}%".format(100 * i // len(cylinders)), end="")
    #     draw(cylinder)

    #     if i % 20 == 0:
    #         bpy.ops.object.select_all(action='DESELECT')
    #         bpy.ops.object.select_by_type(type='MESH')
    #         bpy.ops.object.join()

    # bpy.ops.object.select_all(action='DESELECT')
    # bpy.ops.object.select_by_type(type='MESH')
    # bpy.ops.object.join()
    # bpy.ops.object.shade_smooth()

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
