import click
import jsonpickle

from irving import autotrader
from irving.cli.autotrader.groups import autotrader_group


@autotrader_group.command(help="Parse Autotrader listings.")
@click.argument("file", type=click.Path(exists=True))
def parse_listings(file):
    listings = autotrader.parse_listings(file)
    click.echo(jsonpickle.encode(listings, unpicklable=False))
