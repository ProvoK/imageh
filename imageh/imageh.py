from collections import namedtuple
from functools import partial

from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError
from . import formats


class ImagehError(Exception):
    pass


class UnknownFormatError(ImagehError):
    pass


def calculate_aspect_ratio(width, height):
    # type: (int, int) -> str
    ratio = round(width/height, 1)
    if ratio % 1 == 0:
        ratio = int(ratio)
    return '{}:{}'.format(ratio, 1)


ParsedURL = namedtuple('ParsedURL', ['scheme', 'filename', 'extension'])


def parse_uri(url):
    # type: (str) -> ParsedURL
    """Returns a ParsedURL namedtuple."""
    p = urlparse(url)
    filename = p.geturl().split('/')[-1]
    extension = filename.split('.')[-1] if '.' in filename else ''
    return ParsedURL(scheme=p.scheme, filename=filename, extension=extension)


def analyze(url: str):
    # type: (str) -> Descriptor
    """
    TODO DOC
    :param url:
    :return:
    """

    open_func = urlopen if url.startswith('http') else partial(open, mode='rb')
    try:
        with open_func(url) as fd:
            desc = parse_fd(fd=fd)
            parse_res = parse_uri(url)
            desc.url = url
            desc.filename = parse_res.filename
            desc.extension = parse_res.extension
            desc.aspect_ratio = calculate_aspect_ratio(desc.width, desc.height)

            return desc
    except (FileNotFoundError, URLError) as err:
        raise FileNotFoundError(err) from err
    except UnknownFormatError:
        raise
    except Exception as err:
        # TODO log error
        raise ImagehError('Unknown error...{}'.format(err))


def parse_fd(fd):
    # type: (BinaryIO) -> Descriptor
    """
    TODO DOC
    :param fd:
    :return:
    """
    chunk = fd.read(4)

    for parser_cls in formats.load():
        if parser_cls.check_format(chunk):
            parser = parser_cls(fd, chunk)
            return parser.parse()
    raise UnknownFormatError('Unknown or not supported image format')
