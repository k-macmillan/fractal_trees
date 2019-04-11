import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D


def __check_1d_args(xs, label):
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
def plot_displacement_1d(xs, labels=None, title=None, filename=None, gui=False):
    """Plot the given 1D fractal heightmap(s).

    :param xs: The heightmap or heightmaps to plot
    :type xs: Either an np.ndarray or tuple of np.ndarrays
    :param labels: The label or labels for each of the heightmaps, defaults to None
    :type labels: A string or tuple of strings, optional
    :param filename: The filename to save the plot to, defaults to None
    :param gui: Whether to open a GUI window with the plot, defaults to False
    """
    plt.clf()

    single = __check_1d_args(xs, labels)
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

    if title is None:
        plt.title("1D Random Midpoint Displacement")
    else:
        plt.title(title)
    plt.xlabel("$x$")
    plt.ylabel("$h$")

    if labels is not None:
        plt.legend()

    if filename is not None:
        plt.savefig(filename)

    if gui:
        plt.show()


def plot_displacement_2d(Z, title=None, filename=None, gui=False):
    """Plot the given 2D fractal heightmap.

    :param Z: The 2D heightmap to plot
    :param filename: The filename to save the plot to, defaults to None
    :param gui: Whether to open a GUI window with the plot, defaults to False
    """
    plt.clf()

    nx, ny = Z.shape
    X, Y = np.meshgrid(np.linspace(0, 10, nx), np.linspace(0, 10, ny))
    floor = Z.min()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # ax.view_init(axim=, elev=)

    ax.plot_surface(
        X,
        Y,
        Z,
        linewidth=0.1,
        antialiased=False,
        cmap=sns.cubehelix_palette(reverse=True, dark=0.1, as_cmap=True),
    )
    ax.contour(
        X,
        Y,
        Z,
        20,
        zdir="z",
        offset=floor - 2.5,
        cmap=sns.cubehelix_palette(reverse=True, dark=0.1, as_cmap=True),
    )
    ax.set_zlim(floor - 2.5, Z.max())

    if title is None:
        plt.title("2D Random Midpoint Displacement")
    else:
        plt.title(title)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$h$")

    if filename is not None:
        plt.savefig(filename)

    if gui:
        plt.show()
