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
    height: dp(45)
    #width: _label.texture_size[0] + dp(16)
    width: dp(45)
    padding: (dp(8), 0)
    theme_text_color: 'Custom'
    text_color: root.theme_cls.primary_color
    MDLabel:
        id: _label
        size: dp(45), dp(45)
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
    size: [dp(328), dp(484)] if self.theme_cls.device_orientation == 'portrait'\
        else [dp(512), dp(354)]
    pos_hint: {'center_x': .5, 'center_y': .5}
    canvas:
        Color:
            rgb: app.theme_cls.primary_color
        Rectangle:
            size: [dp(328), dp(96)] if self.theme_cls.device_orientation == 'portrait'\
                else [dp(168), dp(354)]
            pos: [root.pos[0], root.pos[1] + root.height-dp(96)] if self.theme_cls.device_orientation == 'portrait'\
                else [root.pos[0], root.pos[1] + root.height-dp(354)]  #]
        Color:
            rgb: app.theme_cls.bg_normal
        Rectangle:
            size: [dp(328), dp(484)-dp(96)] if self.theme_cls.device_orientation == 'portrait'\
                else [dp(344), dp(354)]
            pos: [root.pos[0], root.pos[1] + root.height-dp(96)-(dp(484)-dp(96))]\
                if self.theme_cls.device_orientation == 'portrait' else [root.pos[0]+dp(168), root.pos[1]]  #+dp(334)

    GridLayout:
        id: main_layout
        cols: 7
        size: (dp(250), dp(45*8))
        size_hint: (None, None)
        pos: (dp(200), dp(50))
        pos_hint: {'center_x': .4, 'center_y': .35} if root.theme_cls.device_orientation == 'portrait'\
            else {'center_x': .6, 'center_y': .4}

    MDLabel:
        id: label_combined
        font_style: "Display2"
        size_hint: (None, None)
        size: [root.width, dp(30)] if root.theme_cls.device_orientation == 'portrait'\
            else [dp(168), dp(30)]
        pos: [root.pos[0]+dp(15), root.pos[1] + root.height - dp(75)] \
            if root.theme_cls.device_orientation == 'portrait' \
            else [root.pos[0]+dp(3), root.pos[1] + root.height - dp(110)]
        valign: "middle"
        text_size: [root.width, None] if root.theme_cls.device_orientation == 'portrait'\
            else [dp(149), None]

    MDLabel:
        id: label_year
        font_style: "Title"
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos[0]+dp(15), root.pos[1] + root.height - dp(30) - dp(10)
        valign: "middle"

    MDLabel:
        id: label_current_month
        font_style: "Body2"
        text: "September 2016"
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos
        theme_text_color: 'Primary'
        pos_hint: {'center_x': 0.5, 'center_y': 0.75} if self.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.655, 'center_y': 0.93}
        valign: "middle"
        halign: "center"

    MDIconButton:
        icon: 'arrow-left'
        pos_hint: {'center_x': 0.09, 'center_y': 0.75} if root.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.4, 'center_y': 0.93}
        on_release: root.prev_month()

    MDIconButton:
        icon: 'arrow-right'
        pos_hint: {'center_x': 0.91, 'center_y': 0.75} if root.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.925, 'center_y': 0.93}
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
    width = NumericProperty(dp(45))
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
        self.size = dp(45), dp(45)
        self.width = dp(45)
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
        self.size = dp(45), dp(45)
        self.width = dp(45)
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
        self.day = None
        self.month = None
        self.year = None
        self.selected_month = None
        self.selected_year = None
        self.all_rows = []
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
        if not self.day:
            self.set_date(date.today())
        self.ids.label_combined.text = "%s, %s %s" % \
            (str(datetime.date(self.year, self.month, self.day).strftime("%A")[:3]),
             calendar.month_abbr[self.month],
             str(self.day))
        self.ids.label_year.text = str(self.year)
        self.selector = CalendarSelector(self)
        self.generate_array(year=self.year,
                            month=self.month,
                            lookout=self.selector.get_lookout())

    def get_touch(self, instance):
        self.selector.move(instance)
        self.selector.update()
        self.ids.label_combined.text = "%s, %s %s" % \
            (str(datetime.date(self.year, self.month, int(instance.text)).strftime("%A")[:3]),
             calendar.month_abbr[self.month],
             str(instance.text))
        self.ids.label_year.text = str(self.year)
        self.selected_month = self.month
        self.selected_year = self.year
        self.day = instance.text

    def next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.ids.label_current_month.text = "%s %s" % (calendar.month_name[self.month], self.year)
        self.selector.update()
        self.update_array(year=self.year,
                          month=self.month)

    def prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.ids.label_current_month.text = "%s %s" % (calendar.month_name[self.month], self.year)
        self.selector.update()
        self.update_array(year=self.year,
                          month=self.month)

    def add_label(self, text=""):
        return MDLabel(text=text,
                       size=(dp(45), dp(45)),
                       size_hint=(None, None),
                       halign='center',
                       theme_text_color='Primary')

    def add_button(self, lookout, i, disabled=False):
        date_button = DateButton(self,
                                 text=str(i[0]),
                                 size_hint=(None, None),
                                 disabled=disabled)
        date_button.bind(on_press=self.get_touch)
        if lookout:
            if str(lookout) == str(i[0]):
                self.selector.receive_lookout(date_button)
        return date_button

    def generate_array(self, year, month, lookout):
        current_row = []
        label = self.add_label
        button = self.add_button
        for y in range(7):
            for x in range(7):
                current_row.append(button(i=("", ""), disabled=True, lookout=lookout))
            last_row = []
            for item in current_row:
                last_row.append(item)
            self.all_rows.append(last_row)
            del current_row[:]
        self.all_rows[0][0] = label(text=calendar.day_abbr[5][0])
        self.all_rows[0][1] = label(text=calendar.day_abbr[6][0])
        count = 2
        for i in self.cal.iterweekdays():
            if calendar.day_abbr[i][0] not in [calendar.day_abbr[5][0], calendar.day_abbr[6][0]]:
                self.all_rows[0][count] = label(text=calendar.day_abbr[i][0])
                count += 1

        month_start_col = date(year, month, 1).weekday()
        if month_start_col == 5:
            month_start_col = -2
        elif month_start_col == 6:
            month_start_col = -1
        count = 0
        row = 1
        for i in range(-2, month_start_col):
            self.all_rows[row][count] = button(i=("", ""), disabled=True, lookout=lookout)
            count += 1
        for i in self.cal.itermonthdays2(year, month):
            if i[0] == 0 and row < 3:
                self.all_rows[row][count] = button(i=("", ""), disabled=True, lookout=lookout)
            elif i[0] == 0 and row > 3:
                self.all_rows[row][count] = button(i=("", ""), disabled=True, lookout=lookout)
            else:
                self.all_rows[row][count] = button(i=i, lookout=lookout)
                count += 1
                if count == 7:
                    count = 0
                    row += 1
        for row in self.all_rows:
            for item in row:
                if item:
                    self.layout.add_widget(item)

    def update_array(self, year, month):
        for row in self.all_rows:
            for item in row:
                if item:
                    if str(item.__class__.__name__) == "DateButton":
                        item.disabled = True
                        item.text = ""
        month_start_col = date(year, month, 1).weekday()
        if month_start_col == 5:
            month_start_col = -2
        elif month_start_col == 6:
            month_start_col = -1
        count = 0
        for i in range(-2, month_start_col):
            self.all_rows[1][count].text = ""
            self.all_rows[1][count].disabled = True
            count += 1
        row = 1
        for i in self.cal.itermonthdays2(year, month):
            if self.all_rows[row][count] is not None:
                if i[0] == 0 and row < 3:
                    self.all_rows[row][count].text = ""
                    self.all_rows[row][count].disabled = True
                    if count == 7:
                        count = 0
                        row += 1
                elif i[0] == 0 and row > 3:
                    self.all_rows[row][count].text = ""
                    self.all_rows[row][count].disabled = True
                    count += 1
                    if count == 7:
                        count = 0
                        row += 1
                else:
                    self.all_rows[row][count].text = str(i[0])
                    self.all_rows[row][count].disabled = False
                    if month == date.today().month and year == date.today().year:
                        if str(i[0]) == str(date.today().day):
                            self.all_rows[row][count].theme_text_color = 'Custom'
                            self.all_rows[row][count].text_color = self.theme_cls.primary_color
                        else:
                            self.all_rows[row][count].theme_text_color = 'Primary'
                    else:
                        self.all_rows[row][count].theme_text_color = 'Primary'
                    count += 1
                    if count == 7:
                        count = 0
                        row += 1
