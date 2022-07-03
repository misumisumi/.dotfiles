"""config.py"""
from my_modules.groups import set_groups
from my_modules.widgets import default_settings
from my_modules.make_screens import make_screens
from my_modules.shortcut import *
from my_modules.set_wallpaper import *
from my_modules.startup import *

from my_modules.param import PARAM

from libqtile.log_utils import logger

groups = set_groups()
widget_default, extension_defaults = default_settings()
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
