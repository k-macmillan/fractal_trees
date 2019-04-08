import argparse
import json
import sys

import bpy


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Draw a collection of cylinders on Blender.")

    parser.add_argument("blendfiles", type=str, nargs="+", help="The Blender files to join.")
    parser.add_argument("output", type=str, help="The output filename.")

    return parser.parse_args(argv)


def parse_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def main(args):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for file in args.blendfiles:
        with bpy.data.libraries.load(file) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith("template")]

        for obj in data_to.objects:
            if obj is not None:
                bpy.context.scene.objects.link(obj)

    bpy.ops.wm.save_mainfile(filepath=args.output)


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
