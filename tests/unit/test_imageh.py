#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `imageh` package."""
from imageh import imageh

import pytest

from tests.conftest import IMAGES, UNSUPPORTED_IMAGES


@pytest.mark.parametrize('filename, format_, width, height', IMAGES)
def test_parse_reads_correctly(filename, format_, width, height):
    descriptor = imageh.parse(filename)
    assert format_ == descriptor.format
    assert width == descriptor.width
    assert height == descriptor.height


@pytest.mark.parametrize('filename, format_, width, height', IMAGES)
def test_parse_fd_reads_correctly(filename, format_, width, height):
    with open(filename, 'rb') as fd:
        descriptor = imageh.parse_fd(fd)
        assert format_ == descriptor.format
        assert width == descriptor.width
        assert height == descriptor.height


@pytest.mark.parametrize('filename', UNSUPPORTED_IMAGES)
def test_parse_raises_exception_with_unsupported_file_formats(filename):
    with pytest.raises(imageh.UnsupportedFormatError):
        imageh.parse(filename)
