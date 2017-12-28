#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `imageh` package."""
from imageh import imageh

import pytest

from tests.conftest import IMAGES, UNSUPPORTED_IMAGES


@pytest.mark.parametrize('filename, descriptor', IMAGES)
def test_parse_generate_correct_descriptor(filename, descriptor):
    generated_descriptor = imageh.parse(filename)
    assert descriptor == generated_descriptor


@pytest.mark.parametrize('filename, descriptor', IMAGES)
def test_parse_fd_reads_correctly(filename, descriptor):
    with open(filename, 'rb') as fd:
        generated_descriptor = imageh.parse_fd(fd)
        assert descriptor == generated_descriptor


@pytest.mark.parametrize('filename', UNSUPPORTED_IMAGES)
def test_parse_raises_exception_with_unsupported_file_formats(filename):
    with pytest.raises(imageh.UnsupportedFormatError):
        imageh.parse(filename)
