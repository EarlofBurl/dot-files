#!/usr/bin/env sh

#terminnate already running bar instances
killall -q polybar

# Wait until the processes have been shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

# Launch bar
polybar bspwm &
polybar bspwm1 &
polybar bspwm2 &
