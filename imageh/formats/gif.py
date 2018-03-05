import re
import struct

from . import BaseDescriptor, BaseParser
from ..serializer import Serializer


class Descriptor(BaseDescriptor, Serializer):
    format = 'GIF'
    version = None
    pixel_aspect_ratio = None
    color_bits = None
    has_color_table = None
    color_table_size = None
    color_table_sorted = None


class Parser(BaseParser):
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

        descriptor = Descriptor()
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


