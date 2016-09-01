# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.metrics import dp
from kivymd.label import MDLabel
from kivymd.theming import ThemableBehavior
from kivy.uix.floatlayout import FloatLayout
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
from kivy.core.window import Window

Builder.load_string("""
#:import GridLayout kivy.uix.gridlayout.GridLayout
<CalendarButton>
    canvas:
        Color:
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
        size: self.size
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
<MDDatePicker>:
    size_hint: (None, None)
    size: [dp(280), dp(30)+dp(130)+dp(300)] if self.theme_cls.device_orientation == 'portrait'\
        else [dp(30) + dp(130) + dp(325), dp(300)]
    pos_hint: {'center_x': .5, 'center_y': .5}
    canvas:
        Color:
            rgb: app.theme_cls.primary_dark
        Rectangle:
            size: [dp(280), dp(30)] if self.theme_cls.device_orientation == 'portrait'\
                else [dp(200), dp(30)]
            pos: root.pos[0], root.pos[1] + root.height-dp(30)
        Color:
            rgb: app.theme_cls.primary_color
        Rectangle:
            size: [dp(280), dp(130)] if self.theme_cls.device_orientation == 'portrait' else\
                [dp(200), root.height - dp(30)]
            pos: [root.pos[0], root.pos[1] + root.height-(dp(30)+dp(130))] \
                if self.theme_cls.device_orientation == 'portrait' else [root.pos[0], root.pos[1]]
        Color:
            rgb: app.theme_cls.bg_normal
        Rectangle:
            size: [dp(280), dp(300)] if self.theme_cls.device_orientation == 'portrait'\
                else [root.width-dp(200), root.height]
            pos: [root.pos[0], root.pos[1] + root.height-(dp(30)+dp(130)+dp(300))]\
                if self.theme_cls.device_orientation == 'portrait' else [root.pos[0]+dp(200), root.pos[1]]

    GridLayout:
        id: main_layout
        cols: 7
        size: (dp(250), dp(35*8))
        size_hint: (None, None)
        pos: (dp(200), dp(50))
        pos_hint: {'center_x': .5075, 'center_y': .275} if root.theme_cls.device_orientation == 'portrait'\
            else {'center_x': .71, 'center_y': .4}

    MDLabel:
        id: label_weekday
        font_style: "Title"
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos
        pos_hint: {'center_x': 0.5, 'center_y': 0.97} if self.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.22, 'center_y': 0.95}
        valign: "middle"
        halign: "center"

    MDLabel:
        id: label_date
        font_style: "Display3"
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos
        pos_hint: {'center_x': 0.5, 'center_y': 0.85} if self.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.22, 'center_y': 0.6}
        valign: "middle"
        halign: "center"

    MDLabel:
        id: label_short_month
        font_style: "Headline"
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos
        pos_hint: {'center_x': 0.5, 'center_y': 0.75} if self.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.22, 'center_y': 0.45}
        valign: "middle"
        halign: "center"

    MDLabel:
        id: label_year
        font_style: "Headline"
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos
        pos_hint: {'center_x': 0.5, 'center_y': 0.7} if self.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.22, 'center_y': 0.375}
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
        pos_hint: {'center_x': 0.5, 'center_y': 0.61} if self.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.71, 'center_y': 0.925}
        valign: "middle"
        halign: "center"

    MDIconButton:
        icon: 'arrow-left'
        pos_hint: {'center_x': 0.125, 'center_y': 0.61} if root.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.475, 'center_y': 0.925}
        on_release: root.prev_month()

    MDIconButton:
        icon: 'arrow-right'
        pos_hint: {'center_x': 0.875, 'center_y': 0.61} if root.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.94, 'center_y': 0.925}
        on_release: root.next_month()

    MDFlatButton:
        pos: root.pos[0]+root.size[0]-dp(72)*2, root.pos[1] + dp(10)
        text: "Cancel"
        on_release: root.close_cancel()
    MDFlatButton:
        pos: root.pos[0]+root.size[0]-dp(72), root.pos[1] + dp(10)
        text: "OK"
        on_release: root.close_ok()
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
        self.width = dp(35)
        self.size = dp(35), dp(35)
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
        super(CalendarButton, self).__init__(disabled=True)
        self.size = dp(35), dp(35)
        self.width = dp(35)
        self.parent_class = cls
        self.selected_month = cls.month
        self.selected_year = cls.year
        self.selected_day = cls.day
        self.current_button = None
        self.theme_color_with_alpha = self.theme_cls.primary_color
        self.theme_color_with_alpha[3] = 0.4
        Window.bind(on_resize=self.move_resize)

    def add(self):
        try:
            self.parent_class.add_widget(self)
        except WidgetException:
            pass

    def update(self):
        if self.selected_month == self.parent_class.month and self.selected_year == self.parent_class.year:
            try:
                self.move(self.current_button)
                # cls.add_widget(self)
                Clock.schedule_once(lambda x: self.add())
            except WidgetException:
                pass
        else:
            try:
                self.parent_class.remove_widget(self)
            except WidgetException:
                pass

    def move_resize(self, window, width, height, do_again=True):
        self.pos = self.current_button.pos
        # self.size = self.current_button.size
        if do_again:
            Clock.schedule_once(lambda x: self.move_resize(window=window,
                                                           width=width,
                                                           height=height,
                                                           do_again=False), 0.01)

    def move(self, inst=None):
        if not inst:
            pass
        else:
            self.current_button = inst
            self.selected_month = self.parent_class.month
            self.selected_year = self.parent_class.year
            self.pos = inst.pos
            # self.size = inst.size
            Clock.schedule_once(lambda x: self.move_resize(window=None,
                                                           width=None,
                                                           height=None,
                                                           do_again=True), 0.001)

    def receive_lookout(self, inst):
        self.current_button = inst
        self.move(self.current_button)
        self.update()

    def get_lookout(self):
        return self.selected_day


class MDDatePicker(FloatLayout,
                   ThemableBehavior,
                   ElevationBehavior,
                   ModalView):
    date = ObjectProperty()

    def __init__(self, **kwargs):
        super(MDDatePicker, self).__init__(**kwargs)
        self.date = None
        self.layout = self.ids.main_layout
        self.cal = calendar.Calendar()
        self.selector = None

    def close_cancel(self):
        self.dismiss()

    def close_ok(self):
        self.date = datetime.datetime.strptime("".join([str(self.day),
                                                        str(self.selected_month),
                                                        str(self.selected_year)]), "%d%m%Y").date()
        self.dismiss()

    def set_date_str(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year
        self.selected_month = self.month
        self.selected_year = self.year

    def set_date(self, the_date):
        try:
            self.day = the_date.day
            self.month = the_date.month
            self.year = the_date.year
            self.selected_month = self.month
            self.selected_year = self.year
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
            self.set_date(date.today())
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
        self.selector.move(instance)
        self.selector.update()
        self.ids.label_weekday.text = str(datetime.date(self.year, self.month, int(instance.text)).strftime("%A"))
        self.ids.label_date.text = str(instance.text)
        self.ids.label_short_month.text = calendar.month_abbr[self.month].upper()
        self.ids.label_year.text = str(self.year)
        self.selected_month = self.month
        self.selected_year = self.year
        self.day = instance.text

    def next_month(self):
        look = None
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.ids.label_current_month.text = "%s %s" % (calendar.month_name[self.month], self.year)
        self.selector.update()
        if self.selector.selected_month == self.month and self.selector.selected_year == self.year:
            look = self.day
        self.layout.clear_widgets()
        self.generate_calendar(year=self.year,
                               month=self.month,
                               lookout=look)

    def prev_month(self):
        look = None
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.ids.label_current_month.text = "%s %s" % (calendar.month_name[self.month], self.year)
        self.selector.update()
        if self.selector.selected_month == self.month and self.selector.selected_year == self.year:
            look = self.day
        self.layout.clear_widgets()
        self.generate_calendar(year=self.year,
                               month=self.month,
                               lookout=look)

    def add_button(self, lookout, i):
        date_button = DateButton(self,
                                 text=str(i[0]),
                                 size_hint=(None, None))

        date_button.bind(on_press=self.get_touch)
        self.layout.add_widget(date_button)
        if lookout:
            if str(lookout) == str(i[0]):
                self.selector.receive_lookout(date_button)

    def add_label(self, text=""):
        self.layout.add_widget(MDLabel(size=(dp(35), dp(35)),
                               size_hint=(None, None),
                               text=text,
                               halign='center',
                               theme_text_color='Primary'))

    def generate_calendar(self, year, month, lookout=None):
        add_label = self.add_label
        add_button = self.add_button
        add_label(text=calendar.day_abbr[5][0])
        add_label(text=calendar.day_abbr[6][0])
        for i in self.cal.iterweekdays():
            if calendar.day_abbr[i][0] not in [calendar.day_abbr[5][0], calendar.day_abbr[6][0]]:
                add_label(text=calendar.day_abbr[i][0])

        month_start_col = date(year, month, 1).weekday()
        if month_start_col == 5:
            month_start_col = -2
        elif month_start_col == 6:
            month_start_col = -1
        for i in range(-2, month_start_col):
            add_label()
        for i in self.cal.itermonthdays2(year, month):
            if i[0] != 0:
                add_button(lookout=lookout, i=i)
