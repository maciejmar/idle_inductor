import time
import pyautogui
import pynput
import tkinter as tk

idle_time = 0
last_activity = time.time()
reset_interval = 180
reset_drag_pixels = 5
window_duration = 2000  # 2 seconds in milliseconds

def on_move(x, y):
    global last_activity
    last_activity = time.time()

def on_click(x, y, button, pressed):
    global last_activity
    last_activity = time.time()

def on_scroll(x, y, dx, dy):
    global last_activity
    last_activity = time.time()

def on_press(key):
    global last_activity
    last_activity = time.time()

def on_release(key):
    global last_activity
    last_activity = time.time()

mouse_listener = pynput.mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

def show_temporary_window():
    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations
    label = tk.Label(root, text="Idle state reset successfully!", padx=20, pady=10)
    label.pack()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"+{x}+{y}") #place window in center of the screen
    root.after(window_duration, root.destroy)  # Destroy after 2 seconds
    root.mainloop()

try:
    while True:
        current_time = time.time()
        idle_time = current_time - last_activity

        if idle_time >= reset_interval:
            try:
                current_mouse_x, current_mouse_y = pyautogui.position()
                pyautogui.dragTo(current_mouse_x + reset_drag_pixels, current_mouse_y, duration=0.1)
                last_activity = time.time()
                print("Idle reset triggered.")
                show_temporary_window()

            except pyautogui.FailSafeException:
                print("Fail-safe triggered. Mouse reset skipped.")
            except Exception as e:
                print(f"An error occurred during reset: {e}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Script interrupted by user.")
finally:
    mouse_listener.stop()
    keyboard_listener.stop()