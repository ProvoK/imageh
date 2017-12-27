from enum import Enum
import json
import re
import struct
from typing import List, ByteString, BinaryIO


class ImagehError(Exception):
    pass


class UnknownFormatError(ImagehError):
    pass


class UnsupportedFormatError(ImagehError):
    pass


class CustomEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Enum):
            return o.name
        return json.JSONEncoder.default(self, o)


class ImageDescriptor(object):

    def __init__(self, format, width, height):
        # type: (str, int, int) -> None

        self.format = format
        self.width = width
        self.height = height

    def json(self):
        return json.dumps(self.__dict__, cls=CustomEncoder)


class PNGColourType(Enum):
    GREY_SCALE = 0
    TRUE_COLOUR = 2
    INDEXED_COLOUR = 3
    GREY_SCALE_ALPHA = 4
    TRUE_COLOUR_ALPHA = 6


class PNGFilterType(Enum):
    DEFAULT = 0
    SUB = 1
    UP = 2
    AVERAGE = 3
    PAETH = 4


class PNGCompressionType(Enum):
    STANDARD = 0


class PNGInterlaceType(Enum):
    NONE = 0
    ADAM7 = 1


class PNGDescriptor(ImageDescriptor):

    def __init__(self,
                 width,
                 height,
                 bit_depth=None,
                 colour_type=None,
                 compression=None,
                 filter_method=None,
                 interlace_method=None):
        super(PNGDescriptor, self).__init__('PNG', width, height)
        self.bit_depth = bit_depth
        self.colour_type = PNGColourType(colour_type)
        self.compression = PNGCompressionType(compression)
        self.filter_method = PNGFilterType(filter_method)
        self.interlace_method = PNGInterlaceType(interlace_method)


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
        # Width, Height, Bit depth, Colour type, Compression method
        # Filter method, Interlace method
        values = list(struct.unpack('>LLBBBBB', ihdr[0:13]))
        desc = PNGDescriptor(*values)
        return desc


class GIFParser(BaseParser):

    @staticmethod
    def check_format(head):
        return bool(re.search(b'GIF', head))

    def parse(self):
        chunk = self.fd.read(24)
        w, h = map(int, struct.unpack('<HH', chunk[6:10]))
        return ImageDescriptor(format='GIF', width=w, height=h)


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
