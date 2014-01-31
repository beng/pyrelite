import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

config = {
    'description': 'A lightweight toolkit for generating SQL strings from simple relational expressions.',
    'author': 'Justin Poliey',
    'url': 'https://github.com/beng/pyrelite',
    'author_email': 'justin.d.poliey@gmail.com',
    'version': '1.0.0',
    'packages': [
        'pyrelite',
        'tests'
    ],
    'name': 'pyrelite',
    'long_description': read('README.rst')
}

setup(**config)
