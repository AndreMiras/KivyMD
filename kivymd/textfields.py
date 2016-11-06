# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, \
    ListProperty, BooleanProperty, OptionProperty
from kivy.metrics import sp, dp
from kivy.animation import Animation
from kivymd.label import MDLabel
from kivymd.theming import ThemableBehavior
from kivy.clock import Clock

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
            rgba: self._current_line_color
        Rectangle:
            size: self._line_width, dp(2)
            pos: self.center_x - (self._line_width / 2), self.y + dp(8)
        Color:
            rgba: self._current_error_color
        Rectangle:
            texture: self._msg_lbl.texture
            size: self._msg_lbl.texture_size
            pos: self.x, self.y - dp(8)
        Color:
            rgba: self._current_right_lbl_color
        Rectangle:
            texture: self._right_msg_lbl.texture
            size: self._right_msg_lbl.texture_size
            pos: self.width-self._right_msg_lbl.texture_size[0]+dp(45), self.y - dp(8)
        Color:
            rgba: (self._current_line_color if self.focus and not self.cursor_blink \
            else (0, 0, 0, 0))
        Rectangle:
            pos: [int(x) for x in self.cursor_pos]
            size: 1, -self.line_height
        Color:
            #rgba: self._hint_txt_color if not self.text and not self.focus\
            #else (self.line_color_focus if not self.text or self.focus\
            #else self.line_color_normal)
            rgba: self._current_hint_text_color
        Rectangle:
            texture: self._hint_lbl.texture
            size: self._hint_lbl.texture_size
            pos: self.x, self.y + self._hint_y
        Color:
            rgba: self.disabled_foreground_color if self.disabled else \
            (self.hint_text_color if not self.text and not self.focus else \
            self.foreground_color)

    font_name:    'Roboto'
    foreground_color: app.theme_cls.text_color
    font_size:    sp(16)
    bold:        False
    padding:    0, dp(16), 0, dp(10)
    multiline:    False
    size_hint_y: None
    height: dp(48)
''')


class FixedHintTextInput(TextInput):
    hint_text = StringProperty('')

    def on__hint_text(self, instance, value):
        pass

    def _refresh_hint_text(self):
        pass


class SingleLineTextField(ThemableBehavior, FixedHintTextInput):
    line_color_normal = ListProperty()
    line_color_focus = ListProperty()
    error_color = ListProperty()
    error = BooleanProperty(False)
    text_len_error = BooleanProperty(False)
    message = StringProperty("This field is required")
    message_mode = OptionProperty("none", options=["none", "on_error", "persistent", "on_focus"])
    max_text_length = NumericProperty(None)
    required = BooleanProperty(False)
    _hint_txt_color = ListProperty()
    _hint_lbl = ObjectProperty()
    _hint_lbl_font_size = NumericProperty(sp(16))
    _hint_y = NumericProperty(dp(10))
    _error_label = ObjectProperty()
    _line_width = NumericProperty(0)
    _hint_txt = StringProperty('')
    _current_line_color = line_color_focus
    _current_error_color = ListProperty([0.0, 0.0, 0.0, 0.0])
    _current_hint_text_color = _hint_txt_color
    _current_right_lbl_color = ListProperty([0.0, 0.0, 0.0, 0.0])

    def __init__(self, **kwargs):
        Clock.schedule_interval(self._update_color, 5)
        self._msg_lbl = MDLabel(font_style='Caption',
                                halign='left',
                                valign='middle',
                                text=self.message)

        self._right_msg_lbl = MDLabel(font_style='Caption',
                                      halign='right',
                                      valign='middle',
                                      text="")

        self._hint_lbl = MDLabel(font_style='Subhead',
                                 halign='left',
                                 valign='middle')
        super(SingleLineTextField, self).__init__(**kwargs)
        self.line_color_normal = self.theme_cls.divider_color
        self.line_color_focus = list(self.theme_cls.primary_color)
        self.base_line_color_focus = list(self.theme_cls.primary_color)
        self.error_color = self.theme_cls.error_color

        self._hint_txt_color = self.theme_cls.disabled_hint_text_color
        self.cursor_color = self.theme_cls.primary_color
        self.bind(message=self._set_msg,
                  hint_text=self._set_hint,
                  _hint_lbl_font_size=self._hint_lbl.setter('font_size'),
                  message_mode=self._set_message_mode,
                  max_text_length=self._set_max_text_length,
                  text=self.on_text)
        self.has_had_text = False

    def _update_color(self, *args):
        self.line_color_normal = self.theme_cls.divider_color
        self.base_line_color_focus = list(self.theme_cls.primary_color)
        if not self.focus and not self.error and not self.text_len_error:
            self.line_color_focus = self.theme_cls.primary_color
            Animation(duration=.2, _current_hint_text_color=self.theme_cls.disabled_hint_text_color).start(self)
            if self.message_mode == "persistent":
                Animation(duration=.1, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
        if self.focus and not self.error and not self.text_len_error:
            self.cursor_color = self.theme_cls.primary_color

    def on_width(self, instance, width):
        if self.focus and instance is not None or self.error and instance is not None or self.text_len_error and instance is not None:
            self._line_width = width
        self._msg_lbl.width = self.width
        self._right_msg_lbl.width = self.width
        self._hint_lbl.width = self.width

    def on_focus(self, *args):
        Animation.cancel_all(self, '_line_width', '_hint_y',
                             '_hint_lbl_font_size')
        if self.max_text_length is None:
            max_text_length = 9999999999999
        else:
            max_text_length = self.max_text_length
        if len(self.text) > max_text_length or (True if self.required and len(self.text) == 0 and self.has_had_text else False):
            self.text_len_error = True
        if self.error or (True if self.max_text_length is not None and len(self.text) > self.max_text_length else False):
            has_error = True
        else:
            if self.required and len(self.text) == 0 and self.has_had_text:
                has_error = True
            else:
                has_error = False

        if self.focus:
            self.has_had_text = True
            Animation.cancel_all(self, '_line_width', '_hint_y',
                                 '_hint_lbl_font_size')
            if len(self.text) == 0:
                Animation(_hint_y=dp(34),
                          _hint_lbl_font_size=sp(12), duration=.2,
                          t='out_quad').start(self)
            Animation(_line_width=self.width, duration=.2, t='out_quad').start(self)
            if has_error:
                Animation(duration=.2, _current_hint_text_color=self.error_color, _current_right_lbl_color=self.error_color,
                          _current_line_color=self.error_color).start(self)
                if self.message_mode == "on_error" and (self.error or self.text_len_error):
                    Animation(duration=.2, _current_error_color=self.error_color).start(self)
                elif self.message_mode == "on_error" and not self.error and not self.text_len_error:
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)
                elif self.message_mode == "persistent":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
                elif self.message_mode == "on_focus":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
            else:
                Animation(duration=.2, _current_hint_text_color=self.line_color_focus,
                          _current_right_lbl_color=self._hint_txt_color).start(self)
                if self.message_mode == "on_error":
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)
                if self.message_mode == "persistent":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
                elif self.message_mode == "on_focus":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
        else:
            if len(self.text) == 0:
                Animation(_hint_y=dp(10),
                          _hint_lbl_font_size=sp(16), duration=.2,
                          t='out_quad').start(self)
            if has_error:
                Animation(duration=.2, _current_line_color=self.error_color,
                          _current_hint_text_color=self.error_color,
                          _current_right_lbl_color=self.error_color).start(self)
                if self.message_mode == "on_error" and (self.error or self.text_len_error):
                    Animation(duration=.2, _current_error_color=self.error_color).start(self)
                elif self.message_mode == "on_error" and not self.error and not self.text_len_error:
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)
                elif self.message_mode == "persistent":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
                elif self.message_mode == "on_focus":
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)
            else:
                Animation(duration=.2, _current_line_color=self.base_line_color_focus,
                          _current_hint_text_color=self.theme_cls.disabled_hint_text_color,
                          _current_right_lbl_color=(0, 0, 0, 0)).start(self)
                if self.message_mode == "on_error":
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)
                elif self.message_mode == "persistent":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
                elif self.message_mode == "on_focus":
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)

                Animation(_line_width=0, duration=.2, t='out_quad').start(self)

    def on_text(self, instance, text):
        if len(text) > 0:
            self.has_had_text = True
        if self.max_text_length is not None:
            self._right_msg_lbl.text = "{}/{}".format(len(text), self.max_text_length)
            max_text_length = self.max_text_length
        else:
            max_text_length = 9999999999999
        if len(text) > max_text_length or (True if self.required and len(text) == 0 and self.has_had_text else False):
            self.text_len_error = True
        else:
            self.text_len_error = False
        if self.error or self.text_len_error:
            if self.focus:
                Animation(duration=.2, _current_hint_text_color=self.error_color,
                          _current_line_color=self.error_color).start(self)
                if self.message_mode == "on_error" and (self.error or self.text_len_error):
                    Animation(duration=.2, _current_error_color=self.error_color).start(self)
                if self.text_len_error:
                    Animation(duration=.2, _current_right_lbl_color=self.error_color).start(self)
        else:
            if self.focus:
                Animation(duration=.2, _current_right_lbl_color=self.theme_cls.disabled_hint_text_color).start(self)
                Animation(duration=.2, _current_hint_text_color=self.base_line_color_focus,
                          _current_line_color=self.base_line_color_focus).start(self)
                if self.message_mode == "on_error":
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)

    def on_text_validate(self):
        self.has_had_text = True
        if self.max_text_length is None:
            max_text_length = 9999999999999
        else:
            max_text_length = self.max_text_length
        if len(self.text) > max_text_length or (True if self.required and len(self.text) == 0 and self.has_had_text else False):
            self.text_len_error = True

    def _set_hint(self, instance, text):
        self._hint_lbl.text = text

    def _set_msg(self, instance, text):
        self._msg_lbl.text = text
        self.message = text

    def _set_message_mode(self, instance, text):
        self.message_mode = text
        if self.message_mode == "persistent":
            Animation(duration=.1, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)

    def _set_max_text_length(self, instance, length):
        self.max_text_length = length
        self._right_msg_lbl.text = "{}/{}".format(len(self.text), length)
