import ctypes
from ctypes import wintypes
import time

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_SYSKEYDOWN = 0x0104

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
            print(f"Key Pressed: VK={struct.vkCode}, ScanCode={struct.scanCode}, Flags={struct.flags}")
            
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
pointer = CMPFUNC(low_level_handler)

hook = user32.SetWindowsHookExW(WH_KEYBOARD_LL, pointer, kernel32.GetModuleHandleW(None), 0)

if not hook:
    print("Failed to set hook! Try running as Administrator.")
    exit(1)

print("Low-Level Keyboard Hook active.")
print("Press keys (and FN combinations) to see raw Windows events.")
print("Close this window to stop.")

try:
    msg = wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))
except KeyboardInterrupt:
    pass
finally:
    user32.UnhookWindowsHookEx(hook)
