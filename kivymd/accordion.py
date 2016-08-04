# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.properties import StringProperty,ListProperty,OptionProperty
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
from kivymd.theming import ThemableBehavior
from kivy.uix.accordion import Accordion, AccordionItem
from kivymd.backgroundcolorbehavior import BackgroundColorBehavior
from kivy.uix.boxlayout import BoxLayout

class MDAccordionItemTitleLayout(ThemableBehavior,BackgroundColorBehavior,BoxLayout):
    pass

class MDAccordion(ThemableBehavior,BackgroundColorBehavior, Accordion):
    pass

class MDAccordionItem(ThemableBehavior,AccordionItem):
    title_theme_color = OptionProperty(None, allownone=True,
                                       options=['Primary', 'Secondary', 'Hint',
                                                'Error', 'Custom'])
    ''' Color theme for title text and  icon '''

    title_color = ListProperty(None, allownone=True)
    ''' Color for title text and icon if `title_theme_color` is Custom '''
    
    background_color = ListProperty(None, allownone=True)
    ''' Color for the background of the accordian item title in rgba format. 
    '''
    
    divider_color = ListProperty(None, allownone=True)
    ''' Color for dividers between different titles in rgba format 
    To remove the divider set a color with an alpha of 0. 
    '''

    indicator_color = ListProperty(None, allownone=True)
    ''' Color for the indicator on the side of the active item in rgba format 
    To remove the indicator set a color with an alpha of 0. 
    '''


    title_template = StringProperty('MDAccordionItemTitle')
    ''' Template to use for the title '''
    
    icon_expanded = StringProperty('chevron-up')
    ''' Icon name to use when this item is expanded  '''
    
    icon_collapsed = StringProperty('chevron-down')
    ''' Icon name to use when this item is collapsed  '''
 
 
Builder.load_string('''
#:import MDLabel kivymd.label.MDLabel
#:import md_icons kivymd.icon_definitions.md_icons


<MDAccordionItem>:
    canvas.before:
        Color:
            rgba: self.background_color or self.theme_cls.primary_color
        Rectangle:
            size:self.size
            pos:self.pos
        PushMatrix
        Translate:
            xy: (dp(2),0) if self.orientation == 'vertical' else (0,dp(2))
    canvas.after:
        PopMatrix
        Color:
            rgba: self.divider_color or self.theme_cls.divider_color   
        Rectangle:
            size:(dp(1),self.height) if self.orientation == 'horizontal' else (self.width,dp(1)) 
            pos:self.pos
        Color:
            rgba: [0,0,0,0] if self.collapse else (self.indicator_color or self.theme_cls.accent_color)   
        Rectangle:
            size:(dp(2),self.height) if self.orientation == 'vertical' else (self.width,dp(2)) 
            pos:self.pos

[MDAccordionItemTitle@MDAccordionItemTitleLayout]:
    padding: '12dp'
    orientation: 'horizontal' if ctx.item.orientation=='vertical' else 'vertical'
    canvas:
        PushMatrix
        Translate:
            xy: (-dp(2),0) if ctx.item.orientation == 'vertical' else (0,-dp(2))
            
        Color:
            rgba: self.background_color or self.theme_cls.primary_color
        Rectangle:
            size:self.size
            pos:self.pos
        
    canvas.after:
        Color:
            rgba: [0,0,0,0] if ctx.item.collapse else (ctx.item.indicator_color or self.theme_cls.accent_color)   
        Rectangle:
            size:(dp(2),self.height) if ctx.item.orientation == 'vertical' else (self.width,dp(2)) 
            pos:self.pos
        PopMatrix
    MDLabel:
        id:_label
        theme_text_color:ctx.item.title_theme_color
        text_color:ctx.item.title_color
        text: ctx.item.title
        text_size: (self.width, None) if ctx.item.orientation=='vertical' else (None,self.width)
        canvas.before:
            PushMatrix
            Rotate:
                angle: 270 if ctx.item.orientation == 'horizontal' else 0
                origin: self.center
        canvas.after:
            PopMatrix
        
    MDLabel:
        id:_icon
        theme_text_color:ctx.item.title_theme_color
        text_color:ctx.item.title_color
        font_style:'Icon'
        text:md_icons[ctx.item.icon_collapsed if ctx.item.collapse else ctx.item.icon_expanded]
        halign: 'right' if ctx.item.orientation=='vertical' else 'center'
        #valign: 'middle' if ctx.item.orientation=='vertical' else 'bottom'
        canvas.before:
            PushMatrix
            Rotate:
                angle: 90 if ctx.item.orientation == 'horizontal' else 0
                origin:self.center
        canvas.after:
            PopMatrix
    
''')           
    
if __name__ == '__main__':
    from kivy.app import App
    from kivymd.theming import ThemeManager
    
    class AccordionApp(App):
        theme_cls = ThemeManager()
        def build(self):
            #self.theme_cls.primary_palette = 'Indigo'
            return Builder.load_string("""#:import MDLabel kivymd.label.MDLabel
BoxLayout:
    spacing: '64dp'
    MDAccordion:
        orientation:'vertical'
        MDAccordionItem:
            title:'Item 1'
            MDLabel:
                text:'Content 1'
                theme_text_color:'Primary'
        MDAccordionItem:
            title:'Item 2'
            MDLabel:
                text:'Content 2'
                theme_text_color:'Primary'
        MDAccordionItem:
            title:'Item 3'
            MDLabel:
                text:'Content 3'
                theme_text_color:'Primary'
    MDAccordion:
        orientation:'horizontal'
        MDAccordionItem:
            title:'Item 1'
            MDLabel:
                text:'Content 1'
                theme_text_color:'Primary'
        MDAccordionItem:
            title:'Item 2'
            MDLabel:
                text:'Content 2'
                theme_text_color:'Primary'
        MDAccordionItem:
            title:'Item 3'
            MDLabel:
                text:'Content 3'
                theme_text_color:'Primary'
""")
            

    AccordionApp().run()