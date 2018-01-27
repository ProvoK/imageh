import os
import subprocess

import pytest

from imageh.imageh import (
    PNGDescriptor,
    PNGColorType,
    PNGInterlaceType,
    PNGFilterType,
    PNGCompressionType,
    GIFDescriptor,
    PNGParser,
    GIFParser
)

join = os.path.join

TEST_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
FOLDER_PATH = join(TEST_DIR_PATH, 'static')

HTTP_PORT = 8888
HTTP_PATH = 'http://localhost:{}'.format(HTTP_PORT)


@pytest.fixture(autouse=True, scope='session')
def http_server():
    null_fd = open(os.devnull, 'w')
    proc = subprocess.Popen(
        ['python', '-m', 'http.server', str(HTTP_PORT)],
        cwd=FOLDER_PATH,
        stdout=null_fd,
        stderr=null_fd
    )
    yield
    proc.terminate()


def make_descriptor(**kwargs):
    cls = kwargs.pop('cls')
    descriptor = cls()
    for attr, value in kwargs.items():
        setattr(descriptor, attr, value)

    return descriptor


def png_images(base_path):
    return (
        (
            join(base_path, 'cat.png'),
            make_descriptor(
                cls=PNGDescriptor,
                width=960,
                height=603,
                bytes_read=PNGParser.bytes_to_read + 4,
                bit_depth=8,
                color_type=PNGColorType.TRUE_COLOUR_ALPHA,
                compression=PNGCompressionType.DEFLATE_INFLATE,
                filter_method=PNGFilterType.ADAPTIVE,
                interlace_method=PNGInterlaceType.NONE,
                filename='cat.png',
                url=join(base_path, 'cat.png'),
                extension='png',
                aspect_ratio='1.6:1'
            )
        ),
        (
            join(base_path, 'cat-png'),
            make_descriptor(
                cls=PNGDescriptor,
                width=960,
                height=603,
                bytes_read=PNGParser.bytes_to_read + 4,
                bit_depth=8,
                color_type=PNGColorType.TRUE_COLOUR_ALPHA,
                compression=PNGCompressionType.DEFLATE_INFLATE,
                filter_method=PNGFilterType.ADAPTIVE,
                interlace_method=PNGInterlaceType.NONE,
                filename='cat-png',
                url=join(base_path, 'cat-png'),
                extension='',
                aspect_ratio='1.6:1'
            )
        ),
    )


def gif_images(base_path):
    return (
        (
            join(base_path, 'spongebob.gif'),
            make_descriptor(
                cls=GIFDescriptor,
                width=500,
                height=334,
                bytes_read=GIFParser.bytes_to_read + 4,
                version='89a',
                pixel_aspect_ratio=0,
                color_bits=8,
                has_color_table=True,
                color_table_size=7,
                color_table_sorted=True,
                filename='spongebob.gif',
                url=join(base_path, 'spongebob.gif'),
                extension='gif',
                aspect_ratio='1.5:1'
            )
        ),
        (
            join(base_path, 'spongebob-gif'),
            make_descriptor(
                cls=GIFDescriptor,
                width=500,
                height=334,
                bytes_read=GIFParser.bytes_to_read + 4,
                version='89a',
                pixel_aspect_ratio=0,
                color_bits=8,
                has_color_table=True,
                color_table_size=7,
                color_table_sorted=True,
                filename='spongebob-gif',
                url=join(base_path, 'spongebob-gif'),
                extension='',
                aspect_ratio='1.5:1'
            )
        ),
        (
            join(base_path, 'happy_dog.gif'),
            make_descriptor(
                cls=GIFDescriptor,
                width=370,
                height=370,
                bytes_read=GIFParser.bytes_to_read + 4,
                version='89a',
                pixel_aspect_ratio=0,
                color_bits=8,
                has_color_table=True,
                color_table_size=7,
                color_table_sorted=True,
                filename='happy_dog.gif',
                url=join(base_path, 'happy_dog.gif'),
                extension='gif',
                aspect_ratio='1:1'
            )
        ),
        (
            join(base_path, 'happy_dog-gif'),
            make_descriptor(
                cls=GIFDescriptor,
                width=370,
                height=370,
                bytes_read=GIFParser.bytes_to_read + 4,
                version='89a',
                pixel_aspect_ratio=0,
                color_bits=8,
                has_color_table=True,
                color_table_size=7,
                color_table_sorted=True,
                filename='happy_dog-gif',
                url=join(base_path, 'happy_dog-gif'),
                extension='',
                aspect_ratio='1:1'
            )
        ),
    )


def images(base_path):
    return (*png_images(base_path), *gif_images(base_path))


def unsupported_images(base_path):
    return (join(base_path, 'homer.svg'),)
