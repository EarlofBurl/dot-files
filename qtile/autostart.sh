#!/bin/sh

xrandr --output HDMI-0 --off --output DP-0 --off --output DP-1 --mode 1920x1080 --pos 3000x0 --rotate normal --output DP-2 --off --output DP-3 --primary --mode 1920x1080 --pos 1080x0 --rotate normal --output DP-4 --off --output DP-5 --mode 1920x1080 --pos 0x0 --rotate left
nm-applet &
dunst &
playerctl &
blueman-applet &
pasystray &
picom &
flameshot &
clipmenud &
nextcloud &
protonmail-bridge &
kdeconnect-indicator &
nitrogen --restore &
mpris-scrobbler &
