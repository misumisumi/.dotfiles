#! /bin/sh
PLUG="HDMI-A-0"
num_line=$(xrandr | grep $PLUG -n | awk -F ':' '{print $1}')
size=$(xrandr | head -n $((2+1)) | tail -n1 | awk -F'    ' '{print $1}')
echo $size
