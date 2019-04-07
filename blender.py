import argparse
import itertools
import json
import sys

from fractals.grammar import Grammar
from fractals.graphics import Graphics


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
    clist = graphics.compute(lstring)
    cylinders = {}
    for c in clist:
        if c["length"] not in cylinders:
            cylinders[c["length"]] = [c]
        else:
            cylinders[c["length"]].append(c)
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
    graphics.draw(cylinders, basename + ".blend")


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
