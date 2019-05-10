import os

import pytest

from openapi.spec.ext.spec import BundledSpec


def get_path(path):
    return os.path.join('tests/fixtures', path)


def get_expected_path(path):
    return get_path(path).replace('openapi', 'expected_openapi')


@pytest.mark.parametrize('path', [
    'simple/openapi.yaml',
    'indirect/openapi.yaml',
], ids=[
    'simple',
    'indirect',
])
def test_bundle_openapi_yaml(path):
    with BundledSpec(get_path(path)) as spec:
        spec.resolve()
        spec.bundle()

    with BundledSpec(get_expected_path(path)) as expected:
        pass

    assert expected.data == spec.data
