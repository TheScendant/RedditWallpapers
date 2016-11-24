#!/bin/bash

# TODO: At night only dark wallpapers.

# Wallpaper's directory.
dir="${HOME}/Wallpapers/Images"
# export DBUS_SESSION_BUS_ADDRESS environment variable
PID=$(pgrep gnome-session)
export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-)

# Random wallpaper.
wallpaper=`find "${dir}" -type f | shuf -n1`
echo  $wallpaper > ${HOME}/Wallpapers/currBG
# Change wallpaper.
# http://bit.ly/HYEU9H
gsettings set org.gnome.desktop.background picture-options "spanned"
gsettings set org.gnome.desktop.background picture-uri "file://${wallpaper}"
