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

PNG_IMAGES = (
    (
        join(root_path, 'static/cat.png'),
        PNGDescriptor(
            960, 603, 8,
            PNGColorType.TRUE_COLOUR_ALPHA,
            PNGCompressionType.DEFLATE_INFLATE,
            PNGFilterType.ADAPTIVE,
            PNGInterlaceType.NONE
        )
    ),
    (
        join(root_path, 'static/cat-png'),
        PNGDescriptor(
            960, 603, 8,
            PNGColorType.TRUE_COLOUR_ALPHA,
            PNGCompressionType.DEFLATE_INFLATE,
            PNGFilterType.ADAPTIVE,
            PNGInterlaceType.NONE
        )
    ),
)

GIF_IMAGES = (
    (
        join(root_path, 'static/spongebob.gif'),
        GIFDescriptor(
            500, 334, '89a',
            0, 8, True, 7, True
        )
    ),
    (
        join(root_path, 'static/spongebob-gif'),
        GIFDescriptor(
            500, 334, '89a',
            0, 8, True, 7, True
        )
    ),
    (
        join(root_path, 'static/happy_dog.gif'),
        GIFDescriptor(
            370, 370, '89a',
            0, 8, True, 7, True
        )
    ),
    (
        join(root_path, 'static/happy_dog-gif'),
        GIFDescriptor(
            370, 370, '89a',
            0, 8, True, 7, True
        )
    ),
)

IMAGES = (*PNG_IMAGES, *GIF_IMAGES)


UNSUPPORTED_IMAGES = (
    join(root_path, 'static/homer.svg'),
)
