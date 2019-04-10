import argparse
import json
import sys

from natural.lindenmayer import Graphics


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Draw a collection of cylinders on Blender.")

    parser.add_argument("cylinders", type=str, help="The cylinders JSON file to use.")

    parser.add_argument("--job", type=int, default=None, help="This script's job number.")
    parser.add_argument("--jobs", type=int, default=None, help="The total number of jobs.")

    parser.add_argument("output", type=str, help="The the output filename.")

    return parser.parse_args(argv)


def parse_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def main(args):
    # TODO: Validate the JSON file.
    clist = parse_json(args.cylinders)

    start = None
    stop = None

    if args.job is not None and args.jobs is not None:
        chunksize = len(clist) // args.jobs
        start = args.job * chunksize
        stop = start + chunksize

    if start is not None or stop is not None:
        clist = clist[start:stop]

    cylinders = {}
    for c in clist:
        if c["length"] not in cylinders:
            cylinders[c["length"]] = [c]
        else:
            cylinders[c["length"]].append(c)
    Graphics.draw(cylinders, args.output)


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
