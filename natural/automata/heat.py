import numba
import numpy as np


@numba.njit(cache=True)
def step(grid, temp):
    """Perform one time step of a 2D diffusion CA."""
    rows, cols = grid.shape
    for row in range(rows):
        # Do not update the left and right boundaries
        for col in range(1, cols - 1):
            # Perform a four neighbor average, and wraparound the top and bottom.
            temp[row, col] = (
                grid[(row + 1) % rows, col + 1]
                + grid[(row + 1) % rows, col - 1]
                + grid[(row - 1) % rows, col + 1]
                + grid[(row - 1) % rows, col - 1]
            ) / 4
    grid[:, :] = temp[:, :]


def istep(rows, cols, xmin, xmax, ymin, ymax):
    domain = np.zeros((rows, cols))
    domain[:, 0] = np.linspace(ymin, ymax, cols) * (10 - np.linspace(ymin, ymax, rows))
    temporary = domain.copy()
    while True:
        step(domain, temporary)
        yield domain
