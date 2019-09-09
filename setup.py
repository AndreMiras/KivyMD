import os
import re
from setuptools import setup

VERSION_FILE = "kivymd/__init__.py"
ver_file_data = open(VERSION_FILE, "rt").read()
ver_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
ver_reg_search = re.search(ver_regex, ver_file_data, re.M)
if ver_reg_search:
    version = ver_reg_search.group(1)
else:
    raise ValueError("Unable to find version string in {}.".format(VERSION_FILE))


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup_params = {
    'name': 'kivymd',
    'version': version,
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
    'requires': ['kivy'],
}


def run_setup():
    setup(**setup_params)


# makes sure the setup doesn't run at import time
if __name__ == '__main__':
    run_setup()
