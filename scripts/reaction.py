"""Run the Gray-Scott Model with configurable parameters."""
import argparse

import seaborn as sns
import matplotlib.pyplot as plt

from natural.automata.reaction_diffusion import gray_scott


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="""If multiple values are given for some parameters, every combination of the given parameters will be plotted in the same window.""",
    )
    plot = parser.add_argument_group()

    plot.add_argument(
        "--gui", action="store_true", default=False, help="Open a GUI window displaying the plot."
    )
    plot.add_argument(
        "--output", "-o", type=str, default=None, help="The filename to save the results as."
    )
    plot.add_argument("--title", type=str, default=None, help="The plot title.")
    plot.add_argument(
        "--uv", action="store_true", default=False, help="Plot both U and V concentrations."
    )

    runtime = parser.add_argument_group()
    runtime.add_argument("--size", "-n", type=int, default=128, help="The grid size.")
    runtime.add_argument("--ru", type=float, default=0.14, help="The U diffusion rate.")
    runtime.add_argument("--rv", type=float, default=0.06, help="The V diffusion rate.")
    runtime.add_argument("--feed", "-f", type=float, default=0.035, help="The U feedrate.")
    runtime.add_argument("--kill", "-k", type=float, default=0.065, help="The U,V kill rate.")
    runtime.add_argument(
        "--iterations", "-i", type=int, default=1000, help="The number of iterations."
    )

    init = parser.add_argument_group()
    init.add_argument(
        "--radius",
        "-r",
        type=int,
        default=None,
        help="The initial high concentration center radius.",
    )
    init.add_argument(
        "--u0",
        type=float,
        default=0.5,
        help="The initial high concentration center U concentration.",
    )
    init.add_argument(
        "--v0",
        type=float,
        default=0.25,
        help="The initial high concentration center V concentration.",
    )
    init.add_argument(
        "--scale",
        "-s",
        type=float,
        default=0.02,
        help="The scale of the initial uniform distribution.",
    )

    return parser.parse_args()


def main(args):
    u, v = gray_scott(
        args.size,
        args.iterations,
        args.ru,
        args.rv,
        args.feed,
        args.kill,
        args.scale,
        args.radius,
        args.u0,
        args.v0,
    )

    if args.uv:
        _, axes = plt.subplots(1, 2)
        axes = iter(axes.flatten())

        axis = next(axes)
        sns.heatmap(u, square=True, xticklabels=False, yticklabels=False, ax=axis)
        axis.set_title("$U$ concentration")
        axis = next(axes)
        sns.heatmap(v, square=True, xticklabels=False, yticklabels=False, ax=axis)
        axis.set_title("$V$ concentration")
        plt.tight_layout()

        if args.title is not None:
            plt.title(args.title)

        if args.output is not None:
            plt.savefig(args.output)

        if args.gui:
            plt.show()
    else:
        sns.heatmap(u, square=True, xticklabels=False, yticklabels=False)
        if args.title is not None:
            plt.title(args.title)

        if args.output is not None:
            plt.savefig(args.output)

        if args.gui:
            plt.show()


if __name__ == "__main__":
    main(parse_args())
