import os
import re
from setuptools import setup

from kivymd.version import __version__


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup_params = {
    'name': 'kivy_garden.kivymd',
    'version': __version__,
    'description': "Set of widgets for Kivy inspired by Google's Material Design",
    'long_description': read('README.md'),
    'long_description_content_type': 'text/markdown',
    'author': 'Andrés Rodríguez',
    'author_email': 'andres.rodriguez@lithersoft.com',
    'url': 'https://github.com/AndreMiras/KivyMD',
    'packages': ['kivymd'],
    'package_data': {
        'kivymd': [
            'images/*.png',
            'images/*.jpg',
            'images/*.atlas',
            'vendor/*.py',
            'fonts/*.ttf', 'vendor/circleLayout/*.py',
            'vendor/circularTimePicker/*.py',
            'vendor/navigationdrawer/*.py',
        ]
    },
    'install_requires': ['kivy'],
}


def run_setup():
    setup(**setup_params)


# makes sure the setup doesn't run at import time
if __name__ == '__main__':
    run_setup()
