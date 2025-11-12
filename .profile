
export QT_QPA_PLATFORM=xcb
export XLIB_SKIP_ARGB_VISUALS=1             # Fix for FreeCAD invisible window
export WEBKIT_DISABLE_COMPOSITING_MODE=1    # Fix for OrcaSlicer windows not appearing properly
export WAYLAND_DISPLAY=wayland-0
#export $(dbus-launch)

# .net
export DOTNET_ROOT=/snap/dotnet-sdk/current
