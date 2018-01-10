from enum import Enum
import json
import re
import struct
from urllib.parse import urlparse

import attr


class ImagehError(Exception):
    pass


class UnsupportedFormatError(ImagehError):
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

    def __init__(self, fd):
        # type: (BinaryIO) -> None
        self.fd = fd
        self.fd.seek(0)

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
        chunk = self.fd.read(self.bytes_to_read)
        ihdr_pos = self.ihdr_reg.search(chunk).start() + 4
        ihdr = chunk[ihdr_pos: ihdr_pos + 13]
        # Width, Height, Bit depth, Color type, Compression method
        # Filter method, Interlace method
        w, h, bd, ct, cm, fm, im = struct.unpack('>2L5B', ihdr[0:13])
        descriptor = PNGDescriptor()
        descriptor.width = w
        descriptor.height = h
        descriptor.bytes_read = self.bytes_to_read
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
        chunk = self.fd.read(self.bytes_to_read)

        # Version, width, height, packed, background color index, pixel aspect ratio
        ver, w, h, pack, bci, par = struct.unpack('<3sHH3B', chunk[3:])

        packed_bin = bin(pack)[2:]

        descriptor = GIFDescriptor()
        descriptor.version = ver.decode('ascii')
        descriptor.width = w
        descriptor.height = h
        descriptor.bytes_read = self.bytes_to_read
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


def parse_uri(url):
    # type: (str) -> (str, str)
    """
    Returns tuple with (filename, extension) as strings.
    """
    p = urlparse(url)
    filename = p.geturl().split('/')[-1]
    extension = filename.split('.')[-1] if '.' in filename else ''
    return filename, extension


def parse(url: str):
    # type: (str) -> Descriptor
    """
    TODO DOC
    :param url:
    :return:
    """
    with open(url, 'rb') as fd:
        desc = parse_fd(fd=fd)
        filename, extension = parse_uri(url)
        desc.url = url
        desc.filename = filename
        desc.extension = extension
        desc.aspect_ratio = calculate_aspect_ratio(desc.width, desc.height)

        return desc


def parse_fd(fd):
    # type: (BinaryIO) -> Descriptor
    """
    TODO DOC
    :param fd:
    :return:
    """
    chunk = fd.read(4)
    if PNGParser.check_format(chunk):
        parser = PNGParser(fd)
    elif GIFParser.check_format(chunk):
        parser = GIFParser(fd)
    else:
        raise UnsupportedFormatError('Unknown image format')

    return parser.parse()
