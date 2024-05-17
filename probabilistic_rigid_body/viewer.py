import matplotlib.pyplot as plt


class Viewer():
    def __init__(self, meshgrid):
        self._meshgrid = meshgrid

        self._fig, self._ax = plt.subplots()
        self._ax.set_title("2D Gaussian Distribution Contour")
        self._ax.set_xlabel("X[m]")
        self._ax.set_ylabel("Y[m]")
        self._ax.axis("equal")

    def plot(self, prob_dist):
        self._ax.contourf(
                self._meshgrid[0],
                self._meshgrid[1],
                prob_dist,
                levels=50,
                cmap="viridis")

        plt.show()



def figure():
    return plt.figure()
