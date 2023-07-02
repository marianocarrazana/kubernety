from kubernetes import client, config
import click
from rich import print

from .gui import AppGUI
from .utils import var_dump

default_options = [
    click.option("--format", "-f", default="yaml", help="Output format"),
]


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


def get_client(**kargs):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    return v1


def run_gui(**kargs):
    kclient = get_client(**kargs)
    gui = AppGUI(kclient)
    gui.run()


@click.group(invoke_without_command=True)
@add_options(default_options)
@click.pass_context
def main(ctx, **kargs):
    if ctx.invoked_subcommand is None:
        run_gui(**kargs)


if __name__ == "__main__":
    main()
