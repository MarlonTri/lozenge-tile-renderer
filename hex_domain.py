import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import random

a = np.array([0, 1])
b = np.array([-np.sqrt(3) / 2, -1 / 2])
c = np.array([np.sqrt(3) / 2, -1 / 2])

# replace these to change the colors
color_palette = {0: "#000000", 1: "#ff7f50", 2: "#f8c537", 3: "#25ced1"}
color_map = plt.get_cmap("inferno")
rng = np.random.default_rng()


class HexDomain:
    def __init__(self, size):
        """Creates a hexagonal domain with side length SIDE."""
        self.size = size

        self.gridpoints = np.zeros((self.size * 2, self.size * 2, 2)).astype(int)

    def in_hex(self):
        arr = np.indices(self.gridpoints.shape)
        arr1 = arr[0] + arr[1] + arr[2] >= self.size
        arr2 = arr[0] + arr[1] + arr[2] < 3 * self.size
        ret = np.logical_and(arr1, arr2).astype(int)
        return ret

    def hexant(self):
        """Determines the hexant(hexagon equivalent of quadrant) of an array of pts"""
        arr = np.indices(self.gridpoints.shape)
        axis1 = arr[0] < self.size
        axis2 = arr[0] + arr[1] + arr[2] >= 2 * self.size
        axis3 = arr[1] >= self.size
        axis = np.array([axis1, axis2, axis3]).astype(int)

        # No comment needed....self explanatory? (uhhh)
        return (
            -2 + 6 * (1 - axis[1]) + (2 * axis[1] - 1) * (axis[0] + axis[1] + axis[2])
        ) % 6

    def fill_min(self):
        """Fill the domain with lozenges to create the 'empty cube' tiling."""
        self.gridpoints = (1 + self.hexant() // 2) * self.in_hex()

    def rot_hex(self, x: int, y: int):
        arr = [
            (x, y, 0),
            (x - 1, y, 1),
            (x - 1, y, 0),
            (x - 1, y - 1, 1),
            (x, y - 1, 0),
            (x, y - 1, 1),
        ]
        for i in range(3):
            tmp = self.gridpoints[arr[i]]
            self.gridpoints[arr[i]] = self.gridpoints[arr[i + 3]]
            self.gridpoints[arr[i + 3]] = tmp

    def can_add(self):
        """Returns True iff there is a hexagon of three lozenges centered at POS."""
        arr = np.indices(self.gridpoints.shape[:2])[:, 1:, 1:]
        tri0 = self.gridpoints[arr[0], arr[1], 0]
        tri1 = self.gridpoints[arr[0] - 1, arr[1], 1]
        tri2 = self.gridpoints[arr[0] - 1, arr[1], 0]
        tri3 = self.gridpoints[arr[0] - 1, arr[1] - 1, 1]
        tri4 = self.gridpoints[arr[0], arr[1] - 1, 0]
        tri5 = self.gridpoints[arr[0], arr[1] - 1, 1]

        eq1 = (
            (tri0 == tri1)
            * (tri1 != tri2)
            * (tri2 == tri3)
            * (tri3 != tri4)
            * (tri4 == tri5)
            * (tri5 != tri0)
        )
        eq2 = (
            (tri1 == tri2)
            * (tri2 != tri3)
            * (tri3 == tri4)
            * (tri4 != tri5)
            * (tri5 == tri0)
            * (tri0 != tri1)
        )

        ret = np.array(np.where(eq1 + eq2)) + 1
        return ret.transpose()

    def sample(self, iters=10, q=1):
        """Runs MCMC.

        iters -- number of steps to run for.
        q -- amount of bias to add to the coin flip.  q=1 is 50/50.
        """

    def draw(self, s_size=1000):
        """Displays this domain and all of its lozenges."""

        grid_pix = s_size // (3 * self.size)
        plt.figure()
        gap = 1
        max_style = np.max(self.gridpoints)
        for (i, j, down), style in np.ndenumerate(self.gridpoints):
            if down:
                shape = np.array(((i + gap, i + gap, i), (j, j + gap, j + gap)))
            else:
                shape = np.array(((i, i + gap, i), (j, j, j + gap)))
            shape = shape.astype(float)
            shape[0] += shape[1] / 2
            shape = shape * grid_pix
            color = color_palette[0] if style == 0 else color_map(style / max_style)
            if style == 0:
                continue
            plt.fill(*shape, c=color)
        plt.axis("equal")
        plt.axis("off")
        plt.show()

    def save(self, name = "default"):
        """Creates a npy file containing the lozenges of this domain.  This is
        helpful if you are sampling a large domain and want your computer to
        take a break.  Be careful, there's no error handling.
        """
        np.save(f"{name}_points.npy", self.gridpoints)

    def load(self, name = "default"):
        """Loads a previously saved set of lozenges.  Be careful, there's no
        error handling.
        """
        self.gridpoints = np.load(f"{name}_points.npy")


domain = HexDomain(40)
domain.fill_min()
domain.load()

for i in range(10000000):
    if i % 200000 == 0:
        print("Drawing started!")
        domain.save()
        domain.draw()
    can_adds = domain.can_add() 
    pick = tuple( random.choice(list(can_adds)))
    #print(pick)
    domain.rot_hex(*pick)



domain.draw()
