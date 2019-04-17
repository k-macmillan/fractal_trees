import numpy as np
import scipy as sp


def laplacian(N):
    """Compute a matrix that performs the discretized Laplacian in 2D.

    c.f. https://stackoverflow.com/a/34905913
    c.f. https://rajeshrinet.github.io/blog/2016/gray-scott/
    c.f. p.75 in Computational Methods for Inverse Problems

    Surprisingly, there is not much information online on how to do this in Python specifically.
    Matlab has a `del2()` builtin function, but there are no equivalents in Python, even in the
    SciPy ecosystem.

    Note that this matrix will be N**2 x N**2, and operates on the *flattened* vectors u and v.
    """
    e = np.ones(N ** 2)
    # The upper and lower corners of the L_0 blocks.
    # e2 = np.array(([1] + [0] * (N - 1)) * N)
    # e3 = np.array(([0] * (N - 1) + [1]) * N)

    return sp.sparse.spdiags(
        data=[-4 * e, e, e, e, e, e, e],
        diags=[0, -1, 1, -N, N, -(N ** 2 + 1 - N), N ** 2 + 1 - N],
        m=N ** 2,
        n=N ** 2,
    )


def init(N):
    """Initialize the U, V concentrations."""
    u, v = np.ones((N, N)), np.zeros((N, N))
    u += 0.2 * np.random.random((N, N))
    v += 0.2 * np.random.random((N, N))
    c = N // 2
    # TODO: Play with this initialization.
    r = 16
    # u[c - r : c + r, c - r : c + r] = 0.0
    # v[c - r : c + r, c - r : c + r] = 0.0
    return u, v


def gray_scott(N, ru, rv, f, k, iters):
    """Run the Gray-Scott model with the given parameters.

    :param N: The domain size.
    :param ru: The diffusion rate for u
    :param rv: The diffusion rate for v
    :param f: The feed rate
    :param k: The kill rate
    :param iters: The number of iterations to run the model for
    :returns: a tuple of (u, v) concentration matrices
    """
    u, v = init(N)
    L = laplacian(N)
    u = u.reshape(N * N)
    v = v.reshape(N * N)

    for _ in range(iters):
        uvv = u * v ** 2
        u += ru * L @ u - uvv + f * (1 - u)
        v += rv * L @ v + uvv - (f + k) * v

    return u.reshape((N, N)), v.reshape((N, N))
