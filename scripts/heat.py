"""Generate 2D heat diffusion plots with CAs."""
import argparse

import matplotlib.pyplot as plt
import seaborn as sns

from natural.automata import istep


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)

    ca_args = parser.add_argument_group()
    ca_args.add_argument("--ymin", type=float, default=0, help="The lower domain y boundary.")
    ca_args.add_argument("--ymax", type=float, default=10, help="The upper domain y boundary.")
    ca_args.add_argument(
        "--rows", type=int, default=25, help="The number of cells to use along the y axis."
    )
    ca_args.add_argument(
        "--cols", type=int, default=25, help="The number of cells to use along the x axis."
    )

    plot_args = parser.add_argument_group()
    plot_args.add_argument(
        "--timestep", "-i", type=int, default=10, help="The time interval to generate subplots at."
    )
    plot_args.add_argument("--prows", type=int, default=3, help="The number of rows of subplots.")
    plot_args.add_argument("--pcols", type=int, default=3, help="The number of columns of subplots")
    plot_args.add_argument("--title", type=str, default=None, help="The plot title.")
    plot_args.add_argument("--output", type=str, default=None, help="The output filename.")
    plot_args.add_argument(
        "--gui", action="store_true", default=False, help="Open the plot in a GUI window."
    )

    return parser.parse_args()


def main(args):
    _, axes = plt.subplots(args.prows, args.pcols)
    axes = iter(axes.flatten()) if args.prows * args.pcols != 1 else iter([axes])
    for i, domain in zip(
        range(1, args.timestep * args.prows * args.pcols + 1),
        istep(args.rows, args.cols, args.ymin, args.ymax),
    ):
        if i % args.timestep == 0:
            axis = next(axes)
            sns.heatmap(domain, square=True, xticklabels=False, yticklabels=False, ax=axis)
            axis.set_title(r"$t = {}$".format(i))

    if args.title is not None:
        plt.title(args.title)

    if args.output is not None:
        plt.savefig(args.output)

    if args.gui:
        plt.show()


if __name__ == "__main__":
    main(parse_args())
