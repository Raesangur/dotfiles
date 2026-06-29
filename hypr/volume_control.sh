evsieve --input /dev/input/event7 --hook key:volumeup   exec-shell="pactl set-sink-volume @DEFAULT_SINK@ +5%" & \
evsieve --input /dev/input/event7 --hook key:volumedown exec-shell="pactl set-sink-volume @DEFAULT_SINK@ -5%"
