"""set wallpaper"""
import subprocess

from libqtile import qtile, hook

from my_modules.param import PARAM


MONITOR0=0
MONITOR1=0

# 壁紙の割当

@hook.subscribe.setgroup
def change_wallpaper():
    if not PARAM.laptop:
        global MONITOR0
        global MONITOR1
        group = qtile.current_screen.group
        gidx = qtile.groups.index(group)
        if qtile.current_screen in qtile.screens:
            idx = qtile.screens.index(qtile.current_screen)
            n_groups = len(qtile.groups) // len(qtile.screens)
            if gidx >= n_groups:
                gidx -= n_groups
            if idx == 0:
                MONITOR0 = gidx
            else:
                MONITOR1 = gidx
            subprocess.run('feh --bg-fill {} --bg-fill {}'.format(str(PARAM.wallpapers[MONITOR0]), str(PARAM.wallpapers[MONITOR1])), shell=True)
