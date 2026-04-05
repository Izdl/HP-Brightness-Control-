import ctypes
from ctypes import wintypes
import time
import wmi
import threading

# Windows Constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_SYSKEYDOWN = 0x0104

# VK Codes for Brightness (Sometimes used)
VK_BRIGHTNESS_DOWN = 0x81
VK_BRIGHTNESS_UP = 0x80

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]

def low_level_handler(nCode, wParam, lParam):
    if nCode >= 0:
        if wParam in [WM_KEYDOWN, WM_SYSKEYDOWN]:
            struct = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            print(f"[KEY] VK={struct.vkCode} (0x{struct.vkCode:02X}), ScanCode={struct.scanCode}, Flags={struct.flags}")
            if struct.vkCode == VK_BRIGHTNESS_UP:
                print("Detected: VK_BRIGHTNESS_UP")
            if struct.vkCode == VK_BRIGHTNESS_DOWN:
                print("Detected: VK_BRIGHTNESS_DOWN")
            
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

def monitor_wmi_brightness():
    print("Monitoring WMI Brightness changes (Internal Screen)...")
    c = wmi.WMI(namespace='root/wmi')
    watcher = c.watch_for(notification_type="WmiMonitorBrightnessEvent")
    while True:
        try:
            event = watcher()
            print(f"[WMI] Brightness changed to: {event.Brightness}%")
        except Exception as e:
            print(f"WMI Error: {e}")
            break

def start_hook():
    CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
    pointer = CMPFUNC(low_level_handler)
    hook = user32.SetWindowsHookExW(WH_KEYBOARD_LL, pointer, kernel32.GetModuleHandleW(None), 0)
    
    if not hook:
        print("Failed to set hook! Try running as Administrator.")
        return

    print("Listening for Keys and WMI events. Press Ctrl+C to stop.")
    try:
        msg = wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
    except KeyboardInterrupt:
        pass
    finally:
        user32.UnhookWindowsHookEx(hook)

if __name__ == "__main__":
    t = threading.Thread(target=monitor_wmi_brightness, daemon=True)
    t.start()
    start_hook()
