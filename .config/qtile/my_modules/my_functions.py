"""custom function for qtile"""
import asyncio
import subprocess

from libqtile.core.manager import Qtile
from libqtile import qtile, hook
from libqtile.lazy import lazy

from my_modules.param import PARAM
from my_modules.groups import GROUP_PER_SCREEN

from libqtile.log_utils import logger


PINP_WINDOW = None
FLOATING_WINDOW_IDX = 0
monitor_pos = 'delete'
if not PARAM.laptop:
    monitor_pos = 'right-of'

# @hook.subscribe.client_focus
# def check_window_id(window):
#     logger.warning('idx: {}'.format(qtile.current_screen.index))


# PinPの生成時とWS切替時にフォーカスを当てないようにする
def keep_focus_window_in_tiling(window=None):
    if window is None:
        for window in qtile.current_group.windows:
            if not window.floating:
                break
    qtile.current_group.focus(window, True)


# 一部のソフトは起動直後はwindow nameを出さないため数msのdelayを設ける
@hook.subscribe.client_new
async def move_speclific_apps(window):
    await asyncio.sleep(0.01)
    if window.name == 'Spotify':
        window.togroup('0-media')
    elif window.name == 'ピクチャー イン ピクチャー' or window.name == 'Picture-in-Picture':
        # 画面サイズに合わせて自動的にPinPのサイズとポジションを決定する
        screen_size = (qtile.current_screen.width, qtile.current_screen.height)
        pinp_size = [int(s//PARAM.pinp_scale_down) for s in screen_size]
        pinp_pos = [s-p for s, p in zip(screen_size, pinp_size)]
        pinp_pos[0] = pinp_pos[0] - PARAM.pinp_margin

        global PINP_WINDOW
        PINP_WINDOW = window
        idx = qtile.current_screen.index
        if (monitor_pos == 'right-of' and idx == 1) or (monitor_pos == 'left-of' and idx == 0):
            pinp_pos[0] += screen_size[0]
        elif (monitor_pos == 'below' and idx == 1) or (monitor_pos == 'above' and idx == 0):
            pinp_pos[1] += screen_size[1]
        else:
            pass
        window.cmd_place(*pinp_pos, *pinp_size, borderwidth=PARAM.border,
                         bordercolor=PARAM.c_normal['cyan'], above=False, margin=None)
        keep_focus_window_in_tiling()
    elif window.name == 'WaveSurfer 1.8.8p5':
        window.togroup('0-analyze')
    elif PINP_WINDOW is not None:
        PINP_WINDOW.cmd_bring_to_front()
    else:
        pass


@hook.subscribe.client_killed
def remove_pinp(window):
    if window.name == 'ピクチャー イン ピクチャー' or window.name == 'Picture-in-Picture':
        global PINP_WINDOW
        PINP_WINDOW = None


@lazy.function
def keep_pinp(qtile):
    """
    workspaceを跨いでもPinPが同じ位置に表示されるようにする
    """
    if PINP_WINDOW is not None:
        n_screen = len(qtile.screens)
        now_pinp_screen = qtile.groups.index(PINP_WINDOW.group) // (len(qtile.groups) // n_screen)
        idx = qtile.current_screen.index
        win = qtile.current_window
        if now_pinp_screen == idx:
            PINP_WINDOW.togroup(qtile.current_screen.group.name)
            PINP_WINDOW.cmd_bring_to_front()
            keep_focus_window_in_tiling(win)


@lazy.function
def move_pinp(qtile, pos):
    """
    モニターの四隅にPinP windowを移動できるようにする
    """
    idx = qtile.current_screen.index
    n_screen = len(qtile.screens)
    now_pinp_screen = qtile.groups.index(PINP_WINDOW.group) // (len(qtile.groups) // n_screen)
    if PINP_WINDOW is not None and idx == now_pinp_screen:
        screen_size = (qtile.current_screen.width, qtile.current_screen.height)
        pinp_size = [int(s//PARAM.pinp_scale_down) for s in screen_size]
        pinp_pos = [PINP_WINDOW.float_x, PINP_WINDOW.float_y]
        if pos == 'up':
            pinp_pos[1] = 0
        elif pos == 'down':
            pinp_pos[1] = screen_size[1] - pinp_size[1] - PARAM.pinp_margin
        elif pos == 'left':
            pinp_pos[0] = PARAM.pinp_margin
        else:
            pinp_pos[0] = screen_size[0] - pinp_size[0] - PARAM.pinp_margin
        if (monitor_pos == 'right-of' and idx == 1) or (monitor_pos == 'left-of' and idx == 0):
            pinp_pos[0] += screen_size[0]
        elif (monitor_pos == 'above' and idx == 0) or (monitor_pos == 'below' and idx == 1):
            pinp_pos[1] += screen_size[1]
        else:
            pass
        win = qtile.current_window
        PINP_WINDOW.cmd_place(*pinp_pos, *pinp_size, borderwidth=PARAM.border,
                              bordercolor=PARAM.c_normal['cyan'], above=False, margin=None)
        PINP_WINDOW.cmd_bring_to_front()
        keep_focus_window_in_tiling(win)


# floating windowは次に生成されたwindowの下にいきfocusが当てられないことへの回避策
@lazy.function
def float_cycle(qtile, forward: bool, focus=False):
    global FLOATING_WINDOW_IDX
    floating_windows = []
    for window in qtile.current_group.windows:
        if window.floating:
            floating_windows.append(window)
    if not floating_windows:
        return
    FLOATING_WINDOW_IDX = min(FLOATING_WINDOW_IDX, len(floating_windows) -1)
    if forward:
        FLOATING_WINDOW_IDX += 1
    else:
        FLOATING_WINDOW_IDX += 1
    if FLOATING_WINDOW_IDX >= len(floating_windows):
        FLOATING_WINDOW_IDX = 0
    if FLOATING_WINDOW_IDX < 0:
        FLOATING_WINDOW_IDX = len(floating_windows) - 1
    win = floating_windows[FLOATING_WINDOW_IDX]
    win.cmd_bring_to_front()
    if focus:
        qtile.current_group.focus(win, True)


def check_screen(idx, min_idx, max_idx):
    return min_idx <= idx < max_idx


def calc_range_idx(current_screen_idx):
    """
    あるモニターに所属している先頭と末尾のグループのidxを取得
    """
    min_idx = GROUP_PER_SCREEN * current_screen_idx
    max_idx = GROUP_PER_SCREEN*(current_screen_idx + 1)
    return min_idx, max_idx


"""
各モニターに同じだけのワークスペースを割り当て、モニターを跨いでのfocusとmoveを許可しない
これはxmonadのworkspaceの挙動を再現
ex):
    monitor1 = [ws0, ws1]
    monitor2 = [ws2, ws3]
    if focus == monitor1:
        allow cycle focus and move between ws0 and ws1. (in monitor1)
    else:
        allow cycle focus and move between ws2 and ws3. (in monitor2)
"""
@lazy.function
def focus_previous_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)

    previous_group = group.get_previous_group(skip_empty=True)
    previous_group_index = qtile.groups.index(previous_group)

    idx = qtile.current_screen.index
    min_idx, max_idx = calc_range_idx(idx)
    check = check_screen(previous_group_index, min_idx, max_idx)

    if previous_group_index < group_index and check:
        qtile.current_screen.set_group(previous_group)


@lazy.function
def focus_next_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)

    next_group = group.get_next_group(skip_empty=True)
    next_group_index = qtile.groups.index(next_group)

    idx = qtile.current_screen.index
    min_idx, max_idx = calc_range_idx(idx)
    check = check_screen(next_group_index, min_idx, max_idx)

    if next_group_index > group_index and check:
        qtile.current_screen.set_group(next_group)


@lazy.function
def window_to_previous_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)

    previous_group = group.get_previous_group(skip_empty=False)
    previous_group_index = qtile.groups.index(previous_group)

    idx = qtile.current_screen.index
    min_idx, max_idx = calc_range_idx(idx)
    check = check_screen(previous_group_index, min_idx, max_idx)

    if previous_group_index < group_index and check:
        qtile.current_window.togroup(previous_group.name, switch_group=True)


@lazy.function
def window_to_next_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)

    next_group = group.get_next_group(skip_empty=False)
    next_group_index = qtile.groups.index(next_group)

    idx = qtile.current_screen.index
    min_idx, max_idx = calc_range_idx(idx)
    check = check_screen(next_group_index, min_idx, max_idx)
    if next_group_index > group_index and check:
        qtile.current_window.togroup(next_group.name, switch_group=True)


@lazy.function
def focus_n_screen_group(qtile, idx):
    groups = qtile.groups
    s_idx = qtile.current_screen.index
    if idx < GROUP_PER_SCREEN:
        qtile.current_screen.set_group(groups[int(idx + GROUP_PER_SCREEN*s_idx)])


@lazy.function
def move_n_screen_group(qtile, idx):
    groups = qtile.groups
    s_idx = qtile.current_screen.index
    if idx < GROUP_PER_SCREEN:
        qtile.current_window.togroup(groups[int(idx + GROUP_PER_SCREEN*s_idx)].name, switch_group=True)


@lazy.function
def focus_cycle_screen(qtile, backward=False):
    n_screen = len(qtile.screens)
    idx = qtile.current_screen.index
    if backward:
        to_idx = n_screen - 1 if idx == 0 else idx - 1
    else:
        to_idx = 0 if idx + 1 == n_screen else idx + 1
    qtile.cmd_to_screen(to_idx)


@lazy.function
def move_cycle_screen(qtile, backward=False):
    n_screen = len(qtile.screens)
    idx = qtile.current_screen.index
    if backward:
        to_idx = n_screen - 1 if idx == 0 else idx - 1
        to_group = qtile.groups.index(qtile.current_screen.group)-GROUP_PER_SCREEN
        to_group = to_group if to_group > 0 else (GROUP_PER_SCREEN*PARAM.num_screen) - to_group

    else:
        to_idx = 0 if idx + 1 == n_screen else idx + 1
        to_group = qtile.groups.index(qtile.current_screen.group)+GROUP_PER_SCREEN
        to_group = to_group if to_group < GROUP_PER_SCREEN else to_group - (GROUP_PER_SCREEN*PARAM.num_screen)
    group = qtile.groups[to_group]
    qtile.current_window.togroup(group.name)
    qtile.cmd_to_screen(to_idx)
    qtile.current_screen.set_group(group)


@lazy.function
def attach_screen(qtile, pos):
    if PARAM.laptop:
        if pos=='delete':
            subprocess.run('xrandr --output HDMI-A-0 --off', shell=True)
            subprocess.run('feh --bg-fill {}'.format(PARAM.home.joinpath('Pictures', 'wallpapers', 'main01.jpg')), shell=True)
        else:
            subprocess.run('xrandr --output edp --auto --output hdmi-a-0 --auto --{} edp'.format(pos), shell=True)
            subprocess.run('feh --bg-fill {} --bg-fill {}'.format(PARAM.home.joinpath('Pictures', 'wallpapers', 'main01.jpg'),
                                                                  PARAM.home.joinpath('Pictures', 'wallpapers', 'main02.jpg')), shell=True)
        global monitor_pos
        monitor_pos = '{}'.format(pos)


@lazy.function
def capture_screen(qtile, is_clipboard=False):
    idx = qtile.current_screen.index
    if is_clipboard:
        Qtile.cmd_spawn(qtile, 'flameshot screen -n {} -c'.format(idx))
    else:
        Qtile.cmd_spawn(qtile, 'flameshot screen -n {} -p {}'.format(idx, PARAM.capture_path))

