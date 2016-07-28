# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.properties import BoundedNumericProperty, ReferenceListProperty, ListProperty,BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.elevationbehavior import ElevationBehavior
from kivymd.theming import ThemableBehavior
from kivy.metrics import dp

Builder.load_string('''
<MDCard>
    canvas:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [self.border_radius]
        Color:
            rgba: self.theme_cls.divider_color
            a: self.border_color_a
        Line:
            rounded_rectangle: (self.pos[0],self.pos[1],self.size[0],self.size[1],self.border_radius) 
    background_color: self.theme_cls.bg_light
''')


class MDCard(ThemableBehavior, ElevationBehavior, BoxLayout):
    r = BoundedNumericProperty(1., min=0., max=1.)
    g = BoundedNumericProperty(1., min=0., max=1.)
    b = BoundedNumericProperty(1., min=0., max=1.)
    a = BoundedNumericProperty(0., min=0., max=1.)
    
    border_radius = BoundedNumericProperty(dp(3),min=0)
    border_color_a = BoundedNumericProperty(0, min=0., max=1.)
    background_color = ReferenceListProperty(r, g, b, a)
