export LANG=ja_JP.UTF-8
xrandr --setprovideroutputsource modesetting NVIDIA-1
xrandr --auto
exec dbus-launch qtile


