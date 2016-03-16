# coding=utf-8
from kivy.lang import Builder
from kivy.metrics import sp, dp
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, \
    StringProperty
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivymd.label import MDLabel
from kivymd.theming import ThemableBehavior

Builder.load_string("""
<MDPersistentSearch>
    search_input: search_input
    canvas:
        Color:
            rgba: self.theme_cls.bg_darkest
        Rectangle:
            size: self.size
            pos: self.pos
    FloatLayout:
        MDCard:
            id: search_box
            size_hint: None, None
            height: dp(48)
            width: Window.width - dp(8) * 2
            top: Window.height - dp(8)
            x: dp(8)
            orientation: 'horizontal'
            MDIconButton:
                icon: 'arrow-left' if search_input.focus else 'search'
                theme_text_color: 'Secondary'
                on_release: root.dismiss() if search_input.focus else None  # FIXME
            BoxLayout:
                padding: dp(5), dp(4), 0, 0  # FIXME: NOT EXACT METRIC
                SearchTextInput:
                    id: search_input
                    hint_text: "Search"  # TODO: i18n
                    theme_text_color: 'Primary'
            MDIconButton:
                icon: 'mic' if search_input.text == '' else 'close'
                theme_text_color: 'Secondary'
                on_release: root.mic_input() if search_input.focus else \
                    root.clear_input()

<SearchTextInput>
    canvas.before:
        Clear
        Color:
            rgba: (self.cursor_color if self.focus and not self.cursor_blink \
            else (0, 0, 0, 0))
        Rectangle:
            pos: [int(x) for x in self.cursor_pos]
            size: 1, -self.line_height
        Color:
            rgba: self._hint_txt_color if not self.text and not self.focus \
            else ((1, 1, 1, 0) if not self.text or self.focus \
            else (1, 1, 1, 0))
        Rectangle:
            texture: self._hint_lbl.texture
            size: self._hint_lbl.texture_size
            pos: self.x, self.y + self._hint_y
        Color:
            rgba: self.disabled_foreground_color if self.disabled else \
            (self.hint_text_color if not self.text and not self.focus else \
            self.foreground_color)
    font_name: 'Roboto'
    font_size: sp(20)
    multiline: False
    cursor_color: root.theme_cls.secondary_text_color
    foreground_color: root.theme_cls.text_color
    MDLabel:
        id: _hint_lbl
        font_style: 'Caption'
        theme_text_color: 'Hint'
""")


class SearchTextInput(ThemableBehavior, TextInput):
    search_input = ObjectProperty()

    _hint_text = StringProperty()
    _hint_txt_color = ListProperty()
    _hint_lbl = ObjectProperty()
    _hint_lbl_font_size = NumericProperty(sp(16))
    _hint_y = NumericProperty(dp(10))

    def __init__(self, **kwargs):
        self._hint_lbl = MDLabel(font_style='Subhead',
                                 halign='left',
                                 valign='middle')
        super(SearchTextInput, self).__init__(**kwargs)


class MDPersistentSearch(ThemableBehavior, ModalView):
    def clear_input(self):
        self.search_input.text = ""

    def mic_input(self):
        # Not Implemented
        pass
