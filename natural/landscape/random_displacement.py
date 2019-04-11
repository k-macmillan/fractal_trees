import numpy as np


def rand_displacement_1d(recursions, scale, seed, hurst):
    """Generate a 1D heightmap using the random midpoint displacement algorithm.

    :param recursions: The number of recursive subdivisions to make.
    :param scale: The vertical scale of the generated landscape.
    :param seed: The random seed to use.
    :param hurst: The Hurst roughness exponent.
    :returns: A 1D array of heights.
    """
    np.random.seed(seed)
    N = 2 ** recursions
    x = np.zeros(N + 1)
    x[0], x[N] = scale * np.random.randn(2)

    def _recurse(t0, t2, level):
        """Recursively subdivide and perturb the midpoint with diminishing variance.

        :param t0: The left endpoint.
        :param t2: The right endpoint.
        :param level: The recursive level.
        """
        # NOTE: t1 will always be an integer because N is a power of 2.
        t1 = (t0 + t2) // 2
        # Calculate the diminishing variance.
        var = np.sqrt((scale ** 2 / (2 ** (2 * level * hurst))) * (1 - 2 ** (2 * hurst - 2)))
        x[t1] = 0.5 * (x[t0] + x[t2]) + var * np.random.randn()

        if level < recursions:
            _recurse(t0, t1, level + 1)
            _recurse(t1, t2, level + 1)

    _recurse(0, N, 1)
    return x
