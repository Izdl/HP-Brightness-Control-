import keyboard
import time

print("Listening for key events... Press the FN combinations you mentioned.")
print("Press ESC to exit.")

def on_key_event(event):
    if event.name != 'esc':
        print(f"Key name: {event.name}, Scan code: {event.scan_code}, Event type: {event.event_type}")

keyboard.hook(on_key_event)
keyboard.wait('esc')
