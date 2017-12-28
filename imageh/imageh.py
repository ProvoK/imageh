from enum import Enum
import json
import re
import struct
from typing import List, ByteString, BinaryIO

import attr


class ImagehError(Exception):
    pass


class UnknownFormatError(ImagehError):
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
        return json.dumps(self.__dict__, cls=SerializerJSONEncoder)


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
class BaseDescriptor(object):
    format = attr.ib(init=False)
    width = attr.ib()
    height = attr.ib()


@attr.s
class PNGDescriptor(BaseDescriptor, Serializer):
    format = 'PNG'
    bit_depth = attr.ib()
    color_type = attr.ib()
    compression = attr.ib()
    filter_method = attr.ib()
    interlace_method = attr.ib()


@attr.s
class GIFDescriptor(BaseDescriptor, Serializer):
    format = 'GIF'
    version = attr.ib()
    pixel_aspect_ratio = attr.ib()
    color_bits = attr.ib()
    color_table = attr.ib()
    color_table_size = attr.ib()
    color_table_sorted = attr.ib()


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
    ihdr_reg = re.compile(b'IHDR(.*)IDAT', flags=re.DOTALL)

    @staticmethod
    def check_format(head):
        return bool(re.search(b'PNG', head))

    def parse(self):
        """
        Sources:
            - https://en.wikipedia.org/wiki/Portable_Network_Graphics
            - https://www.w3.org/TR/2003/REC-PNG-20031110/
        """
        chunk = self.fd.read(42)
        ihdr = self.ihdr_reg.search(chunk).group(1)
        # Width, Height, Bit depth, Color type, Compression method
        # Filter method, Interlace method
        w, h, bd, ct, cm, fm, im = struct.unpack('>2L5B', ihdr[0:13])
        return PNGDescriptor(
            w, h, bd,
            PNGColorType(ct),
            PNGCompressionType(cm),
            PNGFilterType(fm),
            PNGInterlaceType(im)
        )


class GIFParser(BaseParser):

    @staticmethod
    def check_format(head):
        return bool(re.search(b'GIF', head))

    def parse(self):
        """
        Sources:
            - https://www.w3.org/Graphics/GIF/spec-gif89a.txt
        """
        chunk = self.fd.read(13)

        # Version, width, height, packed, background color index, pixel aspect ratio
        ver, w, h, pack, bci, par = struct.unpack('<3sHH3B', chunk[3:])

        packed_bin = bin(pack)[2:]
        color_table_flag = bool(packed_bin[0])
        color_resolution = int(packed_bin[1:4], 2) + 1
        sort_flag = bool(packed_bin[4])
        color_table_size = int(packed_bin[5:], 2)

        return GIFDescriptor(
            w, h, ver.decode('ascii'), par,
            color_resolution, color_table_flag,
            color_table_size, sort_flag
        )


def parse(path: str):
    # type: (str) -> ImageDescriptor
    """
    TODO DOC
    :param path: 
    :return: 
    """
    with open(path, 'rb') as fd:
        return parse_fd(fd=fd)


def parse_fd(fd):
    # type: (BinaryIO) -> ImageDescriptor
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
