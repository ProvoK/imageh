from enum import Enum
import re
import struct

import attr

from . import BaseParser, BaseDescriptor
from ..serializer import Serializer


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
class Descriptor(BaseDescriptor, Serializer):
    format = 'PNG'
    bit_depth = attr.ib(init=False)
    color_type = attr.ib(init=False)
    compression = attr.ib(init=False)
    filter_method = attr.ib(init=False)
    interlace_method = attr.ib(init=False)


class Parser(BaseParser):
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
        descriptor = Descriptor()
        descriptor.width = w
        descriptor.height = h
        descriptor.bytes_read = len(self.chunk)
        descriptor.bit_depth = bd
        descriptor.color_type = PNGColorType(ct)
        descriptor.compression = PNGCompressionType(cm)
        descriptor.filter_method = PNGFilterType(fm)
        descriptor.interlace_method = PNGInterlaceType(im)
        return descriptor

