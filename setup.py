import re
from os import path
from setuptools import setup

version_py = open('openapi/spec/ext/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", version_py))
desc = 'Extended tools for openapi spec'

cur_dir = path.abspath(path.dirname(__file__))
with open(path.join(cur_dir, 'README.md')) as f:
    long_description = f.read()

setup(
    name='openapi-ext-tools',
    version=metadata['version'],
    description=desc,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
    url='https://github.com/t2y/openapi-ext-tools',
    license='Apache License 2.0',
    author='Tetsuya Morimoto',
    author_email='tetsuya.morimoto@gmail.com',
    zip_safe=False,
    platforms='any',
    packages=['openapi'],
    namespace_packages=['openapi'],
    include_package_data=True,
    install_requires=[
        'PyYAML',
        'openapi-spec-validator>=0.5.1',
    ],
    tests_require=[
        'tox', 'pytest', 'pytest-pycodestyle', 'pytest-flakes',
    ],
    entry_points = {
        'console_scripts': [
            'openapi-spec-cli=openapi.spec.ext.cli.main:main',
        ],
    },
)
