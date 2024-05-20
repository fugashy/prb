import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import (
        GridSpec,
        GridSpecFromSubplotSpec
        )
from matplotlib.widgets import Cursor

_FIG_SCALE_FACTOR=0.6


class Viewer():
    def __init__(self, meshgrid):
        self._meshgrid = meshgrid

        self._fig = plt.figure(figsize=(
            10*_FIG_SCALE_FACTOR,
            8*_FIG_SCALE_FACTOR))

        self._gs_master = GridSpec(
                nrows=2,
                ncols=2,
                height_ratios=[1, 1])
        gs_main = GridSpecFromSubplotSpec(
                nrows=2,
                ncols=1,
                subplot_spec=self._gs_master[:, 0])
        gs_profile = GridSpecFromSubplotSpec(
                nrows=2,
                ncols=1,
                subplot_spec=self._gs_master[:, 1])

        self._ax_main = self._fig.add_subplot(gs_main[:, :])
        self._ax_main.set_title("P(x, y)")
        self._ax_main.set_xlabel("x[m]")
        self._ax_main.set_ylabel("y[m]")
        self._ax_main.axis("equal")

        self._ax_profile_by_name = {
                "row": {
                    "ax": self._fig.add_subplot(gs_profile[0, :]),
                    "gen_title": lambda xy: f"P(x|y={xy[1]:.2f})",
                    "xlabel": "x[m]",
                    "gen_ylabel": lambda xy: f"P(x|y={xy[1]:.2f})[-]"
                    },
                "col": {
                    "ax": self._fig.add_subplot(gs_profile[1, :]),
                    "gen_title": lambda xy: f"P(y|x={xy[0]:.2f})",
                    "xlabel": "y[m]",
                    "gen_ylabel": lambda xy: f"P(y|x={xy[1]:.2f})[-]"
                    },
                }
        for key in self._ax_profile_by_name.keys():
            conf = self._ax_profile_by_name[key]
            conf["ax"].clear()
            conf["ax"].set_ylim([0, 0.5])
            conf["ax"].set_title(conf["gen_title"]([0, 0]))
            conf["ax"].set_xlabel(conf["xlabel"])
            conf["ax"].set_ylabel(conf["gen_ylabel"]([0, 0]))

        self._gs_master.tight_layout(self._fig)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)

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
            conf["ax"].set_title(conf["gen_title"]([x, y]))
            conf["ax"].set_xlabel(conf["xlabel"])
            conf["ax"].set_ylabel(conf["gen_ylabel"]([x, y]))
            conf["ax"].plot(
                    profile_by_name[key]["x"],
                    profile_by_name[key]["values"])

        self._gs_master.tight_layout(self._fig)
        self._fig.canvas.draw()

