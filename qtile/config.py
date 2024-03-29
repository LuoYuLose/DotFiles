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
    Key([mod], "c", lazy.layout.next(), desc="Move window focus to other window"),
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
    # Key(
    #     [mod, "shift"],
    #     "Return",
    #     lazy.layout.toggle_split(),
    #     desc="Toggle between split and unsplit sides of stack",
    # ),
    Key([mod], "Return", lazy.spawn(terminal)),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "Space", lazy.window.toggle_floating()),
    # 禁用热重载，避免bar出现问题
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # 程序启动配置
    Key([mod], "F1", lazy.spawn("firefox")),
    Key([mod], "r", lazy.spawn("rofi -show drun")),
    Key([mod], "m", lazy.spawn("/opt/YesPlayMusic/yesplaymusic")),
    Key([mod, "Shift"], "m", lazy.spawn("qqmusic")),
    Key([mod, "Shift"], "Return", lazy.spawn("nautilus")),
    Key(["mod1"], "c", lazy.spawn("/home/luoyu/WallPapers/LaunchVideoWallpaper.sh")),
    Key(["mod1"], "l", lazy.spawn("i3lockblur")),
    Key([], "Print", lazy.spawn("flameshot gui")),

    # 音频控制
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +10%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%")),

    # 亮度控制
    Key([], "XF86MonBrightnessUp", lazy.spawn("light -A 10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("light -U 5")),
]

groups = [Group(i) for i in "12345"]

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
    # layout.Columns(
    #     border_focus_stack=["#d75f5f", "#8f3d3d"], 
    #     border_width=3,
    #     margin = 10,
    # ),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(
        # border_focus_stack=["#d75f5f", "#8f3d3d"], 
        border_focus_stack=["#00ffff"], 
        border_width=1,
        margin = 8,
    ),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

# Bar
widget_defaults = dict(
    font="MesloLGS Nerd Font",
    fontsize=18,
    padding=6,
    background = "#fff0f5cc",
    foreground = "000000",
)
extension_defaults = widget_defaults.copy()

sep = widget.Sep(
    foreground="2E3440",
    padding=1,
    linewidth=3,
    size_percent=55,
)

screens = [
    Screen(
        top=bar.Bar(
             [
                # widget.CurrentLayout(),
                widget.GroupBox(
                    background="#add8e6cc",
                    foreground="7FFFD4",
                    highlight_method='block',
                    active = "ff1493",
                ),
                sep,
                widget.Prompt(
                    foreground = "2E3440",
                ),
                widget.WindowName(
                    background="#00fa9acc",
                    empty_group_string = "虚空",
                ),
                sep,
                widget.CPUGraph(
                    background = "#f08080cc",
                    border_color = "#f08080",
                ),
                widget.CPU(
                    background = "#f08080cc",
                    format = "CPU {freq_current}GHz {load_percent}%",
                ),
                sep,
                widget.MemoryGraph(
                    background = "#ffdeadcc",
                    border_color = "#ffdead",
                ),
                widget.Memory(
                    background = "#ffdeadcc",
                    measure_mem = "G",
                    format = "Mem {MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}",
                ),
                # widget.Chord(
                #     chords_colors={
                #         "launch": ("#ffc0cb", "#ffffff"),
                #     },
                #     name_transform=lambda name: name.upper(),
                # ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                sep,
                widget.Clock(
                    format="%Y-%m-%d %a %I:%M %p",
                    background = "#e6e6facc",
                ),
                sep,
                widget.Systray(
                    background = "#ffd700cc",
                ),
                # widget.QuickExit(),
             ],
             24,
             border_width=[4, 2, 2, 0],  # Draw top and bottom borders
             border_color = "#FDF5E6",
             # background="#f8f8ff",
             # border_color="#faebd7",
             # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
         ),
    ),
]
 

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
        Match(wm_class="yesplaymusic"),
        Match(wm_class="steam"),
        Match(wm_class="qqmusic"),
        Match(wm_class="QQ"),
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
