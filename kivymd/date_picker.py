# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivymd.label import MDLabel
from kivymd.theming import ThemableBehavior
from kivy.uix.floatlayout import FloatLayout
from kivymd.elevationbehavior import ElevationBehavior
import calendar
from datetime import date
import datetime
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, \
    BooleanProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivymd.ripplebehavior import CircularRippleBehavior

"""
Builder.load_string(
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
)


class CalendarButton(ThemableBehavior,
                     CircularRippleBehavior,
                     ButtonBehavior,
                     BackgroundColorBehavior,
                     AnchorLayout):
    width = NumericProperty(dp(45))
    text_color = ListProperty()
    text = StringProperty('')
    theme_text_color = OptionProperty(None,
                                      allownone=True,
                                      options=['Primary', 'Secondary', 'Hint',
                                               'Error', 'Custom'])
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
                                         colors[self.theme_cls.theme_style][
                                             'FlatButtonDown']))
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
                                                           do_again=False),
                                0.01)

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
                                                           do_again=True),
                                0.001)

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
                                                        str(
                                                            self.selected_month),
                                                        str(
                                                            self.selected_year)]),
                                               "%d%m%Y").date()
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
            raise TypeError(
                "<DatePicker>.set_date requires a datetime.date, if you would prefer you can pass in <day>,"
                " <month>, <year> separately as strings with <DatePicker>.set_date_str")

    def open(self, *args):
        super(MDDatePicker, self).open(*args)
        if not self.day:
            self.set_date(date.today())
        self.ids.label_combined.text = "%s, %s %s" % \
                                       (str(datetime.date(self.year, self.month,
                                                          self.day).strftime(
                                           "%A")[:3]),
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
                                       (str(datetime.date(self.year, self.month,
                                                          int(
                                                              instance.text)).strftime(
                                           "%A")[:3]),
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
        self.ids.label_current_month.text = "%s %s" % (
            calendar.month_name[self.month], self.year)
        self.selector.update()
        self.update_array(year=self.year,
                          month=self.month)

    def prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.ids.label_current_month.text = "%s %s" % (
            calendar.month_name[self.month], self.year)
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
                current_row.append(
                    button(i=("", ""), disabled=True, lookout=lookout))
            last_row = []
            for item in current_row:
                last_row.append(item)
            self.all_rows.append(last_row)
            del current_row[:]
        count = 0
        for i in self.cal.iterweekdays():
            self.all_rows[0][count] = label(
                text=calendar.day_abbr[i][0].upper())
            count += 1

        month_start_col = date(year, month, 1).weekday()
        count = 0
        row = 1
        for i in range(0, month_start_col):
            self.all_rows[row][count] = button(i=("", ""), disabled=True,
                                               lookout=lookout)
            count += 1
        for i in self.cal.itermonthdays2(year, month):
            if i[0] == 0 and row < 3:
                self.all_rows[row][count] = button(i=("", ""), disabled=True,
                                                   lookout=lookout)
            elif i[0] == 0 and row > 3:
                self.all_rows[row][count] = button(i=("", ""), disabled=True,
                                                   lookout=lookout)
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
        count = 0
        for i in range(0, month_start_col):
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
                            self.all_rows[row][
                                count].theme_text_color = 'Custom'
                            self.all_rows[row][
                                count].text_color = self.theme_cls.primary_color
                        else:
                            self.all_rows[row][
                                count].theme_text_color = 'Primary'
                    else:
                        self.all_rows[row][count].theme_text_color = 'Primary'
                    count += 1
                    if count == 7:
                        count = 0
                        row += 1
"""

Builder.load_string("""
#:import calendar calendar
<MDDatePicker>
    cal_layout: cal_layout

    size_hint: (None, None)
    size: [dp(328), dp(484)] if self.theme_cls.device_orientation == 'portrait'\
        else [dp(512), dp(304)]
    pos_hint: {'center_x': .5, 'center_y': .5}
    canvas:
        Color:
            rgb: app.theme_cls.primary_color
        Rectangle:
            size: [dp(328), dp(96)] if self.theme_cls.device_orientation == 'portrait'\
                else [dp(168), dp(304)]
            pos: [root.pos[0], root.pos[1] + root.height-dp(96)] if self.theme_cls.device_orientation == 'portrait'\
                else [root.pos[0], root.pos[1] + root.height-dp(304)]
        Color:
            rgb: app.theme_cls.bg_normal
        Rectangle:
            size: [dp(328), dp(484)-dp(96)] if self.theme_cls.device_orientation == 'portrait'\
                else [dp(344), dp(304)]
            pos: [root.pos[0], root.pos[1] + root.height-dp(96)-(dp(484)-dp(96))]\
                if self.theme_cls.device_orientation == 'portrait' else [root.pos[0]+dp(168), root.pos[1]]  #+dp(334)
    MDLabel:
        id: label_full_date
        font_style: 'Display1'
        text_color: 1, 1, 1, 1
        theme_text_color: 'Custom'
        size_hint: (None, None)
        size: [root.width, dp(30)] if root.theme_cls.device_orientation == 'portrait'\
            else [dp(168), dp(30)]
        pos: [root.pos[0]+dp(23), root.pos[1] + root.height - dp(74)] \
            if root.theme_cls.device_orientation == 'portrait' \
            else [root.pos[0]+dp(3), root.pos[1] + dp(214)]
        line_height: 0.84
        valign: 'middle'
        text_size: [root.width, None] if root.theme_cls.device_orientation == 'portrait'\
            else [dp(149), None]
        bold: True
        text: root.fmt_lbl_date(root.sel_year, root.sel_month, root.sel_day, root.theme_cls.device_orientation)
    MDLabel:
        id: label_year
        font_style: 'Subhead'
        text_color: 1, 1, 1, 1
        theme_text_color: 'Custom'
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: (root.pos[0]+dp(23), root.pos[1]+root.height-dp(40)) if root.theme_cls.device_orientation == 'portrait'\
            else (root.pos[0]+dp(16), root.pos[1]+root.height-dp(41))
        valign: 'middle'
        text: str(root.sel_year)
    GridLayout:
        id: cal_layout
        cols: 7
        size: (dp(44*7), dp(40*7)) if root.theme_cls.device_orientation == 'portrait'\
            else (dp(46*7), dp(32*7))
        col_default_width: dp(42) if root.theme_cls.device_orientation == 'portrait'\
            else dp(39)
        size_hint: (None, None)
        padding: (dp(2), 0) if root.theme_cls.device_orientation == 'portrait'\
            else (dp(7), 0)
        spacing: (dp(2), 0) if root.theme_cls.device_orientation == 'portrait'\
            else (dp(7), 0)
        pos: (root.pos[0]+dp(10), root.pos[1]+dp(60)) if root.theme_cls.device_orientation == 'portrait'\
            else (root.pos[0]+dp(168)+dp(11), root.pos[1]+dp(48))
    MDLabel:
        id: label_month_selector
        font_style: 'Body2'
        text: calendar.month_name[root.sel_month].capitalize() + ' ' + str(root.sel_year)
        size_hint: (None, None)
        size: root.width, dp(30)
        pos: root.pos
        theme_text_color: 'Primary'
        pos_hint: {'center_x': 0.5, 'center_y': 0.75} if self.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.67, 'center_y': 0.915}
        valign: "middle"
        halign: "center"
    MDIconButton:
        icon: 'chevron-left'
        theme_text_color: 'Secondary'
        pos_hint: {'center_x': 0.09, 'center_y': 0.745} if root.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.39, 'center_y': 0.925}
        on_release: root.change_month('prev')
    MDIconButton:
        icon: 'chevron-right'
        theme_text_color: 'Secondary'
        pos_hint: {'center_x': 0.92, 'center_y': 0.745} if root.theme_cls.device_orientation == 'portrait'\
            else {'center_x': 0.94, 'center_y': 0.925}
        on_release: root.change_month('next')
    MDFlatButton:
        pos: root.pos[0]+root.size[0]-dp(72)*2, root.pos[1] + dp(7)
        text: "Cancel"
        on_release: root.dismiss()
    MDFlatButton:
        pos: root.pos[0]+root.size[0]-dp(72), root.pos[1] + dp(7)
        text: "OK"
        on_release: root.ok_click()

<DayButton>
    size_hint: None, None
    size: (dp(40), dp(40)) if root.theme_cls.device_orientation == 'portrait'\
        else (dp(32), dp(32))
    MDLabel:
        font_style: 'Caption'
        theme_text_color: 'Custom' if root.is_today and not root.is_selected else 'Primary'
        text_color: root.theme_cls.primary_color
        opposite_colors: root.is_selected
        size_hint_x: None
        valign: 'middle'
        halign: 'center'
        text: root.text

<WeekdayLabel>
    font_style: 'Caption'
    theme_text_color: 'Secondary'
    size: (dp(40), dp(40)) if root.theme_cls.device_orientation == 'portrait'\
        else (dp(32), dp(32))
    size_hint: None, None
    text_size: self.size
    valign: 'middle' if root.theme_cls.device_orientation == 'portrait' else 'bottom'
    halign: 'center'
""")


class DayButton(ThemableBehavior, CircularRippleBehavior, ButtonBehavior,
                AnchorLayout):
    text = StringProperty()
    owner = ObjectProperty()
    is_today = BooleanProperty(False)
    is_selected = BooleanProperty(False)

    def on_release(self):
        self.owner.set_selected_widget(self)


class WeekdayLabel(MDLabel):
    pass


class MDDatePicker(FloatLayout, ThemableBehavior, ElevationBehavior,
                   ModalView):
    _sel_day_widget = ObjectProperty()
    cal_list = None
    cal_layout = ObjectProperty()
    sel_year = NumericProperty()
    sel_month = NumericProperty()
    sel_day = NumericProperty()
    today = date.today()
    callback = ObjectProperty()

    def __init__(self, callback, year=None, month=None, day=None,
                 firstweekday=0,
                 **kwargs):
        self.callback = callback
        self.cal = calendar.Calendar(firstweekday)
        self.sel_year = year if year else self.today.year
        self.sel_month = month if month else self.today.month
        self.sel_day = day if day else self.today.day
        super(MDDatePicker, self).__init__(**kwargs)
        self.generate_cal_widgets()
        self.update_cal_matrix(self.sel_year, self.sel_month,
                               sel_date=date(self.sel_year, self.sel_month,
                                             self.sel_day))

    def ok_click(self):
        self.callback(date(self.sel_year, self.sel_month, self.sel_day))
        self.dismiss()

    def fmt_lbl_date(self, year, month, day, orientation):
        d = datetime.date(int(year), int(month), int(day))
        separator = '\n' if orientation == 'landscape' else ' '
        return d.strftime('%a,').capitalize() + separator + d.strftime(
            '%b').capitalize() + ' ' + str(day).lstrip('0')

    def set_selected_widget(self, widget):
        if self._sel_day_widget:
            self._sel_day_widget.is_selected = False
        widget.is_selected = True
        self.sel_day = int(widget.text)
        self._sel_day_widget = widget

    def update_cal_matrix(self, year, month, sel_date=False):
        dates = [x for x in self.cal.itermonthdates(year, month)]
        self.sel_year = year
        self.sel_month = month
        for idx in range(len(self.cal_list)):
            if idx >= len(dates) or dates[idx].month != month:
                self.cal_list[idx].disabled = True
                self.cal_list[idx].text = ''
            else:
                self.cal_list[idx].disabled = False
                self.cal_list[idx].text = str(dates[idx].day)
                if dates[idx] == sel_date:
                    self.set_selected_widget(self.cal_list[idx])
                self.cal_list[idx].is_today = dates[idx] == self.today

    def generate_cal_widgets(self):
        cal_list = []
        for i in calendar.day_abbr:
            self.cal_layout.add_widget(WeekdayLabel(text=i[0].upper()))
        for i in range(6 * 7):  # 6 weeks, 7 days a week
            db = DayButton(owner=self)
            cal_list.append(db)
            self.cal_layout.add_widget(db)
        self.cal_list = cal_list

    def change_month(self, operation):
        op = 1 if operation is 'next' else -1
        sl, sy = self.sel_month, self.sel_year
        m = 12 if sl + op == 0 else 1 if sl + op == 13 else sl + op
        y = sy - 1 if sl + op == 0 else sy + 1 if sl + op == 13 else sy
        self.update_cal_matrix(y, m, sel_date=date(y, m, self.sel_day))
