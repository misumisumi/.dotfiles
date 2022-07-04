"""layout"""
from libqtile import layout
from libqtile.config import Match

from my_modules.param import PARAM

from libqtile.log_utils import logger


_settings = {'border_width': PARAM.border,
             'border_focus': PARAM.c_normal['cyan'],
             'border_normal': PARAM.c_normal['BGbase']}
# for default
layout1 = [
    layout.Columns(**_settings,
                   border_focus_stack=PARAM.c_normal['cyan'],
                   border_normal_stack=PARAM.c_normal['BGbase'],
                   border_on_single=True, fair=False,
                   num_columns=2, insert_position=1,
                   margin=PARAM.margin, margin_on_single=PARAM.margin,
                   split=False),
]
# For code
layout2 = [
    layout.MonadWide(**_settings,
                     ratio=0.6,
                     new_client_position='bottom',
                     single_border_width=PARAM.border,
                     margin=PARAM.margin, single_margin=PARAM.margin
                     ),
        ]
# For full
layout3 = [
    layout.TreeTab(active_bg=PARAM.c_bright['bblack'],
                   bg_color=PARAM.c_normal['BGbase'],
                   font=PARAM.font,
                   sections=['WS{}'.format(i) for i in range(1, 6)],
                   level_shift=20,
                   fontsize=PARAM.font_size-4,
                   section_fontsize=PARAM.font_size-2,
                   ),
    ]
# For media
layout4 = [
    layout.Slice(match=Match(wm_class='pavucontrol'), width=PARAM.slice_width, side='bottom',
                 fallback=layout1[0]),
    ]

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules, # アスペクト比固定のものでもタイリングさせる
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], **_settings)
