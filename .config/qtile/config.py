"""config.py"""
from my_modules.param import PARAM

from my_modules.groups import set_groups
from my_modules.make_screens import make_screens
from my_modules.shortcut import *
from my_modules.set_wallpaper import *
from my_modules.startup import *


from libqtile.log_utils import logger

widget_defaults =  dict(
                    font=PARAM.font,
                    fontsize=PARAM.font_size,
                    padding=3
                )
extension_defaults = widget_defaults.copy()

groups = set_groups()
screens = make_screens(PARAM.num_screen)

dgroups_key_binder = PARAM.dgroups_key_binder
dgroups_app_rules = PARAM.dgroups_app_rules
follow_mouse_focus = PARAM.follow_mouse_focus
bring_front_click = PARAM.bring_front_click
cursor_warp = PARAM.cursor_warp
auto_fullscreen = PARAM.auto_fullscreen
focus_on_window_activation = PARAM.focus_on_window_activation
reconfigure_screens = PARAM.reconfigure_screens
auto_minimize = PARAM.auto_minimize
wmname = PARAM.wmname
