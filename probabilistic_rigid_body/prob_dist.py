from copy import deepcopy
import numpy as np
from scipy.stats import (
        norm,
        )


class ProbabilityDistribution():
    def __init__(self, gridmap):
        self._gridmap = gridmap
        self._prob_dist = np.zeros(gridmap[0].shape)

    def get(self):
        return deepcopy(self._prob_dist)

    def add(self, rigid_body):
        x, y = rigid_body.pos
        xstd, ystd = rigid_body.pos_std

        angle = rigid_body.angle
        R = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]])

        w, l = rigid_body.size
        wstd, lstd = rigid_body.size_std

        for iy in range(self._prob_dist.shape[0]):
            for ix in range(self._prob_dist.shape[1]):
                cx = self._gridmap[0][iy, ix]
                cy = self._gridmap[1][iy, ix]

                rx, ry = R @ np.array([cx, cy]).T

                u"""
                任意の点 (x,y) について、その点が物体の内部にある確率は、
                その点が物体の重心から矩形の半分の幅w/2と高さh/2の範囲内にある確率に対応
                """
                px = norm.cdf(rx+w/2, x, xstd+wstd) - norm.cdf(rx-w/2, x, xstd+wstd)
                py = norm.cdf(ry+l/2, y, ystd+lstd) - norm.cdf(ry-l/2, y, ystd+lstd)
                self._prob_dist[iy, ix] += px * py

        # Normalize
        self._prob_dist = self._prob_dist / np.sum(self._prob_dist)
