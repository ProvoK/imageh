# -*- coding: utf-8 -*-

"""Console script for imageh."""
import json

import click

from imageh import imageh

UNSUPPORTED_ERROR = 'unknown or unsupported image format or not valid image URI'
INVALID_PATH_ERROR = 'file %s not found'
GENERAL_ERROR = 'unknown error'


@click.command()
@click.argument('filename')
def cli(filename):
    """Console script for imageh."""
    try:
        desc = imageh.analyze(filename)
        print(desc.json())
    except FileNotFoundError:
        print(json.dumps(dict(error=INVALID_PATH_ERROR % filename)))
    except imageh.UnknownFormatError:
        print(json.dumps(dict(error=UNSUPPORTED_ERROR)))
    except Exception:
        print(json.dumps(dict(error=GENERAL_ERROR)))


if __name__ == "__main__":
    cli()
