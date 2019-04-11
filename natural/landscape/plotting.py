import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def __check_1d_args(xs, label, filename):
    if not isinstance(xs, (np.ndarray, tuple)):
        raise ValueError("'xs' must be an np.ndarray or tuple of np.ndarrays")

    if label is not None and not isinstance(label, (str, tuple)):
        raise ValueError("'label' must be a string or tuple of strings")

    if isinstance(xs, np.ndarray) and label is not None and not isinstance(label, str):
        raise ValueError("If plotting one heightmap, 'label' must be a string")

    if isinstance(xs, tuple) and label is not None and not isinstance(label, tuple):
        raise ValueError("If plotting multiple heightmaps, 'label' must be a tuple of strings.")

    if isinstance(xs, tuple) and isinstance(label, tuple) and not len(xs) == len(label):
        raise ValueError("Lengths of 'xs' and 'label' must match.")

    # Indicate whether we're plotting a single heightmap or multiple.
    return isinstance(xs, np.ndarray)


# TODO: Pass in the title?
def plot_displacement_1d(xs, labels=None, filename=None, gui=False):
    """Plot the given 1D fractal heightmap(s).

    :param xs: The heightmap or heightmaps to plot
    :param xs: Either an np.ndarray or tuple of np.ndarrays
    :param labels: The label or labels for each of the heightmaps, defaults to None
    :param labels: A string or tuple of strings, optional
    :param filename: The filename to save the plot to, defaults to None
    """
    plt.clf()

    single = __check_1d_args(xs, labels, filename)
    if single:
        xs = (xs,)
        _labels = (labels,)
    else:
        if labels is None:
            _labels = tuple([None] * len(xs))
        _labels = labels

    # Find max width of the given heightmaps.
    width = max(len(h) for h in xs)

    for heightmap, label in zip(xs, _labels):
        plt.plot(np.linspace(0, width, len(heightmap)), heightmap, label=label)

    plt.title("1D Random Midpoint Displacement")
    plt.xlabel("$x$")
    plt.ylabel("$h$")

    if labels is not None:
        plt.legend()

    if filename is not None:
        plt.savefig(filename)

    if gui:
        plt.show()
