def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')


# How to output colored text to a Linux terminal?
#   https://www.tutorialspoint.com/how-to-output-colored-text-to-a-linux-terminal
# Terminal Colors | Chris Yeh
#   https://chrisyeh96.github.io/2020/03/28/terminal-colors.html
color_table = {
    'fg_black'  : 30, 'bg_black'     : 40,
    'fg_red'    : 31, 'bg_red'       : 41,
    'fg_green'  : 32, 'bg_green'     : 42,
    'fg_yellow' : 33, 'bg_yellow'    : 43,
    'fg_blue'   : 34, 'bg_blue'      : 44,
    'fg_magenta': 35, 'bg_magenta'   : 45,
    'fg_cyan'   : 36, 'bg_cyan'      : 46,
    'fg_white'  : 37, 'bg_white'     : 47,
    'reset'     : 0,
    'bold'      : 1,  'bold_off'     : 21,
    'faint'     : 2,
    'underline' : 4,  'underline_off': 24,
    'blink'     : 5,
    'inverse'   : 7,  'inverse_off'  : 27,
}

"""
30-37      : foreground color (8 colors)
38;5;x     : foreground color (256 colors, non-standard)
38;2;r;g;b : foreground color (RGB, non-standard)

40-47      : background color (8 colors)
48;5;x     : background color (256 colors, non-standard)
48;2;r;g;b : background color (RGB, non-standard)

90-97      : bright foreground color (non-standard)
100-107    : bright background color (non-standard)

"""

msg_level_D = {
    'shell'  : '1;34;40',
    'success': '1;32;40',
    'info'   : '1;36;40',
    'warn'   : '1;35;40',
    'error'  : '1;31;40',
}

def color_print(s, level=''):
    cb = '\x1b[{}m'
    ce = '\x1b[0m'
    
    # cb = cb.format('1;33;40')
    cb = cb.format(msg_level_D[level])
    print(f'{cb}{s}{ce}')


# print_format_table()

for level in list(msg_level_D.keys()):
    color_print(f'{level}: this is a {level} message!', level=level)