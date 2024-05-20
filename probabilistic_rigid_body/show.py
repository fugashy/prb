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
@click.option("--body-size-std", nargs=2, type=float, default=[1e-20, 1e-20], show_default=True)
@click.option("--dist-range-x", nargs=2, type=float, default=[-5, 5], show_default=True)
@click.option("--dist-range-y", nargs=2, type=float, default=[-5, 5], show_default=True)
@click.option("--dist-size", nargs=2, type=int, default=[100, 100], show_default=True)
@click.option("--iteration", type=int, default=1, show_default=True)
@click.option(
        "--pos-std-per-iteration",
        nargs=2,
        type=float,
        default=[1e-20, 1e-20],
        show_default=True)
@click.option(
        "--body-size-std-per-iteration",
        nargs=2,
        type=float,
        default=[1e-20, 1e-20],
        show_default=True)
@click.option("--fill-threshold", type=float, default=0.995, show_default=True)
def rigid_body(
        init_pos,
        pos_std,
        angle_deg,
        body_size,
        body_size_std,
        dist_range_x,
        dist_range_y,
        dist_size,
        iteration,
        pos_std_per_iteration,
        body_size_std_per_iteration,
        fill_threshold):
    rbs = [
        RigidBody(p, pos_std, angle_deg, bs, body_size_std)
        for p, bs in [
            (
                np.random.normal(init_pos, pos_std_per_iteration),
                np.random.normal(body_size, body_size_std_per_iteration)
            )
            for i in range(iteration)]]

    xs = np.linspace(dist_range_x[0], dist_range_x[1], dist_size[0])
    ys = np.linspace(dist_range_y[0], dist_range_y[1], dist_size[1])
    gridmap = np.meshgrid(xs, ys)

    pd = ProbabilityDistribution(gridmap)
    viewer = Viewer(gridmap, fill_threshold)

    for i, rb in enumerate(rbs):
        print(f"no {i+1}/{len(rbs)}")
        pd.add(rb)
        viewer.plot(pd.get())
        input("press enter to the next")
    input("press enter to exit")
