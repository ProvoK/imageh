import os

from imageh.imageh import (
    PNGDescriptor,
    PNGColorType,
    PNGInterlaceType,
    PNGFilterType,
    PNGCompressionType,
    GIFDescriptor,
)

root_path = os.path.dirname(os.path.abspath(__file__))
join = os.path.join


def make_descriptor(**kwargs):
    cls = kwargs.pop('cls')
    descriptor = cls()
    for attr, value in kwargs.items():
        setattr(descriptor, attr, value)

    return descriptor

PNG_IMAGES = (
    (
        join(root_path, 'static/cat.png'),
        make_descriptor(
            cls=PNGDescriptor,
            width=960,
            height=603,
            bytes_read=50,
            bit_depth=8,
            color_type=PNGColorType.TRUE_COLOUR_ALPHA,
            compression=PNGCompressionType.DEFLATE_INFLATE,
            filter_method=PNGFilterType.ADAPTIVE,
            interlace_method=PNGInterlaceType.NONE,
            filename='cat.png',
            url=join(root_path, 'static/cat.png'),
            extension='png',
            aspect_ratio='1.6:1'
        )
    ),
    (
        join(root_path, 'static/cat-png'),
        make_descriptor(
            cls=PNGDescriptor,
            width=960,
            height=603,
            bytes_read=50,
            bit_depth=8,
            color_type=PNGColorType.TRUE_COLOUR_ALPHA,
            compression=PNGCompressionType.DEFLATE_INFLATE,
            filter_method=PNGFilterType.ADAPTIVE,
            interlace_method=PNGInterlaceType.NONE,
            filename='cat-png',
            url=join(root_path, 'static/cat-png'),
            extension='',
            aspect_ratio='1.6:1'
        )
    ),
)

GIF_IMAGES = (
    (
        join(root_path, 'static/spongebob.gif'),
        make_descriptor(
            cls=GIFDescriptor,
            width=500,
            height=334,
            bytes_read=13,
            version='89a',
            pixel_aspect_ratio=0,
            color_bits=8,
            has_color_table=True,
            color_table_size=7,
            color_table_sorted=True,
            filename='spongebob.gif',
            url=join(root_path, 'static/spongebob.gif'),
            extension='gif',
            aspect_ratio='1.5:1'
        )
    ),
    (
        join(root_path, 'static/spongebob-gif'),
        make_descriptor(
            cls=GIFDescriptor,
            width=500,
            height=334,
            bytes_read=13,
            version='89a',
            pixel_aspect_ratio=0,
            color_bits=8,
            has_color_table=True,
            color_table_size=7,
            color_table_sorted=True,
            filename='spongebob-gif',
            url=join(root_path, 'static/spongebob-gif'),
            extension='',
            aspect_ratio='1.5:1'
        )
    ),
    (
        join(root_path, 'static/happy_dog.gif'),
        make_descriptor(
            cls=GIFDescriptor,
            width=370,
            height=370,
            bytes_read=13,
            version='89a',
            pixel_aspect_ratio=0,
            color_bits=8,
            has_color_table=True,
            color_table_size=7,
            color_table_sorted=True,
            filename='happy_dog.gif',
            url=join(root_path, 'static/happy_dog.gif'),
            extension='gif',
            aspect_ratio='1:1'
        )
    ),
    (
        join(root_path, 'static/happy_dog-gif'),
        make_descriptor(
            cls=GIFDescriptor,
            width=370,
            height=370,
            bytes_read=13,
            version='89a',
            pixel_aspect_ratio=0,
            color_bits=8,
            has_color_table=True,
            color_table_size=7,
            color_table_sorted=True,
            filename='happy_dog-gif',
            url=join(root_path, 'static/happy_dog-gif'),
            extension='',
            aspect_ratio='1:1'
        )
    ),
)

IMAGES = (*PNG_IMAGES, *GIF_IMAGES)


UNSUPPORTED_IMAGES = (
    join(root_path, 'static/homer.svg'),
)
