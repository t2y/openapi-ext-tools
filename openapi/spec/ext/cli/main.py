import argparse
import logging
import os
import pathlib
import sys
from pprint import pprint

from openapi_spec_validator import validate_spec_url
from openapi_spec_validator.exceptions import OpenAPISpecValidatorError

from ..utils.log import log
from ..spec import BundledSpec


def validate(path):
    try:
        abspath = os.path.abspath(path)
        validate_spec_url(pathlib.Path(abspath).as_uri())
    except OpenAPISpecValidatorError as e:
        pprint(e)
        sys.exit(1)
    except Exception as e:
        pprint(e)
        sys.exit(2)
    else:
        log.info('validating bundled spec: OK')


def parse_argument(argv=None):
    parser = argparse.ArgumentParser()
    parser.set_defaults(
        spec_path=None,
        bundled_spec_path='bundled_openapi.yaml',
        verbose=False,
    )

    parser.add_argument(
        '--spec-path', required=True,
        help='set path to openapi spec file'
    )
    parser.add_argument(
        '--bundled-spec-path',
        help='set path to bundled spec file'
    )

    parser.add_argument(
        '--verbose', action='store_true',
        help='set verbose mode'
    )

    args = parser.parse_args(argv)
    if not os.path.exists(args.spec_path):
        parser.error(f'{args.spec_path} is not exists')

    return args


def main(argv=None):
    args = parse_argument(argv)
    if args.verbose:
        log.setLevel(logging.DEBUG)

    with BundledSpec(args.spec_path) as spec:
        spec.resolve()
        spec.bundle()
        spec.write(args.bundled_spec_path)

    log.info(f'wrote bundled spec file to "{args.bundled_spec_path}"')
    validate(args.bundled_spec_path)


if __name__ == '__main__':
    main()
