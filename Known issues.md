# Deme KivyMD

## Known issues
- Have no limit minium widget
- Text box don't show
- Dropdown Menu don't have scroll layer
- On Buttons screen, check box disable_the_buttons have error
    ```
    raise AttributeError: 'super' object has no attribute 'on_disabled'
    File "C:\Users\LAPTOP MSI\Documents\KivyMD\demos\kitchen_sink\main.py", line 1087, in <module>

    # More info
    kivy._event.EventObservers._dispatch (kivy\_event.pyx:1120)
    ```
- Can not change theme of app
```
Exception has occurred: kivy.lang.builder.BuilderException
Parser: File "<inline>", line 284: ...     282:                                    size: self.size     283:                                    pos: self.pos >>  284:                            disabled: True     285:     286:        MDTab: ...
AttributeError: 'super' object has no attribute 'on_disabled'
File "C:\Users\LAPTOP MSI\Documents\Kivy-test\envK\lib\site-packages\kivy\lang\builder.py", line 619, in _apply_rule     setattr(widget_set, key, value)
File "kivy\weakproxy.pyx", line 33, in kivy.weakproxy.WeakProxy.__setattr__   File "kivy\properties.pyx", line 483, in kivy.properties.Property.__set__
File "kivy\properties.pyx", line 1470, in kivy.properties.AliasProperty.set
File "C:\Users\LAPTOP MSI\Documents\Kivy-test\envK\lib\site-packages\kivy\uix\widget.py", line 1318, in set_disabled     self.inc_disabled()
File "C:\Users\LAPTOP MSI\Documents\Kivy-test\envK\lib\site-packages\kivy\uix\widget.py", line 1325, in inc_disabled     self.property('disabled').dispatch(self)
File "kivy\properties.pyx", line 562, in kivy.properties.Property.dispatch
File "kivy\properties.pyx", line 579, in kivy.properties.Property.dispatch
File "kivy\_event.pyx", line 1214, in kivy._event.EventObservers.dispatch
File "kivy\_event.pyx", line 1120, in kivy._event.EventObservers._dispatch
File "C:\Users\LAPTOP MSI\Documents\Kivy-test\envK\lib\site-packages\kivymd\button.py", line 178, in on_disabled     super(BaseButton, self).on_disabled(instance, value)
File "C:\users\laptop msi\documents\kivy-test\&lt;string&gt;", line 629, in <module>
File "C:\Users\LAPTOP MSI\Documents\KivyMD\demos\kitchen_sink\main.py", line 1087, in <module>

# More info
kivy._event.EventObservers._dispatch (c:\Users\LAPTOP MSI\Documents\Kivy-test\kivy\_event.pyx:1098)
```
