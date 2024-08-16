# -*- coding: utf-8 -*-
import os
import re
import socket
import asyncio
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, ScratchPad, DropDown, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile.command.base import expose_command
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal, _send_dbus_message
from typing import List  # noqa: F401from typing import List  # noqa: F401

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.popup.toolkit import PopupRelativeLayout, PopupText, PopupWidget
from qtile_extras.popup.templates.mpris2 import COMPACT_LAYOUT, DEFAULT_LAYOUT
from qtile_extras.widget.mixins import ExtendedPopupMixin       

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
alt = "mod1"
myTerm = "kitty"      # My terminal of choice
myBrowser = "firefox" # My browser of choice


keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod], "b",
             lazy.spawn(myBrowser),
             desc='firefox'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod], "x",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "a",
             lazy.reload_config(),
             desc='Reload config Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key([], "Print",
             lazy.spawn("flameshot gui"),
             desc='flameshot screenshot'
             ),
         Key([mod, "control"], "h",
             lazy.spawn("dunstctl history-pop"),
             desc='show dunst history'
             ),
         Key([mod], "l",
             lazy.spawn("powermenu.sh"),
             desc='show powermenu'
             ), 
         ### Programs
         #### Keychords
         KeyChord([mod], "i", [ 
                  Key([], "d", lazy.spawn("nautilus -w")),
                  Key([], "e", lazy.spawn("gnome-text-editor")),
                  Key([], "n", lazy.spawn("flatpak run --env=GTK_THEME=Adwaita-dark io.gitlab.news_flash.NewsFlash")),
                  Key([], "f", lazy.spawn("ferdium")),
                  Key([], "t", lazy.spawn("thunderbird")),
                  Key([], "a", lazy.spawn("/home/manuel/firefox_nightly/firefox")),
                  Key([], "v", lazy.spawn("vivaldi")),
                  Key([], "c", lazy.spawn("chromium-browser")),
                  Key([], "g", lazy.spawn("google-chrome-stable")),
                  Key([], "s", lazy.spawn("steam"))
             ]),
         #### Normal spawns
         Key([mod, "control"], "f",
             lazy.spawn("thunar"),
             desc="File manager"
             ),
         ### rofi
         Key([mod, "control"], "m",
             lazy.spawn("rofi  -show find -modi find:~/.local/share/rofi/finder.sh"),
             desc='file search'
             ),
         Key([mod, "control"], "Return",
             lazy.spawn("rofi -show run"),
             desc='Run Launcher'
             ),
         Key([mod], "space",
             lazy.spawn("rofi -show drun"),
             desc='Run Launcher with .desktop apps'
             ),
         Key([mod, "control"], "Tab",
             lazy.spawn("rofi -show window"),
             desc='Window-Control All'
             ),
         Key([mod, "control"], "u",
             lazy.spawn("rofi -show windowcd"),
             desc='Window Control current'
             ),
         Key([mod, "control"], "t",
             lazy.spawn("rofi -show calc"),
             desc='Calculator'
             ),
         Key([mod, "control"], "l",
             lazy.spawn("rofi -show filebrowser"),
             desc='filebrowser'
             ),
         Key([mod, "control"], "e",
             lazy.spawn("rofi -show emoji"),
             desc='emoji'
             ),
         Key([mod, "control"], "r",
             lazy.spawn("rofi -show"),
             desc='rofi base'
             ),
         Key([mod, "control"], "c",
             lazy.spawn("clipmenu"),
             desc='Clipboard Menu'
             ),
         ### Switch focus to specific monitor (out of three)
         Key([mod], "c",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "e",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         ## Switch focus of monitors
         Key([mod, "shift"], "d",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod, "shift"], "n",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Window controls
         Key([mod], "n",
             lazy.layout.left(),
             desc='Move focus left in current stack pane'
             ),
         Key([mod], "d",
             lazy.layout.right(),
             desc='Move focus right in current stack pane'
             ),
         Key([mod], "r",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "t",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "r",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "t",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod, "mod1"],  "r",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod, "mod1"], "t",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod, "mod1"], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod, "mod1"], "d",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key(["mod1"], "Return",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
          Key([mod, "control"], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "shift"], "space",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
         ### Media Controls
         Key([], "XF86AudioPrev", 
                 lazy.spawn("playerctl previous"), 
                 desc="next song"),
         Key([], "XF86AudioNext", 
                 lazy.spawn("playerctl next"), 
                 desc="next song"),
         Key([], "XF86AudioLowerVolume", 
                 lazy.spawn("amixer sset Master 2%-"), 
                 desc="Lower Volume by 2%"),
         Key([], "XF86AudioRaiseVolume", 
                 lazy.spawn("amixer sset Master 2%+"), 
                 desc="Raise Volume by 2%"),
                 
         Key([], "XF86AudioMute", 
                 lazy.spawn("amixer sset Master 1+ toggle"), 
                 desc="Mute/Unmute Volume"),
         Key([], "XF86AudioPlay", 
                 lazy.spawn("playerctl play-pause"), 
                 desc="Play/Pause player")
]

groups = [Group("", layout='monadtall', matches=[Match(wm_class="firefox")]),
          Group("", layout='floating', matches=[Match(wm_class="Vivaldi-stable")]), 
          Group("", layout='ratiotile', matches=[Match(wm_class="ferdium")]),
          Group("", layout='monadtall'),
          Group("", layout='monadtall', matches=[Match(wm_class="thunderbird")]),
          Group("", layout='monadtall', matches=[Match(wm_class="Steam")]),
          Group("", layout='monadtall'),
          Group("", layout='monadtall'),
          Group("󰱾", layout='monadtall'),
          Group("󰖟", layout='monadtall')]

#define group scratchpads
groups.append(ScratchPad("scratchpad", [
    DropDown("term", "kitty", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    DropDown("ranger", "kitty -e ranger", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    DropDown("volume", "kitty -e pulsemixer", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    DropDown("mus", "kitty -e ncspot", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    DropDown("htop", "kitty -e htop", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),

]))

# Scratchpad keybindings
keys.extend([
    Key([mod], "m", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod], "h", lazy.group['scratchpad'].dropdown_toggle('ranger')),
    Key([mod], "g", lazy.group['scratchpad'].dropdown_toggle('volume')),
    Key([mod], "s", lazy.group['scratchpad'].dropdown_toggle('mus')),
    Key([mod], "f", lazy.group['scratchpad'].dropdown_toggle('htop')),
])



@hook.subscribe.client_new
async def move_spotify(client):
        await asyncio.sleep(0.01)
        if client.name == 'Spotify': client.togroup('')
        elif client.name == 'Discord': client.togroup('')
        elif client.name == 'Signal': client.togroup('')
        elif client.name == 'Firefox': client.togroup('')

@hook.subscribe.client_new
def float_firefox(window):
    wm_class = window.window.get_wm_class()
    if wm_class == ("Places", "firefox"):
        window.floating = True

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {"border_width": 2,
                "margin": 7,
                "border_focus": "#fbf1c7",
                "border_normal": "#282828"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.Bsp(**layout_theme),
    #layout.TreeTab(
    #     font = "ShareTechMono",
    #     fontsize = 10,
    #     sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
    #     section_fontsize = 10,
    #     border_width = 2,
    #     bg_color = "1c1f24",
    #     active_bg = "c678dd",
    #     active_fg = "000000",
    #     inactive_bg = "a9a1e1",
    #     inactive_fg = "1c1f24",
    #     padding_left = 0,
    #     padding_x = 0,
    #     padding_y = 5,
    #     section_top = 10,
    #     section_bottom = 20,
    #     level_shift = 8,
    #     vspace = 3,
    #     panel_width = 200
    #     ),
    layout.Floating(**layout_theme)
]

colors = [["#282828", "#282828"], #0 Gruv bg
          ["#458588", "#458588"], #1 Gruv Blue
          ["#ebdbb2", "#ebdbb2"], #2 Gruv fg
          ["#fabd2f", "#fabd2f"], #3 Gruv yellow
          ["#fb4934", "#fb4934"], #4 Gruv red
          ["#b8bb26", "#b8bb26"], #5 Gruv green
          ["#fe8019", "#fe8019"], #6 Gruv Orange
          ["#928374", "#928374"], #7 Gruv gray
          ["#8ec07c", "#8ec07c"], #8 Gruv aqua
          ["#b16286", "#b16286"]] #9 Gruv Purple

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

decoration_group = {
    "decorations": [
        RectDecoration(colour="#6768d4", radius=10, filled=True, padding_y=0, group=True)
    ],
    "padding": 16,
}

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Nerd Font",
    fontsize = 15,
    padding = 4,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = "#00000000"
                       ),
             widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[0],
                       background = "#00000000",
                       #padding = 6,
                       #borderwith = 3,
                       scale = 0.7,
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = "#00000000"
                       ),            
              widget.Sep(
                       linewidth = 0,
                       foreground = colors[2],
                       background = "#00000000",
                       **decoration_group
                       ),    
              widget.GroupBox(
                       font = "Ubuntu Nerd Font",
                       fontsize = 16,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 7,
                       active = "#eaeaea",
                       inactive = "#b7b7ce",
                       rounded = True,
                       highlight_color = colors[1],
                       highlight_method = "block",
                       this_current_screen_border = "#c3c4dc",
                       this_screen_border = "#c3c4dc",
                       other_current_screen_border = colors[7],
                       other_screen_border = colors[7],
                       foreground = colors[2],
                       #highlight_color="#00000000",
                       background = "#00000000",
                       **decoration_group
                       ),
             widget.Sep(
                       linewidth = 0,
                       foreground = colors[2],
                       background = "#00000000",
                       **decoration_group
                       ),      
             widget.WindowName(
                       foreground = colors[0],
                       background = "#00000000",
                       padding = 6
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = "#00000000"
                       ),        
             widget.Mpris2(
                      popup_layout=COMPACT_LAYOUT,
                      mouse_callbacks = {"Button3": lazy.toggle_player()},
                      background = "#00000000",
                      foreground = colors[0],
                      name='spotify',
                      fmt = " {}",
                      objname=None,
                      display_metadata=['xesam:title', 'xesam:artist'],
                      scroll_chars=None,
                      max_chars=45
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = "#00000000"
                       ),
              widget.Sep(
                       linewidth = 0,
                       foreground = colors[2],
                       background = "#00000000",
                       **decoration_group
                       ),             
              widget.Clock(
                       foreground = "#eaeaea",
                       background = "#00000000",
                       format = "  %a, %d. %b  %H:%M Uhr",
                       **decoration_group
                       ),
             widget.Sep(
                       linewidth = 0,
                       foreground = colors[2],
                       background = "#00000000",
                       **decoration_group
                       ),               
             widget.Sep(
                       linewidth = 0,
                       padding = 12,
                       foreground = colors[2],
                       background = "#00000000"
                       ),                        
             widget.Sep(
                       linewidth = 0,
                       foreground = colors[2],
                       background = "#00000000",
                       **decoration_group
                       ),        
             widget.KeyboardLayout(
                       foreground = "#eaeaea",
                       fmt = '  {}',
                       configured_keyboards=['de neo','de','us'],
                       **decoration_group
                       ),       
             widget.Sep(
                       linewidth = 0,
                       foreground = colors[2],
                       background = "#00000000",
                       **decoration_group
                       ),          
             widget.Systray(
                       linewidth = 0,
                       foreground = colors[2],
                       background = "#00000000",
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = "#00000000"
                       )        
                         ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1                 # Alle Widgets auf Monitor 1, DP1, BenQ

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[13:20]              # Vertikaler Monitor 
    return widgets_screen2                 

def init_widgets_screen3():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[13:20]              # Sys-Tray wird von Monitor 2, DP3, Acer entfernt 
    return widgets_screen2  

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), background="#00000000", opacity=1, size=34, margin=6)),
            Screen(top=bar.Bar(widgets=init_widgets_screen3(), background="#00000000", opacity=1, size=34, margin=6)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", opacity=1, size=34, margin=6))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()
    widgets_screen3 = init_widgets_screen3()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
