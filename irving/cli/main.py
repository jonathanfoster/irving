import click
from click.exceptions import ClickException, Exit

from irving import __version__


class ExceptionHandler(click.Group):
    def invoke(self, ctx):
        try:
            return super().invoke(ctx)
        except Exception as exc:  # pylint: disable=broad-except
            if isinstance(exc, Exit):
                raise
            ClickException.show(click.ClickException(str(exc)))
        return None


@click.group(cls=ExceptionHandler, help="Irving helps you estimate how much your car is worth.")
@click.version_option(version=__version__)
def main():
    pass
