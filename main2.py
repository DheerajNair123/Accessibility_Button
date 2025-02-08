import tkinter as tk
import subprocess
import platform
import pyautogui

# On Windows, we'll use ctypes to send native WM_APPCOMMAND messages.
if platform.system() == "Windows":
    import ctypes

# Variables for dragging behavior
drag_threshold = 5
initial_click_x = 0
initial_click_y = 0
dragging = False

def open_file_manager():
    """Launch the system's file manager silently."""
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.Popen(["explorer", "."])
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", "."])
        else:  # Assume Linux or other Unix-like systems
            subprocess.Popen(["xdg-open", "."])
    except Exception as e:
        print(f"Error launching File Manager: {e}")

def open_chrome():
    """Launch Google Chrome silently."""
    system = platform.system()
    try:
        if system == "Windows":
            # Use a raw string to avoid backslash issues
            subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "Google Chrome"])
        else:  # Linux
            subprocess.Popen(["google-chrome"])
    except Exception as e:
        print(f"Error launching Chrome: {e}")

def go_back():
    """
    Simulate a 'Back' action on the currently active application.
    For Windows, send the WM_APPCOMMAND_BROWSER_BACKWARD command.
    For macOS and Linux, simulate the common hotkey (Command+[ or Alt+Left).
    """
    system = platform.system()
    try:
        if system == "Windows":
            # Get handle for the foreground (active) window.
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            WM_APPCOMMAND = 0x0319
            APPCOMMAND_BROWSER_BACKWARD = 1
            # The command is passed in the high word of lParam.
            ctypes.windll.user32.SendMessageW(hwnd, WM_APPCOMMAND, 0, APPCOMMAND_BROWSER_BACKWARD << 16)
        elif system == "Darwin":
            # Many macOS apps (like Safari or Chrome) use Command+[ for Back.
            pyautogui.hotkey('command', '[')
        else:
            # On Windows (fallback) or Linux, Alt+Left is commonly used.
            pyautogui.hotkey('alt', 'left')
    except Exception as e:
        print(f"Error simulating Back: {e}")

def go_forward():
    """
    Simulate a 'Forward' action on the currently active application.
    For Windows, send the WM_APPCOMMAND_BROWSER_FORWARD command.
    For macOS and Linux, simulate the common hotkey (Command+] or Alt+Right).
    """
    system = platform.system()
    try:
        if system == "Windows":
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            WM_APPCOMMAND = 0x0319
            APPCOMMAND_BROWSER_FORWARD = 2
            ctypes.windll.user32.SendMessageW(hwnd, WM_APPCOMMAND, 0, APPCOMMAND_BROWSER_FORWARD << 16)
        elif system == "Darwin":
            pyautogui.hotkey('command', ']')
        else:
            pyautogui.hotkey('alt', 'right')
    except Exception as e:
        print(f"Error simulating Forward: {e}")

def exit_app():
    """Exit the assistive tool."""
    root.destroy()

def on_press(event):
    """Record the initial position when the canvas is pressed."""
    global initial_click_x, initial_click_y, dragging
    initial_click_x = event.x_root
    initial_click_y = event.y_root
    dragging = False

def on_motion(event):
    """Allow dragging the floating window by moving the canvas."""
    global dragging, initial_click_x, initial_click_y
    dx = event.x_root - initial_click_x
    dy = event.y_root - initial_click_y
    if abs(dx) > drag_threshold or abs(dy) > drag_threshold:
        dragging = True
        new_x = root.winfo_x() + dx
        new_y = root.winfo_y() + dy
        root.geometry(f"+{new_x}+{new_y}")
        # Update positions for smooth dragging.
        initial_click_x = event.x_root
        initial_click_y = event.y_root

def on_release(event):
    """If not dragging, display the context menu."""
    if not dragging:
        context_menu.tk_popup(event.x_root, event.y_root)
    context_menu.grab_release()

# Create a borderless window that stays on top.
root = tk.Tk()
root.overrideredirect(True)         # Remove window decorations.
root.attributes("-topmost", True)   # Keep the window always on top.

# Set a transparent background color.
transparent_color = "orange"
root.attributes("-transparentcolor", transparent_color)

# Make the window slightly translucent for a more seamless feel.
root.attributes("-alpha", 0.85)

# Create a canvas to simulate a circular button with a transparent background.
canvas_size = 80
assistive_canvas = tk.Canvas(root, width=canvas_size, height=canvas_size,
                             highlightthickness=0, bg=transparent_color)
assistive_canvas.pack()

# Draw a grey circle (oval) with a margin.
margin = 5
assistive_canvas.create_oval(margin, margin, canvas_size - margin, canvas_size - margin,
                             fill="grey", outline="grey")

# Optionally, add text inside the circle (e.g., "A" for Assistive).
assistive_canvas.create_text(canvas_size/2, canvas_size/2,
                             text="A", fill="white", font=("Arial", 20, "bold"))

# Bind mouse events for dragging and tapping.
assistive_canvas.bind("<ButtonPress-1>", on_press)
assistive_canvas.bind("<B1-Motion>", on_motion)
assistive_canvas.bind("<ButtonRelease-1>", on_release)

# Create a context menu with all shortcuts.
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Open File Manager", command=open_file_manager)
context_menu.add_command(label="Open Chrome", command=open_chrome)
context_menu.add_separator()
context_menu.add_command(label="Back", command=go_back)
context_menu.add_command(label="Forward", command=go_forward)
context_menu.add_separator()
context_menu.add_command(label="Exit", command=exit_app)

# Position the floating button near the bottom-right of the screen.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
default_x = screen_width - canvas_size - 20  # Adjust as needed.
default_y = screen_height - canvas_size - 20
root.geometry(f"+{default_x}+{default_y}")

root.mainloop()
