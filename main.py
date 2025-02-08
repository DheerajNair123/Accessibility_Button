# import tkinter as tk
# from tkinter import messagebox
# import subprocess
# import platform
#
# # Variables for dragging behavior
# drag_threshold = 5
# initial_click_x = 0
# initial_click_y = 0
# dragging = False
# current_font_size = 14
#
# def open_file_manager():
#     """Launch the system's file manager."""
#     system = platform.system()
#     try:
#         if system == "Windows":
#             # Opens File Explorer in the current directory
#             subprocess.Popen(["explorer", "."])
#         elif system == "Darwin":  # macOS
#             subprocess.Popen(["open", "."])
#         else:  # Assume Linux or other Unix-like systems
#             subprocess.Popen(["xdg-open", "."])
#         messagebox.showinfo("File Manager", "File Manager opened successfully.")
#     except Exception as e:
#         messagebox.showerror("Error", f"Could not launch File Manager:\n{e}")
#
# def open_chrome():
#     """Launch Google Chrome."""
#     system = platform.system()
#     try:
#         if system == "Windows":
#             # This assumes that Chrome is in your PATH.
#             subprocess.Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe"])
#         elif system == "Darwin":
#             subprocess.Popen(["open", "-a", "Google Chrome"])
#         else:  # Linux
#             # This assumes that 'google-chrome' is installed and in your PATH.
#             subprocess.Popen(["google-chrome"])
#         messagebox.showinfo("Chrome", "Chrome launched successfully.")
#     except Exception as e:
#         messagebox.showerror("Error", f"Could not launch Chrome:\n{e}")
#
# def on_button_press(event):
#     """Record the initial click position for dragging."""
#     global initial_click_x, initial_click_y, dragging
#     initial_click_x = event.x_root
#     initial_click_y = event.y_root
#     dragging = False
#
# def on_button_motion(event):
#     """Allow dragging the floating button around the screen."""
#     global dragging, initial_click_x, initial_click_y
#     dx = event.x_root - initial_click_x
#     dy = event.y_root - initial_click_y
#     if abs(dx) > drag_threshold or abs(dy) > drag_threshold:
#         dragging = True
#         new_x = root.winfo_x() + dx
#         new_y = root.winfo_y() + dy
#         root.geometry(f"+{new_x}+{new_y}")
#         # Update the initial positions for continuous dragging
#         initial_click_x = event.x_root
#         initial_click_y = event.y_root
#
# def on_button_release(event):
#     """Show the context menu if it was a tap (and not a drag)."""
#     if not dragging:
#         context_menu.tk_popup(event.x_root, event.y_root)
#     context_menu.grab_release()
#
# # Create a borderless window that stays on top
# root = tk.Tk()
# root.overrideredirect(True)  # Remove window decorations
# root.attributes("-topmost", True)  # Keep the window on top
#
# # Create the floating accessibility button
# button = tk.Button(root, text="Assistive", font=("Arial", current_font_size),
#                    relief="raised", bd=2)
# button.pack()
#
# # Bind mouse events for dragging and tapping
# button.bind("<ButtonPress-1>", on_button_press)
# button.bind("<B1-Motion>", on_button_motion)
# button.bind("<ButtonRelease-1>", on_button_release)
#
# # Create a context menu with shortcuts for File Manager and Chrome
# context_menu = tk.Menu(root, tearoff=0)
# context_menu.add_command(label="Open File Manager", command=open_file_manager)
# context_menu.add_command(label="Open Chrome", command=open_chrome)
#
# # Position the floating button near the bottom-right of the screen
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# default_x = screen_width - 100  # Adjust as needed
# default_y = screen_height - 100  # Adjust as needed
# root.geometry(f"+{default_x}+{default_y}")
#
# root.mainloop()

import tkinter as tk
import subprocess
import platform
import pyautogui  # For simulating keystrokes

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
            # Use a raw string to prevent backslash issues
            subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "Google Chrome"])
        else:  # Linux
            subprocess.Popen(["google-chrome"])
    except Exception as e:
        print(f"Error launching Chrome: {e}")

def go_back():
    """Simulate the 'Back' command (e.g., browser back)."""
    system = platform.system()
    try:
        if system == "Darwin":
            # On macOS, many browsers use Command + [ for going back.
            pyautogui.hotkey('command', '[')
        else:
            # On Windows and most Linux desktops, Alt + Left Arrow works.
            pyautogui.hotkey('alt', 'left')
    except Exception as e:
        print(f"Error simulating Back: {e}")

def go_forward():
    """Simulate the 'Forward' command (e.g., browser forward)."""
    system = platform.system()
    try:
        if system == "Darwin":
            # On macOS, many browsers use Command + ] for going forward.
            pyautogui.hotkey('command', ']')
        else:
            # On Windows and Linux, Alt + Right Arrow works.
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
        # Update initial positions for continuous dragging
        initial_click_x = event.x_root
        initial_click_y = event.y_root

def on_release(event):
    """If not dragging, display the context menu."""
    if not dragging:
        context_menu.tk_popup(event.x_root, event.y_root)
    context_menu.grab_release()

# Create a borderless window that stays on top
root = tk.Tk()
root.overrideredirect(True)         # Remove window decorations
root.attributes("-topmost", True)   # Keep the window on top

# Set a transparent background color (choose a color that won't be used elsewhere)
transparent_color = "orange"
root.attributes("-transparentcolor", transparent_color)

# Make the window slightly translucent for a seamless feel
root.attributes("-alpha", 0.85)

# Create a canvas to simulate a circular button with a transparent background
canvas_size = 80
assistive_canvas = tk.Canvas(root, width=canvas_size, height=canvas_size,
                             highlightthickness=0, bg=transparent_color)
assistive_canvas.pack()

# Draw a grey circle (oval) with a margin
margin = 5
assistive_canvas.create_oval(margin, margin, canvas_size - margin, canvas_size - margin,
                             fill="grey", outline="grey")

# Optionally add text inside the circle (e.g., "A" for Assistive)
assistive_canvas.create_text(canvas_size/2, canvas_size/2,
                             text="A", fill="white", font=("Arial", 20, "bold"))

# Bind mouse events for dragging and tapping
assistive_canvas.bind("<ButtonPress-1>", on_press)
assistive_canvas.bind("<B1-Motion>", on_motion)
assistive_canvas.bind("<ButtonRelease-1>", on_release)

# Create a context menu with shortcuts for File Manager, Chrome, Back, Forward, and Exit
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Open File Manager", command=open_file_manager)
context_menu.add_command(label="Open Chrome", command=open_chrome)
context_menu.add_separator()
context_menu.add_command(label="Back", command=go_back)
context_menu.add_command(label="Forward", command=go_forward)
context_menu.add_separator()
context_menu.add_command(label="Exit", command=exit_app)

# Position the floating button near the bottom-right of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
default_x = screen_width - canvas_size - 20  # Adjust margins as needed
default_y = screen_height - canvas_size - 20
root.geometry(f"+{default_x}+{default_y}")

root.mainloop()
