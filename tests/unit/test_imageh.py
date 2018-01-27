#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `imageh` package."""
from imageh import imageh

import pytest

from tests.conftest import images, unsupported_images, FOLDER_PATH, HTTP_PATH


@pytest.mark.parametrize('filename, descriptor', images(FOLDER_PATH))
def test_analyze_generate_correct_descriptor(filename, descriptor):
    generated_descriptor = imageh.analyze(filename)
    assert descriptor == generated_descriptor


@pytest.mark.parametrize('filename, descriptor', images(HTTP_PATH))
def test_analyze_generate_correct_descriptor_remote(filename, descriptor):
    generated_descriptor = imageh.analyze(filename)
    assert descriptor == generated_descriptor


@pytest.mark.parametrize('filename, descriptor', images(FOLDER_PATH))
def test_parse_fd_reads_correctly(filename, descriptor):
    with open(filename, 'rb') as fd:
        generated_descriptor = imageh.parse_fd(fd)

        # These properties are not evaluated by parse_fd -> mocked
        generated_descriptor.extension = descriptor.extension
        generated_descriptor.aspect_ratio = descriptor.aspect_ratio
        generated_descriptor.filename = descriptor.filename
        generated_descriptor.url = descriptor.url

        assert descriptor == generated_descriptor


@pytest.mark.parametrize('filename', unsupported_images(FOLDER_PATH))
def test_parse_raises_exception_with_unsupported_file_formats(filename):
    with pytest.raises(imageh.UnknownFormatError):
        imageh.analyze(filename)


@pytest.mark.parametrize('filename', unsupported_images(HTTP_PATH))
def test_parse_raises_exception_with_unsupported_file_formats_remote(filename):
    with pytest.raises(imageh.UnknownFormatError):
        imageh.analyze(filename)


@pytest.mark.parametrize('uri', [
    '/not/existent/path',
    'http://yolo'
])
def test_analyze_not_existent_path_or_file_raises_correct_error(uri):
    with pytest.raises(FileNotFoundError):
        imageh.analyze(uri)
