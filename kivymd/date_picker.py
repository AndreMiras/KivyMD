# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.metrics import dp
from kivymd.label import MDLabel
from kivymd.theming import ThemableBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.elevationbehavior import ElevationBehavior
import calendar
from datetime import date
import datetime
from kivy.properties import StringProperty, ListProperty, NumericProperty, OptionProperty, ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivymd.ripplebehavior import RectangularRippleBehavior
from kivymd.backgroundcolorbehavior import BackgroundColorBehavior
from kivy.animation import Animation
from kivymd.color_definitions import colors
from kivy.utils import get_color_from_hex
from kivy.uix.widget import WidgetException

Builder.load_string("""
<MDDatePicker>:
    size_hint: (None, None)
    size: dp(300), dp(30)+dp(130)+dp(300)
    pos_hint: {'center_x': .5, 'center_y': .5}
    canvas:
        Color:
            rgb: app.theme_cls.primary_dark
        Rectangle:
            size: dp(300), dp(30)
            pos: root.pos[0], root.pos[1] + root.height-dp(30)
        Color:
            rgb: app.theme_cls.primary_color
        Rectangle:
            size: dp(300), dp(130)
            pos: root.pos[0], root.pos[1] + root.height-(dp(30)+dp(130))
        Color:
            rgb: app.theme_cls.bg_normal
        Rectangle:
            size: dp(300), dp(300)
            pos: root.pos[0], root.pos[1] + root.height-(dp(30)+dp(130)+dp(300))

    MDLabel:
        id: label_weekday
        font_style: "Headline"
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos
        pos_hint: {'center_x': 0.5, 'center_y': 0.97}
        valign: "middle"
        halign: "center"

    MDLabel:
        id: label_date
        font_style: "Display3"
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos
        pos_hint: {'center_x': 0.5, 'center_y': 0.85}
        valign: "middle"
        halign: "center"

    MDLabel:
        id: label_short_month
        font_style: "Headline"
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos
        pos_hint: {'center_x': 0.5, 'center_y': 0.75}
        valign: "middle"
        halign: "center"

    MDLabel:
        id: label_year
        font_style: "Headline"
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        valign: "middle"
        halign: "center"

    MDLabel:
        id: label_current_month
        font_style: "Body2"
        text: "September 2016"
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos
        theme_text_color: 'Primary'
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        valign: "middle"
        halign: "center"

    MDIconButton:
        icon: 'arrow-left'
        pos_hint: {'center_x': 0.275, 'center_y': 0.6}
        on_release: root.prev_month()

    MDIconButton:
        icon: 'arrow-right'
        pos_hint: {'center_x': 0.725, 'center_y': 0.6}
        on_release: root.next_month()

    MDFlatButton:
        pos: root.pos[0]+root.size[0]-dp(72)*2, root.pos[1] + dp(10)
        text: "Cancel"
        on_release: root.close_cancel()
    MDFlatButton:
        pos: root.pos[0]+root.size[0]-dp(72), root.pos[1] + dp(10)
        text: "OK"
        on_release: root.close_ok()
<CalendarButton>
    canvas:
        Color:
            #rgba: self.background_color if self.state == 'normal' else self._bg_color_down
            rgba: self._current_button_color
        Rectangle:
            size: self.size
            pos: self.pos
    size_hint: (None, None)
    height: dp(36)
    width: _label.texture_size[0] + dp(16)
    padding: (dp(8), 0)
    theme_text_color: 'Custom'
    text_color: root.theme_cls.primary_color
    MDLabel:
        id: _label
        text: root._text
        font_style: 'Button'
        size_hint_x: None
        text_size: (None, root.height)
        height: self.texture_size[1]
        theme_text_color: root.theme_text_color
        text_color: root.text_color
        valign: 'middle'
        halign: 'center'
        opposite_colors: root.opposite_colors

<CalendarSelector>
    canvas:
        Color:
            rgba: self.theme_color_with_alpha
        Ellipse:
            size: self.size
            pos: self.pos
""")


class CalendarButton(ThemableBehavior,
                     RectangularRippleBehavior,
                     ButtonBehavior,
                     BackgroundColorBehavior,
                     AnchorLayout):
    width = NumericProperty(dp(64),
                            min=dp(64),
                            max=None,
                            errorhandler=lambda x: dp(64))
    text_color = ListProperty()
    text = StringProperty('')
    theme_text_color = OptionProperty(None,
                                      allownone=True,
                                      options=['Primary', 'Secondary', 'Hint', 'Error', 'Custom'])
    text_color = ListProperty(None,
                              allownone=True)

    _text = StringProperty('')
    _bg_color_down = ListProperty([0, 0, 0, 0])
    _current_button_color = ListProperty([0, 0, 0, 0])

    def __init__(self, **kwargs):
        super(CalendarButton, self).__init__(**kwargs)
        self._current_button_color = self.background_color
        '''self._bg_color_down = get_color_from_hex(
            colors[self.theme_cls.theme_style]['FlatButtonDown'])'''

        Clock.schedule_once(lambda x: self.ids._label.bind(
            texture_size=self.update_width_on_label_texture))

    def update_width_on_label_texture(self, instance, value):
        self.ids._label.width = value[0]

    def on_text(self, instance, value):
        self._text = value.upper()

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            return False
        elif not self.collide_point(touch.x, touch.y):
            return False
        elif self in touch.ud:
            return False
        elif self.disabled:
            return False
        else:
            self.fade_bg = Animation(duration=.2,
                                     _current_button_color=get_color_from_hex(
                                        colors[self.theme_cls.theme_style]['FlatButtonDown']))
            self.fade_bg.start(self)
            return super(CalendarButton, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.fade_bg.stop_property(self, '_current_button_color')
            Animation(duration=.05,
                      _current_button_color=self.background_color).start(self)
        return super(CalendarButton, self).on_touch_up(touch)


class DateButton(CalendarButton):
    def __init__(self, cls, **kwargs):
        super(CalendarButton, self).__init__(**kwargs)
        self.width = kwargs['size'][0]
        self.size = kwargs['size']
        self.text = kwargs['text']
        if self.text == str(date.today().day) \
                and cls.month == date.today().month \
                and cls.year == date.today().year:
            pass
        else:
            self.theme_text_color = 'Primary'


class CalendarSelector(CalendarButton):
    theme_color_with_alpha = ListProperty([0.0, 0.0, 0.0, 0.0])

    def __init__(self, cls):
        super(CalendarButton, self).__init__()
        self.selected_month = cls.month
        self.selected_year = cls.year
        self.selected_day = cls.day
        self.current_button = None
        self.disabled = True
        self.theme_color_with_alpha = self.theme_cls.primary_color
        self.theme_color_with_alpha[3] = 0.4

    def update(self, cls):
        if self.selected_month == cls.month and self.selected_year == cls.year:
            try:
                cls.add_widget(self)
                self.move(cls, self.current_button)
            except WidgetException:
                pass
        else:
            try:
                cls.remove_widget(self)
            except WidgetException:
                pass

    def move(self, cls, inst):
        if not inst:
            pass
        else:
            self.current_button = inst
            self.selected_month = cls.month
            self.selected_year = cls.year
            self.pos = inst.pos
            self.size = inst.size

    def receive_lookout(self, inst, cls):
        self.current_button = inst
        self.move(cls, self.current_button)
        self.update(cls)
        # cls.add_widget(self)

    def get_lookout(self):
        return self.selected_day


class MDDatePicker(FloatLayout,
                   ThemableBehavior,
                   ElevationBehavior,
                   ModalView):
    background_color = ListProperty([0, 0, 0, 0])
    date = ObjectProperty()

    def __init__(self, **kwargs):
        super(MDDatePicker, self).__init__(**kwargs)
        self.date = None
        self.layout = None
        self.selector = None

    def close_cancel(self):
        self.dismiss()

    def close_ok(self):
        self.date = datetime.datetime.strptime("".join([str(self.day),
                                                        str(self.month),
                                                        str(self.year)]), "%d%m%Y").date()
        self.dismiss()

    def set_date_str(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def set_date(self, the_date):
        try:
            self.day = the_date.day
            self.month = the_date.month
            self.year = the_date.year
        except AttributeError:
            raise TypeError("<DatePicker>.set_date requires a datetime.date, if you would prefer you can pass in <day>,"
                            " <month>, <year> separately as strings with <DatePicker>.set_date_str")

    def open(self, *args):
        super(MDDatePicker, self).open(*args)
        try:
            self.year
            self.month
            self.day
        except AttributeError:
            self.set_date_str(date.today().day, date.today().month, date.today().year)
        self.ids.label_weekday.text = str(datetime.date(self.year, self.month, self.day).strftime("%A"))
        self.ids.label_date.text = str(self.day)
        self.ids.label_short_month.text = calendar.month_name[self.month][:3].upper()
        self.ids.label_year.text = str(self.year)
        self.ids.label_current_month.text = calendar.month_name[self.month] + " " + str(self.year)
        self.selector = CalendarSelector(self)
        self.generate_calendar(year=self.year,
                               month=self.month,
                               lookout=self.selector.get_lookout())

    def get_touch(self, instance):
        self.selector.move(self, instance)
        self.selector.update(self)
        self.ids.label_weekday.text = str(datetime.date(self.year, self.month, int(instance.text)).strftime("%A"))
        self.ids.label_date.text = str(int(instance.text))
        self.ids.label_short_month.text = calendar.month_abbr[self.month].upper()
        self.ids.label_year.text = str(self.year)
        self.day = instance.text

    def next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.selector.update(self)
        self.remove_widget(self.layout)
        del self.layout
        self.generate_calendar(year=self.year,
                               month=self.month)
        self.ids.label_current_month.text = calendar.month_name[self.month] + " " + str(self.year)

    def prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.selector.update(self)
        self.remove_widget(self.layout)
        del self.layout
        self.generate_calendar(year=self.year,
                               month=self.month)
        self.ids.label_current_month.text = calendar.month_name[self.month] + " " + str(self.year)

    def generate_calendar(self, year, month, lookout=None):
        actual_date = datetime.date(year, month, 1)
        cal = calendar.Calendar()
        self.layout = GridLayout(cols=7, size=(dp(250), dp(35*8)),
                                 size_hint=(None, None),
                                 pos=(dp(200), dp(50)),
                                 pos_hint={'center_x': .5, 'center_y': .275})
        for i in range(0, 2):
            self.layout.add_widget(MDLabel(size=(dp(35), dp(35)),
                                           size_hint=(None, None), text="S",
                                           halign="center",
                                           theme_text_color='Primary'))
        for i in cal.iterweekdays():
            if str(calendar.day_abbr[i][0]) == "S":
                pass
            else:
                self.layout.add_widget(MDLabel(size=(dp(35), dp(35)),
                                               size_hint=(None, None),
                                               text=calendar.day_abbr[i][0],
                                               halign="center",
                                               theme_text_color='Primary'))

        def first_day_of_month(d):
            return date(d.year, d.month, 1)

        month_start_col = first_day_of_month(actual_date).weekday()
        if month_start_col == 5:
            month_start_col = -2
        if month_start_col == 6:
            month_start_col = -1
        for i in range(-2, month_start_col):
            self.layout.add_widget(MDLabel(size=(dp(35), dp(35)),
                                           size_hint=(None, None)))
        for i in cal.itermonthdays2(year, month):
            if str(i[0]) == "0":
                pass
            else:
                date_button = DateButton(self, text=str(i[0]),
                                         size=(dp(35), dp(35)),
                                         size_hint=(None, None),
                                         pos=self.pos)
                date_button.bind(on_press=self.get_touch)
                self.layout.add_widget(date_button)
                if lookout:
                    if str(lookout) == str(i[0]):
                        self.selector.receive_lookout(date_button, self)
                        self.selector.move(cls=self, inst=date_button)
                        self.actual_start_lookout = date_button
                        Clock.schedule_once(lambda x: self.selector.move(cls=self,
                                                                         inst=self.actual_start_lookout),
                                            0.0000001)
        self.add_widget(self.layout)


if __name__ == "__main__":
    from kivy.app import App
    from kivymd.theming import ThemeManager

    class DatePickerApp(App):
        theme_cls = ThemeManager()

        def get_date(self, instance, the_date):
            print(the_date)
            self.last_date = the_date

        def open_dialog(self):
            self.date_picker = MDDatePicker()
            self.day = 19
            self.month = 9
            self.year = 2020
            # self.date_picker.set_date(datetime.datetime.strptime("".join([str(self.day),
            #                                                              str(self.month),
            #                                                              str(self.year)]), "%d%m%Y").date())'''
            # self.date_picker.set_date_str(self.day, self.month, self.year)
            self.date_picker.bind(date=self.get_date)
            try:
                self.date_picker.set_date(self.last_date)
            except AttributeError:
                pass
            self.date_picker.open()

        def build(self):
            main_widget = Builder.load_string("""
#:import MDRaisedButton kivymd.button.MDRaisedButton
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
FloatLayout:
    MDRaisedButton:
        size_hint: None, None
        size: 3 * dp(48), dp(48)
        # center_x: self.parent.center_x
        text: 'Switch theme color (debug)'
        on_release: MDThemePicker().open()
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
