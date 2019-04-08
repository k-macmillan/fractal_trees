import argparse
import json
import sys

from fractals.graphics import Graphics


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Draw a collection of cylinders on Blender.")

    parser.add_argument("cylinders", type=str, help="The cylinders JSON file to use.")

    # If start, stop are given, only render a portion of the file.
    parser.add_argument(
        "--start", type=int, default=None, help="The starting index of the JSON array."
    )
    parser.add_argument(
        "--stop", type=int, default=None, help="The ending index of the JSON array."
    )

    return parser.parse_args(argv)


def parse_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def main(args):
    # TODO: Validate the JSON file.
    clist = parse_json(args.cylinders)

    # TODO: If start and/or stop are given, modify the filename.
    if args.start is not None or args.stop is not None:
        clist = clist[args.start : args.stop]

    # Extensionless filename to save everything as.
    basename = args.cylinders.replace(".json", "")

    cylinders = {}
    for c in clist:
        if c["length"] not in cylinders:
            cylinders[c["length"]] = [c]
        else:
            cylinders[c["length"]].append(c)
    Graphics.draw(cylinders, basename + ".blend")


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
