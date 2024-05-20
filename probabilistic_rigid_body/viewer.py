import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import (
        GridSpec,
        GridSpecFromSubplotSpec
        )
from matplotlib.widgets import Cursor

_FIG_SCALE_FACTOR=0.6


class Viewer():
    def __init__(self, meshgrid, fill_threshold):
        self._meshgrid = meshgrid
        self._fill_threshold = fill_threshold

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

        xs = self._meshgrid[0][0, :]
        ys = self._meshgrid[1][:, 0]

        col = np.argmin(np.abs(xs - x))
        row = np.argmin(np.abs(ys - y))

        profile_xs = self._image[row, :] / np.sum(self._image[row, :])
        profile_ys = self._image[:,col] / np.sum(self._image[:, col])

        def calc_fill_range(values, th):
            # 両サイドから中央値を求めて，その間をベースidxとする
            med_begin = 0.0
            med_begin_idx = 0
            for i, v in enumerate(values):
                med_begin += v
                if med_begin >= 0.5:
                    med_begin_idx = i
                    break
            med_end = 0.0
            med_end_idx = med_begin_idx
            for i, v in enumerate(values):
                if i <= med_begin_idx:
                    continue
                med_end += v
                if med_end >= 0.5:
                    med_end_idx = i
                    break

            base_idx = int((med_begin_idx + med_end_idx) / 2)

            prob_sum = 0.0
            d = 0
            try:
                while True:
                    if d == 0:
                        prob_sum += values[base_idx]
                    else:
                        prob_sum += values[base_idx + d]
                        prob_sum += values[base_idx - d]
                    # if prob_sum >= 0.9973:
                    if prob_sum >= th:
                        break
                    d += 1
            except IndexError:
                return [0, len(values)]
            return [
                    max([base_idx - d, 0]),
                    min([base_idx + d, len(values)])]

        th = 0.995
        fill_range_x = calc_fill_range(profile_xs, self._fill_threshold)
        fill_range_y = calc_fill_range(profile_ys, self._fill_threshold)

        profile_by_name = {
                "row": {
                    "x": xs,
                    "values": profile_xs,
                    "x_fill": xs[fill_range_x[0]:fill_range_x[1]],
                    "values_fill": profile_xs[fill_range_x[0]:fill_range_x[1]],
                    },
                "col": {
                    "x": ys,
                    "values": profile_ys,
                    "x_fill": ys[fill_range_y[0]:fill_range_y[1]],
                    "values_fill": profile_ys[fill_range_y[0]:fill_range_y[1]],
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
            conf["ax"].fill_between(
                    profile_by_name[key]["x_fill"],
                    profile_by_name[key]["values_fill"])

        self._gs_master.tight_layout(self._fig)
        self._fig.canvas.draw()

