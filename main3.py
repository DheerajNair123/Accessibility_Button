
import tkinter as tk
import subprocess
import platform
import pyautogui
import pygame

# Initialize pygame for sound effects
pygame.mixer.init()

# Variables for dragging behavior
drag_threshold = 5
initial_click_x = 0
initial_click_y = 0
dragging = False

# Function to play sounds
def play_sound(sound):
    """Play a given sound."""
    try:
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error loading sound: {e}")

# Functions to simulate actions
def open_file_manager():
    """Launch the system's file manager silently."""
    # play_sound("ironman_startup.mp3")  # Play action sound
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.Popen(["explorer", "."])
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", "."])
        else:  # Linux and others
            subprocess.Popen(["xdg-open", "."])
    except Exception as e:
        print(f"Error launching File Manager: {e}")

def open_chrome():
    """Launch Google Chrome silently."""
    play_sound("action_sound.mp3")  # Play action sound
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "Google Chrome"])
        else:  # Linux
            subprocess.Popen(["google-chrome"])
    except Exception as e:
        print(f"Error launching Chrome: {e}")

def simulate_back():
    """Simulate Alt+Left for Back navigation."""
    pyautogui.hotkey('alt', 'left')
    root.deiconify()  # Re-show the assistive window after sending the keystroke

def simulate_forward():
    """Simulate Alt+Right for Forward navigation."""
    pyautogui.hotkey('alt', 'right')
    root.deiconify()

def go_back():
    """Hide the assistive tool briefly and simulate the Back command."""
    root.withdraw()  # Hide the assistive window temporarily
    root.after(100, simulate_back)

def go_forward():
    """Hide the assistive tool briefly and simulate the Forward command."""
    root.withdraw()  # Hide the assistive window temporarily
    root.after(100, simulate_forward)

def exit_app():
    """Exit the assistive tool."""
    root.destroy()

# Dragging the window functionality
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
root.attributes("-topmost", True)   # Keep the window on top.

# Set the window to be fully transparent
root.attributes("-transparentcolor", "black")

# Set the transparency level of the window
root.attributes("-alpha", 0.85)  # Slight transparency

# Create a canvas to simulate a circular button with a transparent background.
canvas_size = 100
assistive_canvas = tk.Canvas(root, width=canvas_size, height=canvas_size,
                             highlightthickness=0, bg="black")
assistive_canvas.pack()

# Draw a neon-blue circle (oval) with a margin.
margin = 5
assistive_canvas.create_oval(margin, margin, canvas_size - margin, canvas_size - margin,
                             fill="#00FFFF", outline="#00FFFF")

# Optionally add text inside the circle (e.g., "A" for Assistive).
assistive_canvas.create_text(canvas_size / 2, canvas_size / 2,
                             text="A", fill="black", font=("Arial", 30, "bold"))

# Bind mouse events for dragging and tapping.
assistive_canvas.bind("<ButtonPress-1>", on_press)
assistive_canvas.bind("<B1-Motion>", on_motion)
assistive_canvas.bind("<ButtonRelease-1>", on_release)

# Create a context menu with cool neon hover effects.
context_menu = tk.Menu(root, tearoff=0, bg='black', fg='cyan', activebackground='#333', activeforeground='cyan')

# Add commands without icons
context_menu.add_command(label="Open File Manager", command=open_file_manager)
context_menu.add_command(label="Open Chrome", command=open_chrome)
context_menu.add_separator()
context_menu.add_command(label="Back", command=go_back)
context_menu.add_command(label="Forward", command=go_forward)
context_menu.add_separator()
context_menu.add_command(label="Exit", command=exit_app)

# Neon hover effect: change color when hovered
def on_hover(event):
    event.widget.config(bg="#333", fg="cyan")

def on_leave(event):
    event.widget.config(bg="black", fg="cyan")

for item in context_menu.winfo_children():
    item.bind("<Enter>", on_hover)
    item.bind("<Leave>", on_leave)

# Position the floating button near the bottom-right of the screen.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
default_x = screen_width - canvas_size - 20  # Adjust margins as needed.
default_y = screen_height - canvas_size - 20
root.geometry(f"+{default_x}+{default_y}")

# Start the pulsating glow effect
glow_phase = 0

root.mainloop()
