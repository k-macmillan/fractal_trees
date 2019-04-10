import argparse
import itertools
import json
import sys

from natural.lindenmayer import Grammar, Graphics


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Draw a collection of cylinders on Blender.")

    parser.add_argument("config", type=str, help="The configuration JSON file to use.")

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

    graphics = Graphics(
        unit=config["unit"],
        angle=config["angle"],
        radius=config["radius"],
        proportion=config["proportion"],
        randomness=config["randomness"],
    )

    print("Computing all the cylinders.")
    cylinders = graphics.compute(lstring)

    print("Saving {} cylinders to {}-cylinders.json".format(len(cylinders), basename))
    graphics.dump(cylinders, basename + "-cylinders")


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
