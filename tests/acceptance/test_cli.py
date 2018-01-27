import json

import pexpect
import pytest

from tests.conftest import images, unsupported_images, FOLDER_PATH, HTTP_PATH


@pytest.mark.parametrize('uri, descriptor', images(FOLDER_PATH))
def test_cli_supported_image_file(uri, descriptor):
    child = pexpect.spawn('imageh %s' % uri)
    child.expect(descriptor.json())


@pytest.mark.parametrize('uri, descriptor', images(HTTP_PATH))
def test_cli_supported_image_remote(uri, descriptor):
    child = pexpect.spawn('imageh %s' % uri)
    child.expect(descriptor.json())


@pytest.mark.parametrize('uri', unsupported_images(FOLDER_PATH))
def test_cli_unsupported_image_file(uri):
    error_msg = {
        'error': 'unsupported image format or not valid image URI'
    }
    child = pexpect.spawn('imageh %s' % uri)
    child.expect(json.dumps(error_msg))


@pytest.mark.parametrize('uri', unsupported_images(HTTP_PATH))
def test_cli_unsupported_image_remote(uri):
    error_msg = {
        'error': 'unsupported image format or not valid image URI'
    }
    child = pexpect.spawn('imageh %s' % uri)
    child.expect(json.dumps(error_msg))


@pytest.mark.parametrize('uri', ['/not/existent/path'])
def test_cli_not_existent_path_or_file(uri):
    error_msg = {
        'error': 'file %s not found' % uri
    }
    child = pexpect.spawn('imageh %s' % uri)
    child.expect(json.dumps(error_msg))
