# -*- coding: utf-8 -*-
# Two implementations. The first is based on color brightness obtained from:-
# https://www.w3.org/TR/AERT#color-contrast
# The second is based on relative luminance calculation for sRGB obtained from:-
# https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
# and contrast ratio calculation obtained from:-
# https://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef
#
# Preliminary testing suggests color brightness more closely matches the
# Material Design spec suggested text colors, but the alternative implementation
# is both newer and the current 'correct' recommendation, so is included here
# as an option.

''' Implementation of color brightness method '''
def _color_brightness(c):
    brightness = c[0] * 299 + c[1] * 587 + c[2] * 114
    brightness = brightness
    return brightness

def _black_or_white_by_color_brightness(color):
    if _color_brightness(color) >= 500:
        return 'black'
    else:
        return 'white'

''' Implementation of contrast ratio and relative luminance method '''
def _normalized_channel(c):
    if c <= 0.03928:
        return c/12.92
    else:
        return ((c + 0.055) / 1.055) ** 2.4

def _luminance(color):
    rg = _normalized_channel(color[0])
    gg = _normalized_channel(color[1])
    bg = _normalized_channel(color[2])
    return 0.2126*rg + 0.7152*gg + 0.0722*bg

def _black_or_white_by_contrast_ratio(color):
    l_color = _luminance(color)
    l_black = 0.0
    l_white = 1.0
    b_contrast = (l_color + 0.05) / (l_black + 0.05)
    w_contrast = (l_white + 0.05) / (l_color + 0.05)
    return 'white' if w_contrast >= b_contrast else 'black'

def get_contrast_text_color(color, use_color_brightness=True):
    if use_color_brightness:
        c = _black_or_white_by_color_brightness(color)
    else:
        c = _black_or_white_by_contrast_ratio(color)
    if c == 'white':
        return (1, 1, 1, 1)
    else:
        return (0, 0, 0, 1)

if __name__ == '__main__':
    from kivy.utils import get_color_from_hex
    from kivymd.color_definitions import colors, text_colors
    for c in ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue',
            'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime',
            'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Grey',
            'BlueGrey']:
        print("For the {} color palette:".format(c))
        for h in ['50', '100', '200', '300', '400', '500', '600', '700',
                '800', '900', 'A100', 'A200', 'A400', 'A700']:
            hex = colors[c].get(h)
            if hex:
                col = get_color_from_hex(hex)
                col_bri = get_contrast_text_color(col)
                con_rat = get_contrast_text_color(col, use_color_brightness=False)
                text_color = text_colors[c][h]
                print("   The {} hue gives {} using color brightness, {} using contrast ratio, and {} from the MD spec"
                        .format(h, col_bri, con_rat, text_color))
