import click

from .show import show

@click.group()
def prb():
    pass


def main():
    commands = [
            show,
            ]
    [prb.add_command(c) for c in commands]

    prb()

