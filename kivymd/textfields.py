# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    ListProperty, BooleanProperty
from kivy.metrics import sp, dp
from kivy.animation import Animation
from kivymd.label import MDLabel
from theming import ThemableBehavior

Builder.load_string('''
<SingleLineTextField>:
    canvas.before:
        Clear
        Color:
            rgba: self.line_color_normal
        Line:
            id: "the_line"
            points: self.x, self.y + dp(8), self.x + self.width, self.y + dp(8)
            width: 1
            dash_length: dp(3)
            dash_offset: 2 if self.disabled else 0
        Color:
            rgba: self._current_color_1
        Rectangle:
            size: self._line_width, dp(2)
            pos: self.center_x - (self._line_width / 2), self.y + dp(8)
        Color:
            rgba: self._current_color_2
        Rectangle:
            texture: self._msg_lbl.texture
            size: self._msg_lbl.texture_size
            pos: self.x, self.y - dp(8)
        Color:
            rgba: (self._current_color_1 if self.focus and not self.cursor_blink \
            else (0, 0, 0, 0))
        Rectangle:
            pos: [int(x) for x in self.cursor_pos]
            size: 1, -self.line_height
        Color:
            #rgba: self._hint_txt_color if not self.text and not self.focus\
            #else (self.line_color_focus if not self.text or self.focus\
            #else self.line_color_normal)
            rgba: self._current_color_3
        Rectangle:
            texture: self._hint_lbl.texture
            size: self._hint_lbl.texture_size
            pos: self.x, self.y + self._hint_y
        Color:
            rgba: self.disabled_foreground_color if self.disabled else \
            (self.hint_text_color if not self.text and not self.focus else \
            self.foreground_color)

    font_name:    'Roboto'
    font_size:    sp(16)
    bold:        False
    padding:    0, dp(16), 0, dp(10)
    multiline:    False
    size_hint_y: None
    height: dp(48)
''')


class SingleLineTextField(ThemableBehavior, TextInput):
    line_color_normal = ListProperty()
    line_color_focus = ListProperty()
    error_color = ListProperty()
    error = BooleanProperty(False)
    message = StringProperty("")
    message_mode = StringProperty("none")
    mode = message_mode

    _hint_txt_color = ListProperty()
    _hint_lbl = ObjectProperty()
    _hint_lbl_font_size = NumericProperty(sp(16))
    _hint_y = NumericProperty(dp(10))
    _error_label = ObjectProperty()
    _line_width = NumericProperty(0)
    _hint_txt = StringProperty('')
    _current_color_1 = line_color_focus
    _current_color_2 = ListProperty([0.0, 0.0, 0.0, 0.0])
    _current_color_3 = _hint_txt_color

    def __init__(self, **kwargs):
        self._msg_lbl = MDLabel(font_style='Caption',
                                theme_text_color='Error',
                                halign='left',
                                valign='middle',
                                text=self.message)

        self._hint_lbl = MDLabel(font_style='Subhead',
                                 halign='left',
                                 valign='middle')
        super(SingleLineTextField, self).__init__(**kwargs)
        self.line_color_normal = self.theme_cls.divider_color
        self.line_color_focus = list(self.theme_cls.primary_color)
        self.bob = list(self.theme_cls.primary_color)
        self.error_color = self.theme_cls.error_color

        self._hint_txt_color = self.theme_cls.disabled_hint_text_color
        self.hint_text_color = (1, 1, 1, 0)
        self.cursor_color = self.theme_cls.primary_color
        self.bind(message=self._set_msg,
                  hint_text=self._set_hint,
                  _hint_lbl_font_size=self._hint_lbl.setter('font_size'),
                  message_mode=self._set_mode)

    def on_hint_text_color(self, instance, color):
        self._hint_txt_color = self.theme_cls.disabled_hint_text_color
        self.hint_text_color = (1, 1, 1, 0)

    def on_width(self, instance, width):
        self.anim = Animation(_line_width=width, duration=.2, t='out_quad')
        self._msg_lbl.width = self.width
        self._hint_lbl.width = self.width

    def on_pos(self, *args):
        self.hint_anim_in = Animation(_hint_y=dp(34),
                                      _hint_lbl_font_size=sp(12), duration=.2,
                                      t='out_quad')
        self.hint_anim_out = Animation(_hint_y=dp(10),
                                       _hint_lbl_font_size=sp(16), duration=.2,
                                       t='out_quad')

    def on_focus(self, *args):
        if self.focus:
            Animation.cancel_all(self, '_line_width', '_hint_y',
                                 '_hint_lbl_font_size')
            if len(self.text) == 0:
                self.hint_anim_in.start(self)
            if self.error:
                if self.mode == "on_error":
                    Animation(duration=.2, _current_color_2=self.error_color).start(self)
                    Animation(duration=.2, _current_color_3=self.error_color).start(self)
                elif self.mode == "persistent":
                    Animation(duration=.2, _current_color_2=self.theme_cls.disabled_hint_text_color).start(self)
                    Animation(duration=.2, _current_color_3=self.error_color).start(self)
                elif self.mode == "on_focus":
                    Animation(duration=.2, _current_color_2=self.theme_cls.disabled_hint_text_color).start(self)
                    Animation(duration=.2, _current_color_3=self.error_color).start(self)
                else:
                    Animation(duration=.2, _current_color_3=self.error_color).start(self)
            elif not self.error:
                self.on_width(None, self.width)
                self.anim.start(self)
                if self.mode == "on_error":
                    Animation(duration=.2, _current_color_2=(0, 0, 0, 0)).start(self)
                    Animation(duration=.2, _current_color_3=self.line_color_focus).start(self)
                if self.mode == "persistent":
                    Animation(duration=.2, _current_color_2=self.theme_cls.disabled_hint_text_color).start(self)
                    Animation(duration=.2, _current_color_3=self.line_color_focus).start(self)
                elif self.mode == "on_focus":
                    Animation(duration=.2, _current_color_2=self.theme_cls.disabled_hint_text_color).start(self)
                    Animation(duration=.2, _current_color_3=self.line_color_focus).start(self)
                else:
                    Animation(duration=.2, _current_color_3=self.line_color_focus).start(self)
        else:
            Animation.cancel_all(self, '_line_width', '_hint_y',
                                 '_hint_lbl_font_size')
            if len(self.text) == 0:
                self.hint_anim_out.start(self)
            if not self.error:
                self.line_color_focus = self.bob
                Animation(duration=.2, _current_color_1=self.line_color_focus).start(self)
                Animation(duration=.2, _current_color_3=self.theme_cls.disabled_hint_text_color).start(self)
                if self.mode == "on_error":
                    Animation(duration=.2, _current_color_2=(0, 0, 0, 0)).start(self)
                elif self.mode == "persistent":
                    Animation(duration=.2, _current_color_2=self.theme_cls.disabled_hint_text_color).start(self)
                elif self.mode == "on_focus":
                    Animation(duration=.2, _current_color_2=(0, 0, 0, 0)).start(self)

                self.on_width(None, 0)
                self.anim.start(self)
            elif self.error:
                Animation(duration=.2, _current_color_1=self.error_color).start(self)
                Animation(duration=.2, _current_color_3=self.error_color).start(self)
                if self.mode == "on_error":
                    Animation(duration=.2, _current_color_2=self.error_color).start(self)
                elif self.mode == "persistent":
                    Animation(duration=.2, _current_color_2=self.theme_cls.disabled_hint_text_color).start(self)
                elif self.mode == "on_focus":
                    Animation(duration=.2, _current_color_2=(0, 0, 0, 0)).start(self)

    def _set_hint(self, instance, text):
        self._hint_lbl.text = text

    def _set_msg(self, instance, text):
        self._msg_lbl.text = text
        self.message = text

    def _set_mode(self, instance, text):
        self.mode = text
        print(self.mode)
        if self.mode == "persistent":
            Animation(duration=.1, _current_color_2=self.theme_cls.disabled_hint_text_color).start(self)

if __name__ == "__main__":
    from kivy.app import App
    from kivymd.theming import ThemeManager
    from kivy.core.window import Window

    class TextApp(App):
        Window.size = (900, 140)
        theme_cls = ThemeManager()

        def set_error_message(self, *args):
            if len(self.root.ids.text_field_error.text) == 0:
                self.root.ids.text_field_error.error = True
            else:
                self.root.ids.text_field_error.error = False

        def build(self):
            main_widget = Builder.load_string("""
BoxLayout:
    size_hint_y: 1
    padding: dp(48)
    BoxLayout:
        SingleLineTextField:
            id: text_field
            size_hint: 0.8, None
            height: dp(48)
            hint_text: "No helper text"
    BoxLayout:
        SingleLineTextField:
            id: text_field
            size_hint: 0.8, None
            height: dp(48)
            hint_text: "on_focus"
            message: "Some text is required"
            message_mode: "on_focus"
    BoxLayout:
        SingleLineTextField:
            id: text_field
            size_hint: 0.8, None
            height: dp(48)
            hint_text: "persistent"
            message: "Text is always here"
            message_mode: "persistent"
    BoxLayout:
        SingleLineTextField:
            id: text_field_error
            size_hint: 0.8, None
            height: dp(48)
            hint_text: "on_error (no text)"
            message: "You must out something here"
            message_mode: "on_error"
""")
            main_widget.ids.text_field_error.bind(
                on_text_validate=self.set_error_message,
                on_focus=self.set_error_message)
            return main_widget

    TextApp().run()
