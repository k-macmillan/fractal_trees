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


def init(N, scale, r, u0, v0):
    """Initialize the U, V concentrations."""
    u, v = np.ones((N, N)), np.zeros((N, N))
    u += scale * np.random.random((N, N))
    v += scale * np.random.random((N, N))
    c = N // 2
    # TODO: Play with this initialization.
    if r is not None:
        u[c - r : c + r, c - r : c + r] = u0
        v[c - r : c + r, c - r : c + r] = v0
    return u, v


def gray_scott(N, iters, ru, rv, f, k, scale, r, u0, v0):
    """Run the Gray-Scott model with the given parameters.

    :param N: The domain size.
    :param iters: The number of iterations to run the model for
    :param ru: The diffusion rate for u
    :param rv: The diffusion rate for v
    :param f: The feed rate
    :param k: The kill rate
    :param scale: The scale of the random initialization
    :param r: The size of the center, high concentration, initialization, if not None
    :param u0, v0: The center initial concentrations of U and V
    :returns: a tuple of (u, v) concentration matrices
    """
    u, v = init(N, scale=scale, r=r, u0=u0, v0=v0)
    L = laplacian(N)
    u = u.reshape(N * N)
    v = v.reshape(N * N)

    for _ in range(iters):
        uvv = u * v ** 2
        u += ru * L @ u - uvv + f * (1 - u)
        v += rv * L @ v + uvv - (f + k) * v

    return u.reshape((N, N)), v.reshape((N, N))
