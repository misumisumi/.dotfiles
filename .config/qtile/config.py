from typing import List  # noqa: F401
from pathlib import Path
import subprocess
import asyncio
import time

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger
from libqtile.core.manager import Qtile
from libqtile import qtile

colors = {
        'BGbase': '#222d32', 'FGbase': '#475359',
        'black': '#01060e', 'red': 'ff5252',
        'green': '#4db69f', 'yellow': '#c9bc0e',
        'blue': '#008fc2', 'magenta': '#cf00ac',
        'cyan': '#02adc7', 'white': '#cfd8dc',
        'clear': '#00000000'
        }
colors2 = {
        'bblack': "#475359", 'bred': "#ff4f4d",
        'bgreen': "#56d6ba", 'byellow': "#c9c30e",
        'bblue': "#c9c30e", 'bmagenta': "#9c0082",
        'bcyan': "#02b7c7", 'bwhite': "#a7b0b5"
        }
screan_size = [2560-5, 1440]
pinp_size = [800, 450]
pinp_pos = [s-p for s, p in zip(screan_size, pinp_size)]

mod = 'mod4' # super key
terminal = 'kitty'
browser = 'vivaldi-stable'
home = Path.home()
capture_path = home.joinpath('Pictures', 'screenshot')
wallpapers = list(home.joinpath('Pictures', 'wallpapers').glob('*.jpg'))
wallpapers.sort()


num_screen = 2
laptop = False

pinp_window = None


monitor1=0
monitor2=0

@hook.subscribe.setgroup
def change_wallpaper():
    global monitor1
    global monitor2
    group = qtile.current_screen.group
    gidx = qtile.groups.index(group)
    if qtile.current_screen in qtile.screens:
        idx = qtile.screens.index(qtile.current_screen)
        n_groups = len(qtile.groups) // len(qtile.screens)
        if gidx >= n_groups:
            gidx -= n_groups
        if idx == 0:
            monitor1 = gidx
        else:
            monitor2 = gidx
        subprocess.run('feh --bg-fill {} --bg-fill {}'.format(str(wallpapers[monitor1]), str(wallpapers[monitor2])), shell=True)
        
# 擬似的に各スクリーンにグループが割り当てられるようにするための初期化
def init_screen_and_group():
    time.sleep(0.05)
    qtile.cmd_to_screen(0)
    logger.warning(qtile.groups)
    qtile.current_screen.set_group(qtile.groups[0])
    time.sleep(0.05)
    qtile.cmd_to_screen(1)
    qtile.current_screen.set_group(qtile.groups[7])

# StartUp
@hook.subscribe.startup_once
def autostart():
    subprocess.run('feh --bg-fill {} --bg-fill {}'.format(str(wallpapers[0]), str(wallpapers[0])), shell=True)
    init_screen_and_group()


# spotifyは起動直後はwindow nameを出さないため数msのdelayを設ける
@hook.subscribe.client_new
async def move_spotify(window):
    await asyncio.sleep(0.005)
    # logger.warning(window)
    if window.name == 'Spotify':
        window.togroup('0-media')
    elif window.name == 'ピクチャー イン ピクチャー':
        _pinp_pos = pinp_pos.copy()
        global pinp_window
        pinp_window = window
        idx = qtile.screens.index(qtile.current_screen)
        if idx == 1:
            _pinp_pos[0] += screan_size[0]
        window.cmd_place(*_pinp_pos, *pinp_size, borderwidth=2,
                         bordercolor=colors['cyan'], above=False, margin=None)
    elif window.name == 'WaveSurfer 1.8.8p5':
        window.togroup('0-analyze')
    else:
        pass


@hook.subscribe.client_killed
def remove_pinp(window):
    if window.name == 'ピクチャー イン ピクチャー':
        global pinp_window
        pinp_window = None


@hook.subscribe.focus_change
def float_always_show_front_focus_change():
    for window in qtile.current_group.windows:
        if window.floating:
            window.cmd_bring_to_front()


# floating windowは次に生成されたwindowの下にいきfocusが当てられないことへの回避策
floating_window_index = 0
def float_cycle(qtile, forward: bool):
    global floating_window_index
    floating_windows = []
    for window in qtile.current_group.windows:
        if window.floating:
            floating_windows.append(window)
    if not floating_windows:
        return
    floating_window_index = min(floating_window_index, len(floating_windows) -1)
    if forward:
        floating_window_index += 1
    else:
        floating_window_index += 1
    if floating_window_index >= len(floating_windows):
        floating_window_index = 0
    if floating_window_index < 0:
        floating_window_index = len(floating_windows) - 1
    win = floating_windows[floating_window_index]
    win.cmd_bring_to_front()
    win.cmd_focus()


@lazy.function
def float_cycle_backward(qtile):
    float_cycle(qtile, False)


@lazy.function
def float_cycle_forward(qtile):
    float_cycle(qtile, True)


@lazy.function
def keep_pinp(qtile):
    if pinp_window is not None:
        n_screen = len(qtile.screens)
        now_pinp_screen = qtile.groups.index(pinp_window.group) // (len(qtile.groups) // n_screen)
        idx = qtile.screens.index(qtile.current_screen)
        if now_pinp_screen == idx:
            pinp_window.togroup(qtile.current_screen.group.name)
            for window in qtile.current_group.windows:
                if not window.floating:
                    break
            window.cmd_focus(warp=True)


def check_screen(idx, min_idx, max_idx):
    return min_idx <= idx < max_idx

def calc_range_idx(current_screen_idx, num_group):
    n_screen = len(qtile.screens)
    group_per_s = num_group // n_screen
    min_idx = group_per_s * current_screen_idx
    max_idx = group_per_s*(current_screen_idx + 1)
    return min_idx, max_idx

# Groupを自動的に取得してwindowまたはfocusを適切に配置する
@lazy.function
def focus_previous_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)

    previous_group = group.get_previous_group(skip_empty=True)
    previous_group_index = qtile.groups.index(previous_group)

    idx = qtile.screens.index(qtile.current_screen)
    min_idx, max_idx = calc_range_idx(idx, len(qtile.groups))
    check = check_screen(previous_group_index, min_idx, max_idx)

    if previous_group_index < group_index and check:
        qtile.current_screen.set_group(previous_group)


@lazy.function
def focus_next_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)

    next_group = group.get_next_group(skip_empty=True)
    next_group_index = qtile.groups.index(next_group)

    idx = qtile.screens.index(qtile.current_screen)
    min_idx, max_idx = calc_range_idx(idx, len(qtile.groups))
    check = check_screen(next_group_index, min_idx, max_idx)

    if next_group_index > group_index and check:
        qtile.current_screen.set_group(next_group)
        

@lazy.function
def window_to_previous_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)

    previous_group = group.get_previous_group(skip_empty=False)
    previous_group_index = qtile.groups.index(previous_group)

    idx = qtile.screens.index(qtile.current_screen)
    min_idx, max_idx = calc_range_idx(idx, len(qtile.groups))
    check = check_screen(previous_group_index, min_idx, max_idx)

    if previous_group_index < group_index and check:
        qtile.current_window.togroup(previous_group.name, switch_group=True)


@lazy.function
def window_to_next_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)

    next_group = group.get_next_group(skip_empty=False)
    next_group_index = qtile.groups.index(next_group)

    idx = qtile.screens.index(qtile.current_screen)
    min_idx, max_idx = calc_range_idx(idx, len(qtile.groups))
    check = check_screen(next_group_index, min_idx, max_idx)
    if next_group_index > group_index and check:
        qtile.current_window.togroup(next_group.name, switch_group=True)


@lazy.function
def focus_n_screen_group(qtile, idx, g_per_s):
    groups = qtile.groups
    s_idx = qtile.screens.index(qtile.current_screen)
    if idx < g_per_s:
        qtile.current_screen.set_group(groups[int(idx + g_per_s*s_idx)])


@lazy.function
def move_n_screen_group(qtile, idx, g_per_s):
    groups = qtile.groups
    s_idx = qtile.screens.index(qtile.current_screen)
    if idx < g_per_s:
        qtile.current_window.togroup(groups[int(idx + g_per_s*s_idx)].name, switch_group=True)


@lazy.function
def focus_prev_screen(qtile,):
    n_screen = len(qtile.screens)
    idx = qtile.screens.index(qtile.current_screen)
    prev_idx = idx - 1
    if prev_idx >= 0:
        qtile.cmd_to_screen(prev_idx)


@lazy.function
def focus_next_screen(qtile,):
    n_screen = len(qtile.screens)
    idx = qtile.screens.index(qtile.current_screen)
    next_idx = idx + 1
    if next_idx < n_screen:
        qtile.cmd_to_screen(next_idx)


@lazy.function
def focus_cycle_screen(qtile, backward=False):
    n_screen = len(qtile.screens)
    idx = qtile.screens.index(qtile.current_screen)
    if backward:
        to_idx = n_screen - 1 if idx == 0 else idx - 1
        qtile.cmd_to_screen(to_idx)
    else:
        to_idx = 0 if idx + 1 == n_screen else idx + 1
        qtile.cmd_to_screen(to_idx)


@lazy.function
def move_cycle_screen(qtile, backward=False):
    n_screen = len(qtile.screens)
    idx = qtile.screens.index(qtile.current_screen)
    if backward:
        to_idx = n_screen - 1 if idx == 0 else idx - 1
        group = qtile.screens[to_idx].group.name
        qtile.current_window.togroup(group)
    else:
        to_idx = 0 if idx + 1 == n_screen else idx + 1
        group = qtile.screens[to_idx].group.name
        qtile.current_window.togroup(group)


@lazy.function
def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


@lazy.function
def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


keys = [
    # Switch between windows
    Key([mod], 'h', lazy.layout.left(), desc='Move focus to left'),
    Key([mod], 'l', lazy.layout.right(), desc='Move focus to right'),
    Key([mod], 'j', lazy.layout.down(), desc='Move focus down'),
    Key([mod], 'k', lazy.layout.up(), desc='Move focus up'),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, 'shift'], 'h',
        lazy.layout.shuffle_left(),
        lazy.layout.move_left(),
        desc='Move window to the left'),
    Key([mod, 'shift'], 'l',
        lazy.layout.shuffle_right(),
        lazy.layout.move_right(),
        desc='Move window to the right'),
    Key([mod, 'shift'], 'j', 
        lazy.layout.shuffle_down(),
        lazy.layout.section_down(),
        desc='Move window down'),
    Key([mod, 'shift'], 'k',
        lazy.layout.shuffle_up(),
        lazy.layout.section_up(),
        desc='Move window up'),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, 'control'], 'h',
        focus_previous_group(),
        keep_pinp(),
        desc='focus prev group'),
    Key([mod, 'control'], 'l',
        focus_next_group(),
        keep_pinp(),
        desc='focus next group'),
    # Key([mod, 'control'], 'j', lazy.layout.grow_down(), desc='Grow window down'),
    # Key([mod, 'control'], 'k', lazy.layout.grow_up(), desc='Grow window up'),

    Key([mod, 'shift', 'control'], 'h', 
        window_to_previous_group(), keep_pinp(), desc='win to prev group'),
    Key([mod, 'shift', 'control'], 'l',
        window_to_next_group(), keep_pinp(), desc='win to next group'),

    # Key([mod], 'p', focus_prev_screen(),  desc='focus prev screen'),
    # Key([mod], 'n', focus_next_screen(),  desc='focus next screen'),
    Key([mod], 'n', focus_cycle_screen(),  desc='focus next screen'),
    Key([mod], 'm', focus_cycle_screen(backward=True),  desc='focus next screen'),
    # Key([mod, 'shift'], 'p', window_to_previous_screen(), keep_pinp()),
    Key([mod, 'shift'], 'n', move_cycle_screen(), keep_pinp()),
    Key([mod, 'shift'], 'm', move_cycle_screen(backward=True), keep_pinp()),

    Key([mod], 'space', lazy.window.toggle_maximize()),
    Key([mod, 'shift'], 'space', lazy.window.toggle_minimize()),

    Key([mod], 'f', lazy.window.toggle_fullscreen()),
    Key([mod, 'shift'], 'f', lazy.window.toggle_floating()),

    # Change other layout
    Key([mod], 'Tab', lazy.next_layout(),
        desc='Move window focus to other window'),

    # Key([mod], 'n', lazy.layout.normalize(), desc='Reset all window sizes'),

    Key([mod], 's', lazy.layout.toggle_split(), desc='Launch terminal'),
    Key([mod, 'shift'], 'Return', lazy.spawn(terminal), desc='Launch terminal'),

    Key([mod, 'shift'], 'c', lazy.window.kill(), desc='Kill focused window'),

    Key([mod, 'control'], 'r', lazy.reload_config(), desc='Reload the config'),
    Key([mod, 'control'], 'e', lazy.shutdown(), desc='Shutdown Qtile'),

    # Key([mod], 'm', lazy.spawn('rofi -modi combi -show combi -combi-modi window,drun -show-icons'), desc='show rofi'),
    # Key([mod, 'shift'], 'm', lazy.spawn('rofi -show run'), desc='run rofi script mode'),
    # Key([mod, 'control'], 'm', lazy.spawn('rofi -show power-menu -modi power-menu:rofi-power-menu -show-icons'), desc='run rofi script mode'),
    Key([mod], 'p', lazy.spawn('rofi -modi combi -show combi -combi-modi window,drun -show-icons'), desc='show rofi'),
    Key([mod, 'shift'], 'p', lazy.spawn('rofi -show run'), desc='run rofi script mode'),
    Key([mod, 'control'], 'p', lazy.spawn('rofi -show power-menu -modi power-menu:rofi-power-menu -show-icons'), desc='run rofi script mode'),

    Key([], 'Print', lazy.spawn('flameshot full -p {}'.format(str(capture_path)))),
    Key([mod], 'Print', lazy.spawn('flameshot screen -p {}'.format(str(capture_path)))),
    Key([mod, 'shift'], 'Print', lazy.spawn('flameshot screen -c')),
    Key([mod], "period", float_cycle_forward()),
    Key([mod], "comma", float_cycle_backward()),

    Key([mod], 'q', lazy.spawn('copyq show')),
    Key([mod], 'b', lazy.spawn(browser)),

    Key([], 'XF86AudioRaiseVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +5%')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%')),
    Key([], 'XF86AudioMute', lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),
    Key([], 'XF86AudioMicMute', lazy.spawn('pactl set-source-mute @DEFAULT_SINK@ toggle')),
    Key([], 'XF86AudioPause', lazy.spawn('playerctl play-pause')),
    Key([], 'XF86AudioPlay', lazy.spawn('playerctl play-pause')),
    Key([], 'XF86AudioNext', lazy.spawn('playerctl next')),
    Key([], 'XF86AudioPrev', lazy.spawn('playerctl previous')),
    Key([], 'XF86MonBrightnessUp', lazy.spawn('light -A 5')),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('light -U 5')),
    Key([], 'XF86KbdBrightnessUp', lazy.spawn('light -Ars {} 1'.format('sysfs/leds/asus::kbd_backlight'))),
    Key([], 'XF86KbdBrightnessDown', lazy.spawn('light -Urs {} 1'.format('sysfs/leds/asus::kbd_backlight'))),
    Key([], 'XF86Launch4', lazy.spawn('asusctl profile -n'))

]

default_settings = {'border_width': 2,
                  'border_focus': colors['blue'],
                  'border_normal': colors['BGbase']}
margin = 14
# for default
layouts = [
    layout.Columns(**default_settings,
                   border_focus_stack=colors['cyan'],
                   border_normal_stack=colors['BGbase'],
                   border_on_single=True, fair=False,
                   num_columns=2, insert_position=1,
                   margin=margin, margin_on_single=margin,
                   split=False),
    layout.TreeTab(active_bg=colors2['bblack'],
                   bg_color=colors['BGbase'],
                   font='Noto Sans CJK JP',
                   sections=['WS{}'.format(i) for i in range(1, 4)],
                   level_shift=20,
                   fontsize=14,
                   section_fontsize=16,
                   ),
]
# For code
layouts2 = [
    layout.MonadWide(**default_settings,
                     ratio=0.6,
                     new_client_position='bottom',
                     single_border_width=2,
                     margin=margin, single_margin=margin
                     ),
        ]
# For full
layouts3 = [
    layout.TreeTab(active_bg=colors2['bblack'],
                   bg_color=colors['BGbase'],
                   font='Noto Sans CJK JP',
                   sections=['WS{}'.format(i) for i in range(1, 6)],
                   level_shift=20,
                   fontsize=14,
                   section_fontsize=16,
                   ),
    ]
# For media
layouts4 = [
    layout.Slice(match=Match(wm_class='pavucontrol'), width=350, side='bottom',
                 fallback=layouts[0]),
    ]

match_code = [Match(wm_class='code')]
match_browse = [Match(wm_class='vivaldi-stable'), Match(wm_class='firefox'),
                Match(wm_class='virt-manager')]
match_paper = [Match(wm_class='zathura')]
match_analyze = [Match(title='WaveSurfer 1.8.8p5'), Match(wm_class='thunar'),
                 Match(wm_class='mpv')]
match_full = [Match(wm_class='Steam'), Match(wm_class='krita'),
              Match(wm_class='Gimp'), Match(wm_class='Blender'),
              Match(wm_class='unityhub'), Match(wm_class='Unity'),
              Match(wm_class='obs'), Match(wm_class='audacity'),
              Match(wm_class='looking-glass')]
match_sns = [Match(wm_class='slack'), Match(wm_class='discord'),
             Match(wm_class='zoom')]
match_media = [Match(wm_class='pavucontrol'), Match(wm_class='blueman-manager')]

groups = list()
_groups = {'code': ('', layouts2, match_code),
           'browse': ('', layouts, match_browse),
           'paper': ('', layouts, match_paper),
           'analyze': ('', layouts, match_analyze),
           'full': ('', layouts3, match_full),
           'sns': ('', layouts, match_sns),
           'media': ('', layouts4, match_media)}

if laptop:
    for k, (label, layouts, matches) in _groups.items():
        groups.append(Group('{}-{}'.format(0, k), layouts=layouts, matches=matches, label=label))
else:
    for n in range(num_screen):
        for k, (label, layouts, matches) in _groups.items():
            groups.append(Group('{}-{}'.format(n, k), layouts=layouts, matches=matches, label=label))

for n, i in enumerate(groups, 1):
    keys.extend([
        # mod1 + letter of group = switch to group
        # Key([mod], str(n), lazy.group[i.name].toscreen(0, toggle=False),
        #     keep_pinp(),
        #     desc='Switch to group {}'.format(i.name)),
        Key([mod], str(n), focus_n_screen_group(n-1, len(_groups)), keep_pinp,
            desc='Switch to group {}'.format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, 'shift'], str(n), move_n_screen_group(n-1, len(_groups)), keep_pinp,
            desc='Switch to & move focused window to group {}'.format(i.name)),
    ])
    if n == len(_groups):
        break


@hook.subscribe.screen_change
def attach_screen(notify):
    out = subprocess.check_output('xrandr --listmonitors', shell=True)
    n_monitor = int(out.decode('utf-8').split('\n')[0].split(' ')[-1])
    time.sleep(0.1)
    subprocess.run('xrandr --output eDP --auto --output HDMI-A-0 --auto --right-of eDP', shell=True)
    for k, (label, layouts, matches) in _groups.items():
        qtile.add_group('{}-{}'.format(1, k), layouts=layouts, label=label)


widget_defaults = dict(
    font='Noto Sans CJK JP',
    fontsize=18,
    padding=3,
)
extension_defaults = widget_defaults.copy()
colorset1 = {'background': colors['BGbase'], 'foreground': colors['cyan']}
colorset2 = {'background': colors['cyan'], 'foreground': colors['BGbase']}
colorset3 = {'background': colors['blue'], 'foreground': colors['BGbase']}
colorset4 = {'background': colors['BGbase'], 'foreground': colors['blue']}
colorset5 = {'background': colors['clear'], 'foreground': colors['BGbase']}
colorset6 = {'background': colors['BGbase'], 'foreground': colors['white']}

def left_corner(background, foreground):
    return widget.TextBox(
        foreground = foreground,
        background = background,
        text = "\ue0b6",
        fontsize = 36,
        padding=0
    )

def right_corner(background, foreground):
    return widget.TextBox(
        foreground = foreground,
        background = background,
        text = "\ue0b4",
        fontsize = 36,
        padding=0
    )

def separator():
    return widget.Sep(
        linewidth = 0,
        padding = 10
    )

gaps = 15
screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.Wallpaper(random_selection=True),
                left_corner(**colorset1),
                widget.CurrentScreen(active_color=colors['magenta'],
                                     inactive_color=colors['BGbase'],
                                     inactive_text='N', **colorset2),
                right_corner(**colorset1),
                separator(),
                left_corner(**colorset1),
                widget.CurrentLayout(fmt='{:.3}', **colorset2),
                right_corner(**colorset1),
                separator(),
                left_corner(**colorset4),
                widget.GroupBox(this_current_screen_border=colors['cyan'], borderwidth=2, **colorset3,
                                active=colors['white']),
                right_corner(**colorset4),
                separator(),
                left_corner(**colorset1),
                widget.CPU(format=' {load_percent}%', **colorset2),
                right_corner(**colorset1),
                widget.Memory(format=' {MemUsed: .1f}{mm}/{MemTotal: .1f}{mm}',
                              measure_mem='G', measure_swap='G', **colorset1),
                right_corner(**colorset2),
                widget.DF(format = " {f} GB ({r:.0f}%)", visible_on_warn=False,
                          partition='/home', **colorset2),
                right_corner(**colorset1),
                widget.Spacer(),
                left_corner(**colorset1),
                widget.Clock(format='%Y-%m-%d %a %I:%M:%S %p', **colorset2),
                right_corner(**colorset1),
                separator(),
                separator(),
                left_corner(**colorset4),
                widget.TaskList(border=colors['BGbase'], borderwidth=2, max_title_width=120, **colorset3),
                right_corner(**colorset4),
                separator(),
                left_corner(**colorset1),
                widget.Net(format='{down} ↓↑ {up}', **colorset2),
                right_corner(**colorset1),
                widget.PulseVolume(fmt=' {}', limit_max_volume=True, volume_app='pavucontrol',
                                   update_interval=0.1, **colorset1),
                right_corner(**colorset2),
                # widget.Backlight(fmt=' {}', backlight_name='amdgpu_bl0', **colorset2),
                # right_corner(**colorset1),
                # widget.Battery(format=' {percent:2.0%}', **colorset1),
                # right_corner(**colorset2),
                widget.CheckUpdates(display_format=' {updates}', distro='Arch_paru',
                                    colour_have_updates=colors['magenta'], colour_no_updates=colors['BGbase'],
                                    update_interval=60*60, no_update_string='  0', **colorset2),
                right_corner(**colorset1),
                separator(),
                left_corner(**colorset4),
                widget.Systray(**colorset3),
                right_corner(**colorset4),
                separator(),
                     
            ],
            32,
            background=colors['BGbase'],
            border_color=colors['cyan']
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=['ff00ff', '000000', 'ff00ff', '000000']  # Borders are magenta
        ),
        # right=bar.Gap(gaps),
        # left=bar.Gap(gaps)
        # bottom=bar.Bar(
        #     [widget.Spacer(),
        #      left_corner(**colorset5),
        #      widget.TaskList(border=colors['cyan'], borderwidth=2, max_title_width=120, **colorset6),
        #      right_corner(**colorset5),
        #      widget.Spacer()],
        #     32,
        #     background=colors['clear'],
        #     border_color=colors['cyan'],
        #     opacity=1,
        #         )
    ),
    Screen(
        top=bar.Bar(
            [
                left_corner(**colorset1),
                widget.CurrentScreen(active_color=colors['magenta'],
                                     inactive_color=colors['BGbase'], 
                                     inactive_text='N',**colorset2),
                right_corner(**colorset1),
                separator(),
                left_corner(**colorset1),
                widget.CurrentLayout(fmt='{:.3}', **colorset2),
                right_corner(**colorset1),
                separator(),
                left_corner(**colorset4),
                widget.GroupBox(this_current_screen_border=colors['cyan'], borderwidth=2, **colorset3,
                                active=colors['white']),
                right_corner(**colorset4),
                separator(),
                left_corner(**colorset1),
                widget.CPU(format=' {load_percent}%', **colorset2),
                right_corner(**colorset1),
                widget.Memory(format=' {MemUsed: .1f}{mm}/{MemTotal: .1f}{mm}',
                              measure_mem='G', measure_swap='G', **colorset1),
                right_corner(**colorset2),
                widget.DF(format = " {f} GB ({r:.0f}%)", visible_on_warn=False,
                          partition='/home', **colorset2),
                right_corner(**colorset1),
                widget.Spacer(),
                left_corner(**colorset1),
                widget.Clock(format='%Y-%m-%d %a %I:%M:%S %p', **colorset2),
                right_corner(**colorset1),
                separator(),
                separator(),
                left_corner(**colorset4),
                widget.TaskList(border=colors['BGbase'], borderwidth=2, max_title_width=120, **colorset3),
                right_corner(**colorset4),
                separator(),
                left_corner(**colorset1),
                widget.Net(format='{down} ↓↑ {up}', **colorset2),
                right_corner(**colorset1),
                widget.PulseVolume(fmt=' {}', limit_max_volume=True, volume_app='pavucontrol',
                                   update_interval=0.1, **colorset1),
                right_corner(**colorset2),
                # widget.Backlight(fmt=' {}', backlight_name='amdgpu_bl0', **colorset2),
                # right_corner(**colorset1),
                # widget.Battery(format=' {percent:2.0%}', **colorset1),
                # right_corner(**colorset2),
                widget.CheckUpdates(display_format=' {updates}', distro='Arch_paru',
                                    colour_have_updates=colors['magenta'], colour_no_updates=colors['BGbase'],
                                    update_interval=60*60, no_update_string='  0', **colorset2),
                right_corner(**colorset1),
                     
            ],
            32,
            background=colors['BGbase'],
            border_color=colors['cyan']
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=['ff00ff', '000000', 'ff00ff', '000000']  # Borders are magenta
        ),
        # right=bar.Gap(gaps),
        # left=bar.Gap(gaps)
        # bottom=bar.Bar(
        #     [widget.Spacer(),
        #      left_corner(**colorset5),
        #      widget.TaskList(border=colors['cyan'], borderwidth=2, max_title_width=120, **colorset6),
        #      right_corner(**colorset5),
        #      widget.Spacer()],
        #     32,
        #     background=colors['clear'],
        #     border_color=colors['cyan'],
        #     opacity=1,
        #         )
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod, 'shift'], 'Button1', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    # Click([mod], 'Button2', lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules, # アスペクト比固定のものでもタイリングさせる
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], **default_settings)
auto_fullscreen = True
focus_on_window_activation = 'smart'
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
# wmname = 'LG3D'
wmname = 'qtile'
