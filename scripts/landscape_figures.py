"""Reproducibly plot the landscape figures for the paper."""
import argparse
import os

from natural.landscape import rand_displacement_1d, plot_displacement_1d


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "basepath", type=str, default=".", nargs="?", help="The basepath to save the figures to."
    )
    return parser.parse_args()


def gen_1d_samples(basepath):
    # H = 1/2 is equivalent to ordinary Brownian motion.
    x = rand_displacement_1d(recursions=4, scale=2, hurst=0.5, seed=3)
    plot_displacement_1d(x, filename=basepath + "1d-simple-4-2-0_5-3.eps")

    x = rand_displacement_1d(recursions=10, scale=2, hurst=0.5, seed=37)
    plot_displacement_1d(x, filename=basepath + "1d-simple-10-2-0_5-37.eps")

    xs = []
    labels = []
    for nrc in (4, 6, 8, 10):
        xs.append(rand_displacement_1d(recursions=nrc, scale=2, hurst=0.5, seed=420))
        labels.append("$nrc = {}$".format(nrc))
    xs = tuple(xs)
    labels = tuple(labels)
    plot_displacement_1d(xs, labels, filename=basepath + "1d-nrc-2-0_5-420.eps")

    xs = []
    labels = []
    for scale in (0.5, 1, 2, 4):
        xs.append(rand_displacement_1d(recursions=5, scale=scale, hurst=0.5, seed=420))
        labels.append(r"$\sigma = {}$".format(scale))
    xs = tuple(xs)
    labels = tuple(labels)
    plot_displacement_1d(xs, labels, filename=basepath + "1d-5-sigma-0_5-420.eps")

    xs = []
    labels = []
    for hurst in (0.1, 0.3, 0.5, 0.7, 0.9):
        xs.append(rand_displacement_1d(recursions=5, scale=2, hurst=hurst, seed=420))
        labels.append("$H = {}$".format(hurst))
    xs = tuple(xs)
    labels = tuple(labels)
    plot_displacement_1d(xs, labels, filename=basepath + "1d-5-2-hurst-420.eps")


def main(args):
    if not args.basepath.endswith("/"):
        args.basepath += "/"

    gen_1d_samples(args.basepath)


if __name__ == "__main__":
    main(parse_args())
