# -*- coding: utf-8 -*-

"""Console script for imageh."""
import json

import click

from imageh import imageh

UNSUPPORTED_ERROR = 'unsupported image format or not valid image URI'
INVALID_PATH_ERROR = 'file %s not found'


@click.command()
@click.argument('filename')
def cli(filename):
    """Console script for imageh."""
    try:
        desc = imageh.analyze(filename)
        print(desc.json())
    except FileNotFoundError:
        print(json.dumps(dict(error=INVALID_PATH_ERROR % filename)))
    except imageh.UnsupportedFormatError:
        print(json.dumps(dict(error=UNSUPPORTED_ERROR)))


if __name__ == "__main__":
    cli()
