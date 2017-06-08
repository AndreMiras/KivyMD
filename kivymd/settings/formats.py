# Warning: do not name this module "types"
import datetime
import os

from kivy.compat import text_type
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ObjectProperty, string_types, NumericProperty, StringProperty, BooleanProperty, \
    ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingSpacer
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivymd.date_picker import MDDatePicker

from kivymd.time_picker import MDTimePicker

from kivymd.label import MDLabel
from kivymd.list import TwoLineListItem, IRightBodyTouch, ContainerSupport
from kivymd.selectioncontrols import MDCheckbox


class MDCheckboxRight(MDCheckbox, IRightBodyTouch):
    setting_item = ObjectProperty()

    def on_active(self, instance, value):
        super(MDCheckboxRight, self).on_active(instance, value)
        item = self.setting_item
        item.value = item.values[int(value)]


class KivyMDSettingsItem(TwoLineListItem, ContainerSupport):
    title = StringProperty('<No title set>')
    '''Title of the setting, defaults to '<No title set>'.

    :attr:`title` is a :class:`~kivy.properties.StringProperty` and defaults to
    '<No title set>'.
    '''

    desc = StringProperty(None, allownone=True)
    '''Description of the setting, rendered on the line below the title.

    :attr:`desc` is a :class:`~kivy.properties.StringProperty` and defaults to
    None.
    '''

    disabled = BooleanProperty(False)
    '''Indicate if this setting is disabled. If True, all touches on the
    setting item will be discarded.

    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False.
    '''

    section = StringProperty(None)
    '''Section of the token inside the :class:`~kivy.config.ConfigParser`
    instance.

    :attr:`section` is a :class:`~kivy.properties.StringProperty` and defaults
    to None.
    '''

    key = StringProperty(None)
    '''Key of the token inside the :attr:`section` in the
    :class:`~kivy.config.ConfigParser` instance.

    :attr:`key` is a :class:`~kivy.properties.StringProperty` and defaults to
    None.
    '''

    value = ObjectProperty(None)
    '''Value of the token according to the :class:`~kivy.config.ConfigParser`
    instance. Any change to this value will trigger a
    :meth:`Settings.on_config_change` event.

    :attr:`value` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    panel = ObjectProperty(None)
    '''(internal) Reference to the SettingsPanel for this setting. You don't
    need to use it.

    :attr:`panel` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    content = ObjectProperty(None)
    '''(internal) Reference to the widget that contains the real setting.
    As soon as the content object is set, any further call to add_widget will
    call the content.add_widget. This is automatically set.

    :attr:`content` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    selected_alpha = NumericProperty(0)
    '''(internal) Float value from 0 to 1, used to animate the background when
    the user touches the item.

    :attr:`selected_alpha` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.
    '''

    __events__ = ('on_release',)

    def __init__(self, **kwargs):
        super(KivyMDSettingsItem, self).__init__(**kwargs)
        self.value = self.panel.get_value(self.section, self.key)

    def add_widget(self, widget, *args):
        if issubclass(widget.__class__, IRightBodyTouch):
            self._touchable_widgets.append(widget)
            return self.ids['_right_container'].add_widget(widget)
        if self.content is None:
            return super(KivyMDSettingsItem, self).add_widget(widget, *args)
        return self.content.add_widget(widget, *args)

    def on_touch_down(self, touch):
        if self.propagate_touch_to_touchable_widgets(touch, 'down'):
            return
        super(TwoLineListItem, self).on_touch_down(touch)

    def on_touch_move(self, touch, *args):
        if self.propagate_touch_to_touchable_widgets(touch, 'move', *args):
            return
        super(TwoLineListItem, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch):
        if self.propagate_touch_to_touchable_widgets(touch, 'up'):
            return
        super(TwoLineListItem, self).on_touch_up(touch)

    def on_value(self, instance, value):
        if not self.section or not self.key:
            return
        # get current value in config
        panel = self.panel
        if not isinstance(value, string_types):
            value = str(value)
        panel.set_value(self.section, self.key, value)

    # def __init__(self, **kwargs):
    #     super(KivyMDSettingsItem, self).__init__()


class KivyMDSettingString(KivyMDSettingsItem):
    popup = ObjectProperty(None, allownone=True)
    '''(internal) Used to store the current popup when it's shown.

    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    textinput = ObjectProperty(None)
    '''(internal) Used to store the current textinput from the popup and
    to listen for changes.

    :attr:`textinput` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    '''

    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.text.strip()
        self.value = value

    def on_release(self):
        pass
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(None, None),
            size=(popup_width, '250dp'))

        # create the textinput used for numeric input
        self.textinput = textinput = TextInput(
            text=self.value, font_size='24sp', multiline=False,
            size_hint_y=None, height='42sp')
        textinput.bind(on_text_validate=self._validate)
        self.textinput = textinput

        # construct the content, widget are used as a spacer
        content.add_widget(Widget())
        content.add_widget(textinput)
        content.add_widget(Widget())
        content.add_widget(SettingSpacer())

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=self._validate)
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()


class KivyMDSettingNumeric(KivyMDSettingString):
    def _validate(self, instance):
        # we know the type just by checking if there is a '.' in the original
        # value
        is_float = '.' in str(self.value)
        self._dismiss()
        try:
            if is_float:
                self.value = text_type(float(self.textinput.text))
            else:
                self.value = text_type(int(self.textinput.text))
        except ValueError:
            return


class KivyMDSettingBoolean(KivyMDSettingsItem):
    values = ListProperty(['0', '1'])


class KivyMDSettingOptions(KivyMDSettingString):
    '''Implementation of an option list on top of a :class:`SettingItem`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivy.uix.popup.Popup` with a
    list of options from which the user can select.
    '''

    options = ListProperty([])
    '''List of all availables options. This must be a list of "string" items.
    Otherwise, it will crash. :)

    :attr:`options` is a :class:`~kivy.properties.ListProperty` and defaults
    to [].
    '''
    def _set_option(self, instance):
        self.value = instance.text
        self.popup.dismiss()

    def on_release(self):
        # create the popup
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            content=content, title=self.title, size_hint=(None, None),
            size=(popup_width, '400dp'))
        popup.height = len(self.options) * dp(55) + dp(150)

        # add all the options
        content.add_widget(Widget(size_hint_y=None, height=1))
        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = ToggleButton(text=option, state=state, group=uid)
            btn.bind(on_release=self._set_option)
            content.add_widget(btn)

        # finally, add a cancel button to return on the previous panel
        content.add_widget(SettingSpacer())
        btn = Button(text='Cancel', size_hint_y=None, height=dp(50))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)

        # and open the popup !
        popup.open()


class KivyMDSettingPath(KivyMDSettingString):
    '''Implementation of a Path setting on top of a :class:`SettingItem`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivy.uix.popup.Popup` with a
    :class:`~kivy.uix.filechooser.FileChooserListView` so the user can enter
    a custom value.

    .. versionadded:: 1.1.0
    '''

    show_hidden = BooleanProperty(False)
    '''Whether to show 'hidden' filenames. What that means is
    operating-system-dependent.

    :attr:`show_hidden` is an :class:`~kivy.properties.BooleanProperty` and
    defaults to False.

    .. versionadded:: 1.9.2
    '''

    dirselect = BooleanProperty(True)
    '''Whether to allow selection of directories.

    :attr:`dirselect` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to True.

    .. versionadded:: 1.9.2
    '''
    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.selection

        if not value:
            return

        self.value = os.path.realpath(value[0])

    def on_release(self):
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing=5)
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(None, 0.9),
            width=popup_width)

        # create the filechooser
        initial_path = self.value or os.getcwd()
        self.textinput = textinput = FileChooserListView(
            path=initial_path, size_hint=(1, 1),
            dirselect=self.dirselect, show_hidden=self.show_hidden)
        textinput.bind(on_path=self._validate)

        # construct the content
        content.add_widget(textinput)
        content.add_widget(SettingSpacer())

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=self._validate)
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()


class KivyMDSettingTitle(MDLabel):
    title = Label.text
    theme_text_color = 'Primary'
    panel = ObjectProperty(None)

class KivyMDSettingTime(KivyMDSettingString):
    def on_release(self):
        time_picker = MDTimePicker()
        time_picker.set_time(datetime.datetime.strptime(self.value, '%H:%M'))
        time_picker.bind(time=self._set_value)
        time_picker.open()

    def _set_value(self, instance, value):
        self.value = value.strftime('%H:%M')


class KivyMDSettingDate(KivyMDSettingString):
    def on_release(self):
        value = datetime.datetime.strptime(self.value, '%Y-%m-%d').date()
        date_picker = MDDatePicker(self._set_value, year=value.year, month=value.month, day=value.day)
        date_picker.open()

    def _set_value(self, value):
        self.value = value.strftime('%Y-%m-%d')
