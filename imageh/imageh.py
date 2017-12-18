import struct

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

    def __init__(self, format_: str, width: int, height: int):
        self.format_ = format_
        self.width = width
        self.height = height


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
        format_ = SupportedFormats.GIF.value
        w, h = map(int, struct.unpack('<HH', chunk[6:10]))
    elif chunk[1:4] == b'PNG':
        format_ = SupportedFormats.PNG.value
        w, h = map(int, struct.unpack('>LL', chunk[16:24]))

    return ImageDescriptor(format_, w, h)
