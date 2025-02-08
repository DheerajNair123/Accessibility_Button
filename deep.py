import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3
import platform
import os


class FloatingAccessibilityButton:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Always on top
        self.root.attributes('-alpha', 0.8)  # Slightly transparent

        # Initial position
        self.x = 100
        self.y = 100

        # Create main floating button
        self.create_main_button()

        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)

        # Track drag motion
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

        # Bind events
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.drag)
        self.root.bind('<ButtonRelease-1>', self.stop_drag)

    def create_main_button(self):
        """Create circular floating button"""
        self.canvas = tk.Canvas(self.root, width=40, height=40,
                                bd=0, highlightthickness=0)
        self.canvas.pack()

        # Draw circular button
        self.button_bg = self.canvas.create_oval(
            2, 2, 38, 38,
            fill='#007AFF',  # iOS-style blue
            activefill='#0055BB',
            outline=''
        )

        # Draw accessibility symbol (♿)
        self.canvas.create_text(
            20, 20,
            text='♿',
            font=('Arial', 16),
            fill='white'
        )

        # Bind click event
        self.canvas.tag_bind(self.button_bg, '<Button-1>', self.toggle_menu)

    def toggle_menu(self, event=None):
        """Show/hide accessibility menu"""
        if hasattr(self, 'menu') and self.menu.winfo_exists():
            self.menu.destroy()
        else:
            self.show_menu()

    def show_menu(self):
        """Create floating menu"""
        self.menu = tk.Toplevel(self.root)
        self.menu.overrideredirect(True)
        self.menu.attributes('-topmost', True)

        # Position menu relative to main button
        x = self.root.winfo_x() + 50
        y = self.root.winfo_y() - 80
        self.menu.geometry(f'+{x}+{y}')

        # Menu items
        buttons = [
            ('🌑 High Contrast', self.toggle_high_contrast),
            ('🔊 Text-to-Speech', self.toggle_tts),
            ('🔍 Magnifier', self.toggle_magnifier),
            ('⚙️ Settings', self.open_system_settings)
        ]

        for text, cmd in buttons:
            btn = ttk.Button(self.menu, text=text, command=cmd,
                             style='Floating.TButton')
            btn.pack(pady=2, padx=2, fill=tk.X)

        # Style configuration
        style = ttk.Style()
        style.configure('Floating.TButton', font=('Arial', 10),
                        padding=5, relief='flat')

    def start_drag(self, event):
        """Start dragging the button"""
        self.dragging = True
        self.offset_x = event.x
        self.offset_y = event.y

    def drag(self, event):
        """Handle dragging motion"""
        if self.dragging:
            x = self.root.winfo_x() - self.offset_x + event.x
            y = self.root.winfo_y() - self.offset_y + event.y
            self.root.geometry(f'+{x}+{y}')

    def stop_drag(self, event):
        """Stop dragging"""
        self.dragging = False

    def toggle_high_contrast(self):
        """Toggle high contrast mode"""
        current_bg = self.canvas.itemcget(self.button_bg, 'fill')
        new_color = '#000000' if current_bg != '#000000' else '#007AFF'
        self.canvas.itemconfig(self.button_bg, fill=new_color)
        self.menu.configure(bg='black' if new_color == '#000000' else 'white')

    def toggle_tts(self):
        """Toggle text-to-speech demo"""
        self.tts_engine.say("Accessibility features activated")
        self.tts_engine.runAndWait()

    def toggle_magnifier(self):
        """Show magnifier notification"""
        messagebox.showinfo("Magnifier", "Screen magnifier activated\n(Simulated functionality)")

    def open_system_settings(self):
        """Open OS accessibility settings"""
        system = platform.system()
        try:
            if system == 'Windows':
                os.system('start ms-settings:easeofaccess')
            elif system == 'Darwin':
                os.system('open /System/Library/PreferencePanes/UniversalAccessPref.prefPane')
            elif system == 'Linux':
                os.system('gnome-control-center universal-access')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open settings: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingAccessibilityButton(root)
    root.geometry('40x40+100+100')  # Initial position
    root.mainloop()