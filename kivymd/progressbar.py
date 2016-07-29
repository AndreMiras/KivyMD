# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.properties import ListProperty, OptionProperty
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
from kivymd.theming import ThemableBehavior
from kivy.uix.progressbar import ProgressBar


Builder.load_string('''
<MDProgressBar>:
    canvas:
        Clear
        Color:
            rgba:  self.theme_cls.divider_color
        Rectangle:
            size:    (self.width , dp(4)) if self.orientation == 'horizontal' else (dp(4),self.height) 
            pos:   (self.x, self.center_y - dp(4)) if self.orientation == 'horizontal' else (self.center_x - dp(4),self.y)
        
            
        Color:
            rgba:  self.theme_cls.primary_color
        Rectangle:
            size:     (self.width*self.value_normalized, sp(4)) if self.orientation == 'horizontal' else (sp(4), self.height*self.value_normalized)
            pos:    (self.x, self.center_y - dp(4)) if self.orientation == 'horizontal' else (self.center_x - dp(4),self.y)
        
''')

class MDProgressBar(ThemableBehavior, ProgressBar):
    orientation = OptionProperty('horizontal',options=['horizontal','vertical'])
            
    
if __name__ == '__main__':
    from kivy.app import App
    from kivymd.theming import ThemeManager
    
    class ProgressBarApp(App):
        theme_cls = ThemeManager()
        def build(self):
            return Builder.load_string("""#:import MDSlider kivymd.slider.MDSlider
BoxLayout:
    orientation:'vertical'

    MDSlider:
        id:slider
        min:0
        max:100
        value: 40
        
    MDProgressBar:
        value: slider.value
    MDProgressBar:
        orientation:"vertical"
        value: slider.value
        
""")
            

    ProgressBarApp().run()