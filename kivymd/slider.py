# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty,AliasProperty, BooleanProperty
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
from kivymd.theming import ThemableBehavior
from kivy.uix.slider import Slider


Builder.load_string('''
#:import Thumb kivymd.selectioncontrols.Thumb

<MDSlider>:
    id: slider
    canvas:
        Clear
        Color:
            rgba: self._track_color_disabled if self.disabled else (self._track_color_active if self.active else self._track_color_normal)
        Rectangle:
            size:    (self.width - self.padding*2, dp(4)) if self.orientation == 'horizontal' else (dp(4),self.height - self.padding*2) 
            pos:   (self.x + self.padding, self.center_y - dp(4)) if self.orientation == 'horizontal' else (self.center_x - dp(4),self.y + self.padding)
        Color:
            rgba: self.thumb_color_down if not self.disabled else self._track_color_disabled
        Rectangle:
            size:     (self.value_pos[0]-10, sp(4)) if slider.orientation == 'horizontal' else (sp(4), self.value_pos[1]-10)
            pos:    (self.x + self.padding, self.center_y - dp(4)) if self.orientation == 'horizontal' else (self.center_x - dp(4),self.y + self.padding)

    Thumb:
        id:          thumb
        size_hint:   None, None
        size:        (dp(12), dp(12)) if root.disabled else ((dp(24), dp(24)) if root.active else (dp(16),dp(16)))
        pos:         (slider.value_pos[0] - dp(8), slider.center_y - sp(thumb.height/2+2)) if slider.orientation == 'horizontal' else (slider.center_x - sp(thumb.width/2+2), slider.value_pos[1]-dp(8))
        color:       root._track_color_disabled if root.disabled else root.thumb_color_down
        elevation:    4 if root.active else 2

''')

class MDSlider(ThemableBehavior, Slider):
    active = BooleanProperty(False)

    _thumb_color = ListProperty(get_color_from_hex(colors['Grey']['50']))
    
    def _get_thumb_color(self):
        return self._thumb_color

    def _set_thumb_color(self, color, alpha=None):
        if len(color) == 2:
            self._thumb_color = get_color_from_hex(colors[color[0]][color[1]])
            if alpha:
                self._thumb_color[3] = alpha
        elif len(color) == 4:
            self._thumb_color = color

    thumb_color = AliasProperty(_get_thumb_color, _set_thumb_color,
                                bind=['_thumb_color'])

    _thumb_color_down = ListProperty([1, 1, 1, 1])

    def _get_thumb_color_down(self):
        return self._thumb_color_down

    def _set_thumb_color_down(self, color, alpha=None):
        if len(color) == 2:
            self._thumb_color_down = get_color_from_hex(
                colors[color[0]][color[1]])
            if alpha:
                self._thumb_color_down[3] = alpha
            else:
                self._thumb_color_down[3] = 1
        elif len(color) == 4:
            self._thumb_color_down = color

    thumb_color_down = AliasProperty(_get_thumb_color_down,
                                     _set_thumb_color_down,
                                     bind=['_thumb_color_down'])

    _thumb_color_disabled = ListProperty(
        get_color_from_hex(colors['Grey']['400']))

    def _get_thumb_color_disabled(self):
        return self._thumb_color_disabled

    def _set_thumb_color_disabled(self, color, alpha=None):
        if len(color) == 2:
            self._thumb_color_disabled = get_color_from_hex(
                colors[color[0]][color[1]])
            if alpha:
                self._thumb_color_disabled[3] = alpha
        elif len(color) == 4:
            self._thumb_color_disabled = color

    thumb_color_down = AliasProperty(_get_thumb_color_disabled,
                                     _set_thumb_color_disabled,
                                     bind=['_thumb_color_disabled'])

    _track_color_active = ListProperty()
    _track_color_normal = ListProperty()
    _track_color_disabled = ListProperty()
    _thumb_pos = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super(MDSlider, self).__init__(**kwargs)
        self.theme_cls.bind(theme_style=self._set_colors,
                            primary_color=self._set_colors,
                            primary_palette=self._set_colors)
        self._set_colors()
        
    def _set_colors(self, *args):
        if self.theme_cls.theme_style == 'Dark':
            self._track_color_normal = get_color_from_hex('FFFFFF')
            self._track_color_normal[3] = .3
            self._track_color_active = self._track_color_normal
            self._track_color_disabled = self._track_color_normal
            self.thumb_color = get_color_from_hex(colors['Grey']['400'])
            self.thumb_color_down = get_color_from_hex(
                colors[self.theme_cls.primary_palette]['200'])
            self.thumb_color_disabled = get_color_from_hex(
                colors['Grey']['800'])
        else:
            self._track_color_normal = get_color_from_hex('000000')
            self._track_color_normal[3] = 0.26
            self._track_color_active = get_color_from_hex('000000')
            self._track_color_active[3] = 0.38 
            self._track_color_disabled = get_color_from_hex('000000')
            self._track_color_disabled[3] = 0.26
            self.thumb_color_down = self.theme_cls.primary_color
            
    def on_touch_down(self, touch):
        if super(MDSlider, self).on_touch_down(touch):
            self.active = True
            
    def on_touch_up(self,touch):
        if super(MDSlider, self).on_touch_up(touch):
            self.active = False
#             thumb = self.ids['thumb']
#             if thumb.collide_point(*touch.pos):
#                 thumb.on_touch_down(touch)
#                 thumb.on_touch_up(touch)
            

if __name__ == '__main__':
    from kivy.app import App
    from kivymd.theming import ThemeManager
    
    class SliderApp(App):
        theme_cls = ThemeManager()
        def build(self):
            return Builder.load_string("""
BoxLayout:
    orientation:'vertical'
    BoxLayout:
        size_hint_y:None
        height: '48dp'
        Label:
            text:"Toggle disabled"
            color: [0,0,0,1]
        CheckBox:
            id: cb
            on_press: slider.disabled = not slider.disabled
    BoxLayout:
        size_hint_y:None
        height: '48dp'
        Label:
            text:"Toggle active"
            color: [0,0,0,1]
        CheckBox:
            id: cb
            on_press: slider.active = not slider.active

    MDSlider:
        id:slider
        min:0
        max:100
        value: 40
    
    MDSlider:
        id:slider2
        orientation:"vertical"
        min:0
        max:100
        value: 40
        
""")
            

    SliderApp().run()