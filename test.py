import screen_brightness_control as sbc

try:
    print('All displays:', sbc.list_monitors())
    for monitor in sbc.list_monitors():
        print(f"Brightness for {monitor}: {sbc.get_brightness(display=monitor)}")
except Exception as e:
    print(f"Error: {e}")
