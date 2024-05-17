import click
import numpy as np

from .rigid_body import RigidBody
from .viewer import Viewer
from .prob_dist import ProbabilityDistribution


@click.group()
def show():
    pass


@show.command()
@click.option("--init-pos", nargs=2, type=float, default=[0., 0.], show_default=True)
@click.option("--pos-std", nargs=2, type=float, default=[0.2, 0.2], show_default=True)
@click.option("--angle-deg", type=float, default=30, show_default=True)
@click.option("--body-size", nargs=2, type=float, default=[2., 5.], show_default=True)
@click.option("--body-size-std", nargs=2, type=float, default=[1e-10, 1e-10], show_default=True)
@click.option("--dist-range-x", nargs=2, type=float, default=[-5, 5], show_default=True)
@click.option("--dist-range-y", nargs=2, type=float, default=[-5, 5], show_default=True)
@click.option("--dist-size", nargs=2, type=int, default=[100, 100], show_default=True)
def rigid_body(
        init_pos,
        pos_std,
        angle_deg,
        body_size,
        body_size_std,
        dist_range_x,
        dist_range_y,
        dist_size):
    rb = RigidBody(
            init_pos,
            pos_std,
            angle_deg,
            body_size,
            body_size_std)
    print(f"rigid body:\n{rb}")

    xs = np.linspace(dist_range_x[0], dist_range_x[1], dist_size[0])
    ys = np.linspace(dist_range_y[0], dist_range_y[1], dist_size[1])
    gridmap = np.meshgrid(xs, ys)

    pd = ProbabilityDistribution(gridmap)

    viewer = Viewer(gridmap)

    pd.add(rb)
    viewer.plot(pd.get())
