"""Generate fractal landscapes with the random midpoint displacement algorithm."""
import argparse
import itertools

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

from natural.landscape import rand_displacement_1d, rand_displacement_2d


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="""If multiple values for recursions, scale, or hurst are given,
    every combination of the given parameters will be plotted on the same axis.
    It is advisable to avoid plotting multiple 3D surface plots on the same axis.""",
    )

    parser.add_argument(
        "--one", action="store_true", default=False, help="Generate a 1D heightmap."
    )
    parser.add_argument(
        "--recursions",
        "-r",
        nargs="+",
        type=int,
        default=[6],
        help="The number of recursive subdivisions.",
    )
    parser.add_argument(
        "--scale", "-s", nargs="+", type=float, default=[1], help="The vertical scale."
    )
    parser.add_argument(
        "--hurst", "-H", nargs="+", type=float, default=[0.5], help="The Hurst roughness exponent."
    )
    parser.add_argument(
        "--seed", type=int, default=np.random.randint(2 ** 32 - 1), help="The random seed."
    )
    parser.add_argument(
        "--sealevel", "-l", type=float, default=None, help="The landscape sealevel."
    )
    parser.add_argument(
        "--title",
        "-t",
        type=str,
        default="Random Midpoint Displacement Results",
        help="The plot title.",
    )
    parser.add_argument(
        "--gui", action="store_true", default=False, help="Open the plot in a GUI window."
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None, help="The file to save the plot to."
    )

    return parser.parse_args()


def plot_1d(args):
    width = None
    for scale, hurst, recursions in itertools.product(args.scale, args.hurst, args.recursions):
        heightmap = rand_displacement_1d(
            recursions=recursions, scale=scale, hurst=hurst, seed=args.seed
        )
        if args.sealevel is not None:
            heightmap[heightmap < args.sealevel] = args.sealevel

        if width is None:
            width = len(heightmap)

        label = []

        if len(args.scale) > 1:
            label.append(r"$\sigma = {}$".format(scale))
        if len(args.hurst) > 1:
            label.append(r"$H = {}$".format(hurst))
        if len(args.recursions) > 1:
            label.append(r"$nrc = {}$".format(recursions))

        label = ", ".join(label) if label else None

        plt.plot(np.linspace(0, width, len(heightmap)), heightmap, label=label)

    plt.title(args.title)
    plt.xlabel(r"$x$")
    plt.ylabel(r"$h$")

    if label is not None:
        plt.legend()

    if args.output is not None:
        plt.savefig(args.output)

    if args.gui:
        plt.show()


def plot_2d(args):
    width, height = None, None
    floor = 0
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # NOTE: I would avoid plotting multiple surface plots together
    for scale, hurst, recursions in itertools.product(args.scale, args.hurst, args.recursions):
        heightmap = rand_displacement_2d(
            recursions=recursions, scale=scale, hurst=hurst, seed=args.seed
        )

        if args.sealevel is not None:
            heightmap[heightmap < args.sealevel] = args.sealevel

        if width is None or height is None:
            width, height = heightmap.shape

        X, Y = np.meshgrid(np.linspace(0, 10, width), np.linspace(0, 10, height))
        floor = min(heightmap.min(), floor)

        ax.plot_surface(
            X,
            Y,
            heightmap,
            linewidth=0.1,
            antialiased=False,
            cmap=sns.cubehelix_palette(reverse=True, dark=0.1, as_cmap=True),
        )
        if len(args.scale) == 1 and len(args.hurst) == 1 and len(args.recursions) == 1:
            ax.contour(
                X,
                Y,
                heightmap,
                20,
                zdir="z",
                offset=floor - 2.5,
                cmap=sns.cubehelix_palette(reverse=True, dark=0.1, as_cmap=True),
            )

    ax.set_zlim(floor - 2.5, heightmap.max())
    plt.title(args.title)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_zlabel(r"$h$")

    if args.output is not None:
        plt.savefig(args.output)

    if args.gui:
        plt.show()


def main(args):
    if args.one:
        plot_1d(args)
    else:
        plot_2d(args)


if __name__ == "__main__":
    main(parse_args())
