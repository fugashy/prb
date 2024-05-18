import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import (
        GridSpec,
        GridSpecFromSubplotSpec
        )
from matplotlib.widgets import Cursor


class Viewer():
    def __init__(self, meshgrid):
        self._meshgrid = meshgrid

        self._fig = plt.figure()

        gs_master = GridSpec(
                nrows=2,
                ncols=2,
                height_ratios=[1, 1])
        gs_main = GridSpecFromSubplotSpec(
                nrows=2,
                ncols=1,
                subplot_spec=gs_master[:, 0])
        gs_profile = GridSpecFromSubplotSpec(
                nrows=2,
                ncols=1,
                subplot_spec=gs_master[:, 1])

        self._ax_main = self._fig.add_subplot(gs_main[:, :])
        self._ax_main.set_title("P(x, y)")
        self._ax_main.set_xlabel("x[m]")
        self._ax_main.set_ylabel("y[m]")
        self._ax_main.axis("equal")

        self._ax_profile_by_name = {
                "col": {
                    "ax": self._fig.add_subplot(gs_profile[0, :]),
                    "gen_title": lambda x: f"P(y|x={x:.2f})",
                    "xlabel": "y[m]",
                    "gen_ylabel": lambda x: f"P(y|x={x:.2f})[-]"
                    },
                "row": {
                    "ax": self._fig.add_subplot(gs_profile[1, :]),
                    "gen_title": lambda y: f"P(x|y={y:.2f})",
                    "xlabel": "x[m]",
                    "gen_ylabel": lambda y: f"P(x|y={y:.2f})[-]"
                    }
                }
        for key in self._ax_profile_by_name.keys():
            conf = self._ax_profile_by_name[key]
            conf["ax"].clear()
            conf["ax"].set_ylim([0, 0.5])
            conf["ax"].set_title(conf["gen_title"](0))
            conf["ax"].set_xlabel(conf["xlabel"])
            conf["ax"].set_ylabel(conf["gen_ylabel"](0))

        plt.tight_layout()

        self._cursor = Cursor(self._ax_main, useblit=True, color="red", linewidth=1)
        self._image = None

        self._fig.canvas.mpl_connect("motion_notify_event", self._update_profiles)


    def plot(self, prob_dist):
        self._ax_main.contourf(
                self._meshgrid[0],
                self._meshgrid[1],
                prob_dist,
                levels=50,
                cmap="viridis")

        self._image = prob_dist

        plt.show(block=False)

    def _update_profiles(self, event):
        if self._image is None:
            return
        if not event.inaxes == self._ax_main:
            return

        x, y = event.xdata, event.ydata
        col = np.argmin(np.abs(self._meshgrid[0][0, :] - x))
        row = np.argmin(np.abs(self._meshgrid[1][:, 0] - y))

        profile_by_name = {
                "col": {
                    "x": self._meshgrid[0][0, :],
                    "values": self._image[:, col] / np.sum(self._image[:, col]),
                    },
                "row": {
                    "x": self._meshgrid[1][:, 0],
                    "values": self._image[row, :] / np.sum(self._image[row, :]),
                    }
                }

        for key in profile_by_name.keys():
            conf = self._ax_profile_by_name[key]
            conf["ax"].clear()
            conf["ax"].set_ylim([0, 0.5])
            conf["ax"].set_title(conf["gen_title"](y))
            conf["ax"].set_xlabel(conf["xlabel"])
            conf["ax"].set_ylabel(conf["gen_ylabel"](y))
            conf["ax"].plot(
                    profile_by_name[key]["x"],
                    profile_by_name[key]["values"])

        plt.tight_layout()
        self._fig.canvas.draw()

