import re
import struct
from typing import List, ByteString, BinaryIO
from enum import Enum


class UnsupportedFormats(Enum):
    SVG = 'SVG'


class SupportedFormats(Enum):
    PNG = 'PNG'
    GIF = 'GIF'


class ImagehError(Exception):
    pass


class UnknownFormatError(ImagehError):
    pass


class UnsupportedFormatError(ImagehError):
    pass


class ImageDescriptor(object):

    def __init__(self, format: str, width: int, height: int):
        self.format = format
        self.width = width
        self.height = height


class BaseParser(object):

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

    @staticmethod
    def check_format(head):
        return bool(re.search(b'PNG', head))

    def parse(self):
        chunk = self.fd.read(24)
        w, h = map(int, struct.unpack('>LL', chunk[16:24]))
        return ImageDescriptor(format='PNG', width=w, height=h)


class GIFParser(BaseParser):

    @staticmethod
    def check_format(head):
        return bool(re.search(b'GIF', head))

    def parse(self):
        chunk = self.fd.read(24)
        w, h = map(int, struct.unpack('<HH', chunk[6:10]))
        return ImageDescriptor(format='GIF', width=w, height=h)


def parse(path: str) -> ImageDescriptor:
    extension = path.split('.')[-1]
    if getattr(UnsupportedFormats, extension.upper(), None):
        raise UnsupportedFormatError('Unsupported file type: %s' % extension)
    with open(path, 'rb') as fd:
        return parse_fd(fd=fd)


def parse_fd(fd) -> ImageDescriptor:
    # 8 bytes is the length of PNG header (GIF has 6 byte header)
    chunk = fd.read(24)
    if chunk[:3] == b'GIF':
        format = SupportedFormats.GIF.value
        w, h = map(int, struct.unpack('<HH', chunk[6:10]))
    elif chunk[1:4] == b'PNG':
        format = SupportedFormats.PNG.value
        w, h = map(int, struct.unpack('>LL', chunk[16:24]))
    else:
        raise UnsupportedFormatError('Unknown image format')

    return ImageDescriptor(format, w, h)
