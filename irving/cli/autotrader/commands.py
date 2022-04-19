import click
import jsonpickle

from irving.core import csv
from irving import autotrader
from irving.cli.autotrader.groups import autotrader_group


@autotrader_group.command(help="Parse Autotrader listings.")
@click.argument("file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Output to CSV file.")
def parse_listings(file, output):
    listings = autotrader.parse_listings(file)
    if output:
        csv.write_to_csv(path=output, listings=listings)
    else:
        click.echo(jsonpickle.encode(listings, unpicklable=False))
