# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.properties import ListProperty
from kivy.metrics import sp, dp
from kivymd.theming import ThemableBehavior
from kivy.uix.floatlayout import FloatLayout
from kivymd.elevationbehavior import ElevationBehavior

Builder.load_string("""
<MDDatePicker>:
    size_hint: (None, None)
    size: dp(260), dp(30)+dp(150)+dp(290)
    pos_hint: {'center_x': .5, 'center_y': .5}
    canvas:
        Color:
            rgb: app.theme_cls.primary_dark
        Rectangle:
            size: dp(260), dp(30)
            pos: root.pos[0], root.pos[1] + root.height-dp(30)
        Color:
            rgb: app.theme_cls.primary_color
        Rectangle:
            size: dp(260), dp(150)
            pos: root.pos[0], root.pos[1] + root.height-(dp(30)+dp(150))
        Color:
            rgb: app.theme_cls.bg_normal
        Rectangle:
            size: dp(260), dp(290)
            pos: root.pos[0], root.pos[1] + root.height-(dp(30)+dp(150)+dp(290))

    MDFlatButton:
        pos: root.pos[0]+root.size[0]-dp(72)*2, root.pos[1] + dp(10)
        text: "Cancel"
        on_release: root.close_cancel()
    MDFlatButton:
        pos: root.pos[0]+root.size[0]-dp(72), root.pos[1] + dp(10)
        text: "OK"
        on_release: root.close_ok()

""")


class MDDatePicker(FloatLayout, ThemableBehavior, ElevationBehavior, ModalView):
    background_color = ListProperty([0, 0, 0, 0])

    def __init__(self, **kwargs):
        super(MDDatePicker, self).__init__(**kwargs)

    def close_cancel(self):
        self.dismiss()

    def close_ok(self):
        self.dismiss()


if __name__ == "__main__":
    from kivy.app import App
    from kivymd.theming import ThemeManager

    class DatePickerApp(App):
        theme_cls = ThemeManager()
        theme_cls.primary_palette = "Teal"
        # theme_cls.primary_hue = "200"

        def open_dialog(self):
            self.date_picker = MDDatePicker()
            # self.date_picker.bind(time=self.get_time)
            '''try:
                self.time_picker.set_time(self.last_time)
            except TypeError:
                pass'''
            self.date_picker.open()

        def build(self):
            main_widget = Builder.load_string("""
#:import MDRaisedButton kivymd.button.MDRaisedButton
FloatLayout:
    MDRaisedButton:
        size_hint: None, None
        size: 3 * dp(48), dp(48)
        # center_x: self.parent.center_x
        text: 'Switch theme color (debug)'
        on_release: app.theme_cls.primary_palette = 'Teal' if app.theme_cls.primary_palette != 'Teal' else 'DeepOrange'
        opposite_colors: True
    MDRaisedButton:
        size_hint: None, None
        size: 3 * dp(48), dp(48)
        center_x: self.parent.center_x
        text: 'Switch theme style'
        on_release: app.theme_cls.theme_style = 'Dark' if app.theme_cls.theme_style != 'Dark' else 'Light'
        opposite_colors: True
    MDRaisedButton:
        size_hint: None, None
        pos_hint: {'center_x': .5, 'center_y': .5}
        size: 3 * dp(48), dp(48)
        center_x: self.parent.center_x
        text: 'Open date picker'
        on_release: app.open_dialog()
        opposite_colors: True
""")
            return main_widget

    DatePickerApp().run()

