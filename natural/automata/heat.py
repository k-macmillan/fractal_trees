import numba
import numpy as np


@numba.njit(cache=True)
def step(grid, temp):
    """Perform one time step of a 2D diffusion CA."""
    rows, cols = grid.shape
    for row in range(rows):
        # Do not update the left and right boundaries
        for col in range(1, cols - 1):
            # top, bottom = (row + 1) % rows, (row - 1) % rows
            left, right = col - 1, col + 1
            top = row - 1 if row != 0 else rows - 1
            bottom = row + 1 if row != rows - 1 else 0
            # Perform a four neighbor average, and wraparound the top and bottom.
            temp[row, col] = (
                grid[top, right] + grid[top, left] + grid[bottom, right] + grid[bottom, left]
            ) / 4
    grid[:, :] = temp[:, :]


def istep(rows, cols, xmin, xmax, ymin, ymax):
    domain = np.zeros((rows, cols))
    domain[:, 0] = np.linspace(ymin, ymax, cols) * (10 - np.linspace(ymin, ymax, rows))
    temporary = domain.copy()
    while True:
        step(domain, temporary)
        yield domain
