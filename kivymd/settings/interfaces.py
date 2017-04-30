from kivy.properties import ObjectProperty, NumericProperty, DictProperty, ConfigParser, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivymd.list import MDList

from kivymd.tabs import MDTab
from kivymd.theming import ThemableBehavior


class KivyMDSettingsInterfaceBlank(ScrollView, ThemableBehavior):
    '''A class for displaying settings panels. It displays a single
        settings panel at a time, taking up the full size and shape of the
        ContentPanel.
        '''

    panels = DictProperty({})
    '''(internal) Stores a dictionary mapping settings panels to their uids.

    :attr:`panels` is a :class:`~kivy.properties.DictProperty` and
    defaults to {}.

    '''

    container = ObjectProperty()
    '''(internal) A reference to the GridLayout that contains the
    settings panel.

    :attr:`container` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.

    '''

    current_panel = ObjectProperty(None)
    '''(internal) A reference to the current settings panel.

    :attr:`current_panel` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.

    '''

    current_uid = NumericProperty(0)
    '''(internal) A reference to the uid of the current settings panel.

    :attr:`current_uid` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 0.

    '''

    def add_panel(self, panel, name, uid):
        '''This method is used by Settings to add new panels for possible
        display. Any replacement for ContentPanel *must* implement
        this method.

        :Parameters:
            `panel`: :class:`SettingsPanel`
                It should be stored and displayed when requested.
            `name`:
                The name of the panel as a string. It may be used to represent
                the panel.
            `uid`:
                A unique int identifying the panel. It should be stored and
                used to identify panels when switching.

        '''
        self.panels[uid] = panel
        if not self.current_uid:
            self.current_uid = uid

    def on_current_uid(self, *args):
        '''The uid of the currently displayed panel. Changing this will
        automatically change the displayed panel.

        :Parameters:
            `uid`:
                A panel uid. It should be used to retrieve and display
                a settings panel that has previously been added with
                :meth:`add_panel`.

        '''
        uid = self.current_uid
        if uid in self.panels:
            if self.current_panel is not None:
                self.remove_widget(self.current_panel)
            new_panel = self.panels[uid]
            self.add_widget(new_panel)
            self.current_panel = new_panel
            return True
        return False  # New uid doesn't exist

    def add_widget(self, widget, **kwargs):
        if self.container is None:
            super(KivyMDSettingsInterfaceBlank, self).add_widget(widget)
        else:
            self.container.add_widget(widget)

    def remove_widget(self, widget):
        self.container.remove_widget(widget)


class KivyMDInterfaceWithTabbedPanel(FloatLayout, ThemableBehavior):
    '''The content widget used by :class:`SettingsWithTabbedPanel`. It
    stores and displays Settings panels in tabs of a TabbedPanel.

    This widget is considered internal and is not documented. See
    :class:`InterfaceWithSidebar` for information on defining your own
    interface widget.

    '''
    tabbedpanel = ObjectProperty()
    close_button = ObjectProperty()

    __events__ = ('on_close', )

    title = "Settings"

    def __init__(self, **kwargs):
        super(KivyMDInterfaceWithTabbedPanel, self).__init__(**kwargs)

    def add_panel(self, panel, name, uid):
        pass
        scrollview = ScrollView()
        scrollview.add_widget(panel)
        print('tab-{}'.format(name))
        tab = MDTab(name='tab-{}'.format(name), text=name)
        tab.add_widget(scrollview)
        self.tabbedpanel.add_widget(tab)

    def on_close(self, *args):
        pass


class KivyMDSettingsPanel(MDList):
    title = StringProperty('Default title')
    '''Title of the panel. The title will be reused by the :class:`Settings` in
    the sidebar.
    '''

    config = ObjectProperty(None, allownone=True)
    '''A :class:`kivy.config.ConfigParser` instance. See module documentation
    for more information.
    '''

    settings = ObjectProperty(None)
    '''A :class:`Settings` instance that will be used to fire the
    `on_config_change` event.
    '''

    def __init__(self, **kwargs):
        if 'cols' not in kwargs:
            self.cols = 1
        super(KivyMDSettingsPanel, self).__init__(**kwargs)

    def on_config(self, instance, value):
        if value is None:
            return
        if not isinstance(value, ConfigParser):
            raise Exception('Invalid config object, you must use a'
                            'kivy.config.ConfigParser, not another one !')

    def get_value(self, section, key):
        config = self.config
        if not config:
            return
        return config.get(section, key)

    def set_value(self, section, key, value):
        current = self.get_value(section, key)
        if current == value:
            return
        config = self.config
        if config:
            config.set(section, key, value)
            config.write()
        settings = self.settings
        if settings:
            settings.dispatch('on_config_change', config, section, key, value)

