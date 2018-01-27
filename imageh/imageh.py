from collections import namedtuple
from enum import Enum
from functools import partial
import json
import re
import struct

import attr

from .imports import (
    urlparse,
    urlopen,
    URLError
)


class ImagehError(Exception):
    pass


class UnknownFormatError(ImagehError):
    pass


class SerializerJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Enum):
            return o.name
        return json.JSONEncoder.default(self, o)


class Serializer(object):

    def json(self):
        return json.dumps(self.__dict__, sort_keys=True, cls=SerializerJSONEncoder)


class PNGColorType(Enum):
    GREY_SCALE = 0
    TRUE_COLOR = 2
    INDEXED_COLOUR = 3
    GREY_SCALE_ALPHA = 4
    TRUE_COLOUR_ALPHA = 6


class PNGFilterType(Enum):
    ADAPTIVE = 0
    SUB = 1
    UP = 2
    AVERAGE = 3
    PAETH = 4


class PNGCompressionType(Enum):
    DEFLATE_INFLATE = 0


class PNGInterlaceType(Enum):
    NONE = 0
    ADAM7 = 1


@attr.s
class Descriptor(object):
    width = attr.ib(init=False)
    height = attr.ib(init=False)
    bytes_read = attr.ib(init=False)
    format = attr.ib(init=False)
    filename = attr.ib(init=False)
    url = attr.ib(init=False)
    extension = attr.ib(init=False)
    aspect_ratio = attr.ib(init=False)


@attr.s
class PNGDescriptor(Descriptor, Serializer):
    format = 'PNG'
    bit_depth = attr.ib(init=False)
    color_type = attr.ib(init=False)
    compression = attr.ib(init=False)
    filter_method = attr.ib(init=False)
    interlace_method = attr.ib(init=False)


@attr.s
class GIFDescriptor(Descriptor, Serializer):
    format = 'GIF'
    version = attr.ib(init=False)
    pixel_aspect_ratio = attr.ib(init=False)
    color_bits = attr.ib(init=False)
    has_color_table = attr.ib(init=False)
    color_table_size = attr.ib(init=False)
    color_table_sorted = attr.ib(init=False)


class BaseParser(object):
    """
    TODO DOC
    """
    bytes_to_read = 0

    def __init__(self, fd, chunk):
        # type: (BinaryIO, List) -> None
        self.chunk = chunk + fd.read(self.bytes_to_read)

    @staticmethod
    def check_format(head):
        # type: (List[ByteString]) -> bool
        raise NotImplemented

    def parse(self):
        # type: () -> ImageDescriptor
        raise NotImplemented


class PNGParser(BaseParser):
    ihdr_reg = re.compile(b'IHDR', flags=re.DOTALL)
    bytes_to_read = 50

    @staticmethod
    def check_format(head):
        return bool(re.search(b'PNG', head))

    def parse(self):
        """
        Sources:
            - https://en.wikipedia.org/wiki/Portable_Network_Graphics
            - https://www.w3.org/TR/2003/REC-PNG-20031110/
        """
        ihdr_pos = self.ihdr_reg.search(self.chunk).start() + 4
        ihdr = self.chunk[ihdr_pos: ihdr_pos + 13]
        # Width, Height, Bit depth, Color type, Compression method
        # Filter method, Interlace method
        w, h, bd, ct, cm, fm, im = struct.unpack('>2L5B', ihdr[0:13])
        descriptor = PNGDescriptor()
        descriptor.width = w
        descriptor.height = h
        descriptor.bytes_read = len(self.chunk)
        descriptor.bit_depth = bd
        descriptor.color_type = PNGColorType(ct)
        descriptor.compression = PNGCompressionType(cm)
        descriptor.filter_method = PNGFilterType(fm)
        descriptor.interlace_method = PNGInterlaceType(im)
        return descriptor


class GIFParser(BaseParser):
    bytes_to_read = 13

    @staticmethod
    def check_format(head):
        return bool(re.search(b'GIF', head))

    def parse(self):
        """
        Sources:
            - https://www.w3.org/Graphics/GIF/spec-gif89a.txt
        """
        # Version, width, height, packed, background color index, pixel aspect ratio
        ver, w, h, pack, bci, par = struct.unpack('<3sHH3B', self.chunk[3:][:10])

        packed_bin = bin(pack)[2:]

        descriptor = GIFDescriptor()
        descriptor.version = ver.decode('ascii')
        descriptor.width = w
        descriptor.height = h
        descriptor.bytes_read = len(self.chunk)
        descriptor.pixel_aspect_ratio = par
        descriptor.color_bits = int(packed_bin[1:4], 2) + 1
        descriptor.has_color_table = bool(packed_bin[0])
        descriptor.color_table_size = int(packed_bin[5:], 2)
        descriptor.color_table_sorted = bool(packed_bin[4])

        return descriptor


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
    except Exception:
        # TODO log error
        raise ImagehError('Unknown error...see log')


def parse_fd(fd):
    # type: (BinaryIO) -> Descriptor
    """
    TODO DOC
    :param fd:
    :return:
    """
    chunk = fd.read(4)
    if PNGParser.check_format(chunk):
        parser = PNGParser(fd, chunk)
    elif GIFParser.check_format(chunk):
        parser = GIFParser(fd, chunk)
    else:
        raise UnknownFormatError('Unknown or not supported image format')

    return parser.parse()
