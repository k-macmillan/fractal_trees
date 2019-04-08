import argparse
import json
import sys

import bpy


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Draw a collection of cylinders on Blender.")

    parser.add_argument("blend-files", type=str, nargs="+", help="The Blender files to join.")

    return parser.parse_args(argv)


def parse_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def main(args):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for file in args.blend_files:
        with bpy.data.libraries.load(file) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith("template")]

        for obj in data_to.objects:
            if obj is not None:
                bpy.context.scene.objects.link(obj)

    bpy.ops.wm.save_mainfile(filepath="joined.blend")


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
