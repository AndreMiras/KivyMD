# -*- coding: utf-8 -*-
import os
from ast import literal_eval
from kivy import Logger
from kivy.config import Config
__version_info__ = (0, 1, 3)
__version__ = '0.1.3'

path = os.path.dirname(__file__)
fonts_path = os.path.join(path, "fonts/")
images_path = os.path.join(path, 'images/')

Logger.info("KivyMD: KivyMD version: {}".format(__version__))

LIST_FONT_STYLE = {
    'Body1': ['Roboto', False, 14, 13],
    'Body2': ['Roboto', True, 14, 13],
    'Caption': ['Roboto', False, 12, None],
    'Subhead': ['Roboto', False, 16, 15],
    'Title': ['Roboto', True, 20, None],
    'Headline': ['Roboto', False, 24, None],
    'Display1': ['Roboto', False, 34, None],
    'Display2': ['Roboto', False, 45, None],
    'Display3': ['Roboto', False, 56, None],
    'Display4': ['RobotoLight', False, 112, None],
    'Button': ['Roboto', True, 14, None],
    'Icon': ['Icons', False, 24, None]
}
LIST_FONT_STYLE.update(literal_eval(Config.getdefault('myapp', 'list_fonts', {})))

LIST_FONT_NAME = list(LIST_FONT_STYLE.keys())

DEFAULT_FONT_STYLE = Config.getdefault('myapp', 'default_font_style', 'Body1')
