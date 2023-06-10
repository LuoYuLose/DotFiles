# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook, qtile, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess
import os

# 自启动
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    if qtile.core.name == "x11":
        subprocess.Popen([home + '/.config/qtile/scripts/autostart-x11.sh'])
    elif qtile.core.name =="wayland":
        subprocess.Popen([home + '/.config/qtile/scripts/autostart-wayland.sh'])

mod = "mod4"
# terminal = guess_terminal()
terminal = "kitty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    # 禁用热重载，避免bar出现问题
    # Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # 程序启动配置
    Key([mod], "F1", lazy.spawn("firefox"), desc="火狐浏览器"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Rofi程序启动器"),
    Key([mod], "m", lazy.spawn("/opt/YesPlayMusic/yesplaymusic"), desc="网易云三方音乐播放器"),
    Key([mod, "Shift"], "m", lazy.spawn("qqmusic"), desc="QQ音乐"),

    # 音频控制
    Key([ ], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([ ], "XF86AudioStop", lazy.spawn("playerctl stop")),
    Key([ ], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([ ], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([ ], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +10%")),
    Key([ ], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%")),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

# Bar
# # DEFAULT WIDGET SETTINGS
# BLACK = '#29414f'
# RED = '#ec5f67'
# GREEN = '#99c794'
# YELLOW = '#fac863'
# BLUE = '#6699cc'
# MAGENTA = '#c594c5'
# CYAN = '#5fb3b3'
# WHITE = '#ffffff'
# 
# widget_defaults = dict(
#     font="Source Code Pro",
#     fontsize=18,
#     padding=2,
#     background=BLACK
# )
# extension_defaults = widget_defaults.copy()
# 
# # WIDGETS
# def init_xmenu():
#     return widget.TextBox(
#         text="",
#         foreground=WHITE,
#         background=BLACK,
#         fontsize=32,
#         padding=8,
#         mouse_callbacks={
#             'Button1': lambda: qtile.cmd_spawn([
#                 '/bin/bash', os.path.expanduser(os.path.join(
#                     '~', 'scripts', 'xmenu.sh'))
#             ])
#         }
#     )
# 
# 
# def init_group_box():
#     return widget.GroupBox(
#         fontsize=26,
#         spacing=5,
#         disable_drag=True,
#         active=WHITE,
#         inactive=WHITE,
#         rounded=False,
#         highlight_method="block",
#         this_current_screen_border=GREEN,
#         this_screen_border=CYAN,
#         other_current_screen_border=BLACK,
#         other_screen_border=BLACK,
#         foreground=WHITE,
#         background=BLACK,
#         margin_x=6,
#         margin_y=3,
#         padding_x=4,
#         padding_y=7,
#     )
# 
# 
# def init_check_updates():
#     return widget.CheckUpdates(
#         execute=' '.join(["kitty", '-e', 'paru']),
#         distro='Arch_yay',
#         display_format=' Updates: {updates}',
#         update_interval=1800,
#         foreground=WHITE,
#         background=CYAN,
#         padding=5
#     )
# 
# 
# def init_bitcoin_ticker():
#     return widget.BitcoinTicker(
#         # currency='USD',
#         fmt=" {}",
#         foreground=WHITE,
#         background=GREEN,
#         padding=5
#     )
# 
# 
# def init_thermal_sensor():
#     return widget.ThermalSensor(
#         fmt=' {}',
#         tag_sensor="Package id 0",
#         foreground=WHITE,
#         background=CYAN,
#         padding=5
#     )
# 
# 
# def init_volume():
#     return widget.Volume(
#         fmt=" {}",
#         foreground=WHITE,
#         background=GREEN,
#         padding=5
#     )
# 
# 
# def init_current_layout_icon():
#     return widget.CurrentLayoutIcon(
#         custom_icon_paths=[os.path.expanduser(
#             "$HOME/.config/qtile/icons")],
#         foreground=WHITE,
#         background=CYAN,
#         scale=0.6
#     )
# 
# 
# def init_curren_layout():
#     return widget.CurrentLayout(
#         foreground=WHITE,
#         background=CYAN,
#         padding=5
#     )
# 
# 
# def init_clock():
#     return widget.Clock(
#         fmt=" {}",
#         foreground=WHITE,
#         background=GREEN,
#         padding=5,
#         format="%A, %d %B [ %H:%M ]"
#     )
# 
# 
# def init_wide_bar(tray=True):
#     return [
#         init_xmenu(),
#         init_group_box(),
#         widget.TaskList(),
#         widget.Systray(
#             background=BLACK,
#             padding=5
#         ) if tray else widget.Sep(linewidth=0),
#         widget.Sep(
#             linewidth=0,
#             padding=5,
#             background=BLACK
#         ),
#         init_check_updates(),
#         init_bitcoin_ticker(),
#         init_thermal_sensor(),
#         init_volume(),
#         init_current_layout_icon(),
#         init_curren_layout(),
#         init_clock(),
#         widget.Sep(
#             linewidth=0,
#             padding=5,
#             background=GREEN
#         )
#     ]
# 
# 
# def init_short_bar():
#     return [
#         init_group_box(),
#         widget.TaskList(),
#         init_current_layout_icon(),
#         init_curren_layout(),
#         init_clock(),
#         widget.Sep(
#             linewidth=0,
#             padding=5,
#             background=GREEN
#         )
#     ]
# 
# 
# bar_list = (
#     init_wide_bar(),
#     init_wide_bar(tray=False),
#     init_short_bar(),
# )
# 
# if __name__ in ["config", "__main__"]:
#     screens = [
#         Screen(top=bar.Bar(
#             widgets=widgets, opacity=1, size=30, margin=[8, 8, 0, 8],
#         )) for widgets in bar_list
#     ]
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox("default config", name="default"),
                widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]
 
widget_defaults = dict(
    font="Source Code Pro",
    fontsize=18,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
