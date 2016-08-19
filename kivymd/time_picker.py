from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.metrics import dp
from kivy.animation import Animation
from kivymd.dialog import MDDialog
from theming import ThemableBehavior
from elevationbehavior import ElevationBehavior
from kivymd.button import MDFlatButton
import math

Builder.load_string('''
<MDTimeDialog>:
    Dial
    MDRaisedButton:
        text: "Open time-picker"
        size_hint: None, None
        size: 3 * dp(48), dp(48)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        opposite_colors: True
        on_release: root.dismiss()

<Dial>:
    circle_id: circle_id
    size: root.size
    pos: 0, 0
    canvas:
        Rotate:
            angle: self.angle
            origin: self.center
        Color:
            rgb: 1, 0, 0
        Ellipse:
            size: min(self.size), min(self.size)
            pos: 0.5*self.size[0] - 0.5*min(self.size), 0.5*self.size[1] - 0.5*min(self.size)
    Circle:
        id: circle_id
        size_hint: 0, 0
        size: 50, 50
        pos: 0.5*root.size[0]-25, 0.9*root.size[1]-25
        canvas:
            Color:
                rgb: 0, 1, 0
            Ellipse:
                size: 50, 50
                pos: self.pos
''')


class Circle(Widget):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print "small circle clicked"


class MDTimeDialog(ThemableBehavior, ElevationBehavior, ModalView):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MDTimeDialog, self).__init__(**kwargs)
        if self._window is not None:
            # Logger.warning('ModalView: you can only open once.')
            return self
        # search window
        self._window = self._search_window()
        if not self._window:
            # Logger.warning('ModalView: cannot open view, no window found.')
            return self
        self._window.add_widget(self)

    def dismiss(self, *largs, **kwargs):
        '''Close the view if it is open. If you really want to close the
            view, whatever the on_dismiss event returns, you can use the *force*
            argument:
            ::

                view = ModalView(...)
                view.dismiss(force=True)

            When the view is dismissed, it will be faded out before being
            removed from the parent. If you don't want animation, use::

                view.dismiss(animation=False)

            '''
        if self._window is None:
            return self
        if self.dispatch('on_dismiss') is True:
            if kwargs.get('force', False) is not True:
                return self
        if kwargs.get('animation', True):
            Animation(_anim_alpha=0., d=2).start(self)
        else:
            self._anim_alpha = 0
            self._real_remove_widget()
        return self


class Dial(Widget):
    angle = NumericProperty(0)

    def __int__(self):
        self.start_on_small = False

    def on_touch_down(self, touch):
        if not self.circle_id.collide_point(*touch.pos):
            self.start_on_small = False
            print "big circle clicked"
        else:
            self.start_on_small = True
            y = (touch.y - self.center[1])
            x = (touch.x - self.center[0])
            calc = math.degrees(math.atan2(y, x))
            self.prev_angle = calc if calc > 0 else 360+calc
            self.tmp = self.angle

            return super(Dial, self).on_touch_down(touch) # dispatch touch event futher

    def on_touch_move(self, touch):
        if self.start_on_small:
            y = (touch.y - self.center[1])
            x = (touch.x - self.center[0])
            calc = math.degrees(math.atan2(y, x))
            new_angle = calc if calc > 0 else 360+calc

            self.angle = self.tmp + (new_angle-self.prev_angle)%360

    def on_touch_up(self, touch):
        self.start_on_small = False
        Animation(angle=0).start(self)

