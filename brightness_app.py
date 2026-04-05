import screen_brightness_control as sbc
import wmi
import pythoncom
import time
import sys
import threading
import pystray
from PIL import Image, ImageDraw
import os

TARGET_DISPLAY = "HP E23 G4"
# Change this value to dim the external monitor further (e.g., 10 or 20).
BRIGHTNESS_OFFSET = 15

# Global flag to stop the thread
stop_event = threading.Event()

def get_external_display():
    """Find the specific HP external monitor."""
    monitors = sbc.list_monitors()
    if not monitors:
        return None
    
    for m in monitors:
        if "HP" in m.upper() and "E23" in m.upper():
            return m
    
    for m in monitors:
        if "HP" in m.upper():
            return m
    
    return monitors[0] if len(monitors) > 1 else None

def sync_brightness(new_brightness):
    """Update the external monitor with an offset."""
    ext = get_external_display()
    if not ext:
        return
    
    try:
        adjusted_brightness = max(0, min(100, new_brightness - BRIGHTNESS_OFFSET))
        if new_brightness == 0:
            adjusted_brightness = 0
            
        sbc.set_brightness(adjusted_brightness, display=ext)
    except Exception as e:
        print(f"Sync error: {e}")

def monitor_loop():
    """WMI brightness listener thread."""
    pythoncom.CoInitialize()
    try:
        c = wmi.WMI(namespace='root/wmi')
        watcher = c.WmiMonitorBrightnessEvent.watch_for()
        
        # Initial sync
        try:
            initial = sbc.get_brightness(display=0)
            if isinstance(initial, list): initial = initial[0]
            sync_brightness(initial)
        except:
            pass

        while not stop_event.is_set():
            try:
                # Use a timeout so we can check the exit event
                event = watcher(timeout_ms=1000)
                if event:
                    new_val = event.Brightness
                    sync_brightness(new_val)
            except Exception:
                time.sleep(1)
    finally:
        pythoncom.CoUninitialize()

def create_image():
    """Create a simple icon for the system tray."""
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(30, 30, 30))
    d = ImageDraw.Draw(image)
    # Draw a simple sun or 'HP' logo
    d.ellipse([16, 16, 48, 48], fill=(255, 200, 0)) # Yellow circle
    return image

def on_quit(icon, item):
    stop_event.set()
    icon.stop()

def run_tray():
    icon = pystray.Icon("HP Brightness Sync")
    icon.icon = create_image()
    icon.title = "HP Brightness Sync"
    icon.menu = pystray.Menu(
        pystray.MenuItem("Quit", on_quit)
    )
    
    # Start the monitoring thread
    t = threading.Thread(target=monitor_loop, daemon=True)
    t.start()
    
    icon.run()

if __name__ == "__main__":
    run_tray()
