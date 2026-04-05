from pynput import keyboard
import sys

print("--- Pynput Key Monitor ---")
print("Press any key or FN combinations to see what Windows receives.")
print("Press ESC or Ctrl+C to exit.")

def on_press(key):
    try:
        print(f'Alphanumeric key pressed: {key.char}')
    except AttributeError:
        print(f'Special key pressed: {key}')

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
