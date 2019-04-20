import numpy as np


# TODO: Allow initialization of array?
def rand_displacement_1d(recursions, scale, seed, hurst=0.5):
    """Generate a 1D heightmap using the random midpoint displacement algorithm.

    :param recursions: The number of recursive subdivisions to make
    :param scale: The vertical scale of the generated landscape
    :param seed: The random seed to use
    :param hurst: The Hurst roughness exponent, defaults to 0.5
    :returns: A 1D array of heights
    """
    np.random.seed(seed)
    N = 2 ** recursions
    x = np.zeros(N + 1)
    x[0], x[N] = scale * np.random.randn(2)

    # Calculate the diminishing variance.
    var = [
        np.sqrt((scale ** 2 / (2 ** (2 * l * hurst))) * (1 - 2 ** (2 * hurst - 2)))
        for l in range(recursions)
    ]

    def _recurse(t0, t2, level):
        """Recursively subdivide and perturb the midpoint with diminishing variance.

        :param t0: The left endpoint
        :param t2: The right endpoint
        :param level: The recursive level
        """
        # NOTE: t1 will always be an integer because N is a power of 2.
        t1 = (t0 + t2) // 2
        x[t1] = 0.5 * (x[t0] + x[t2]) + var[level - 1] * np.random.randn()

        if level < recursions:
            _recurse(t0, t1, level + 1)
            _recurse(t1, t2, level + 1)

    _recurse(0, N, 1)
    return x


# TODO: Allow initialization of array?
def rand_displacement_2d(recursions, scale, seed, hurst=0.5):
    """Generate a 2D heightmap using the random midpoint displacement algorithm.

    :param recursions: The number of recursive subdivisions to make
    :param scale: The vertical scale of the generated landscape
    :param seed: The random seed to use
    :param hurst: The Hurst roughness exponent, defaults to 0.5
    :returns: A 2D square matrix of heights
    """
    np.random.seed(seed)
    N = 2 ** recursions
    X = np.zeros((N + 1, N + 1))
    # Initialize the four corners to get started.
    X[0, 0], X[0, -1], X[-1, 0], X[-1, -1] = scale * np.random.randn(4)
    var = [
        np.sqrt((scale ** 2 / (2 ** (2 * l * hurst))) * (1 - 2 ** (2 * hurst - 2)))
        for l in range(recursions)
    ]

    def _recurse(x0, y0, x2, y2, level):
        """Recursively quadsect and perturb the five midpoints with diminishing variance.

        :param x0, y0: The coordinates of the upper left corner to subdivide
        :param x2, y2: The coordinates of the lower right corner to subdivide
        :param level: The recursive level
        """
        x1 = (x0 + x2) // 2
        y1 = (y0 + y2) // 2

        # TODO: Do this if they're unset to allow initialization.
        X[x0, y1] = 0.5 * (X[x0, y0] + X[x0, y2]) + var[level - 1] * np.random.randn()
        X[x1, y0] = 0.5 * (X[x0, y0] + X[x2, y0]) + var[level - 1] * np.random.randn()
        X[x2, y1] = 0.5 * (X[x2, y0] + X[x2, y2]) + var[level - 1] * np.random.randn()
        X[x1, y2] = 0.5 * (X[x0, y2] + X[x2, y2]) + var[level - 1] * np.random.randn()

        X[x1, y1] = (
            0.25 * (X[x0, y1] + X[x1, y0] + X[x2, y1] + X[x1, y2])
            + var[level - 1] * np.random.randn()
        )

        if level < recursions:
            _recurse(x0, y0, x1, y1, level + 1)
            _recurse(x1, y0, x2, y1, level + 1)
            _recurse(x1, y1, x2, y2, level + 1)
            _recurse(x0, y1, x1, y2, level + 1)

    _recurse(0, 0, N, N, 1)
    return X
