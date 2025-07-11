import os
import sys
import math
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
from pathlib import Path
from datetime import datetime
import time
import importlib
import webbrowser
from tkinter import colorchooser
from PIL import ImageColor

class SplashScreen:
    def __init__(self, window):
        self.window = window
        self.window.overrideredirect(True)  # Remove window decorations

        self.window.attributes('-topmost', True)

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        width, height = 400, 200
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        self.window.configure(bg="#242424")

        frame = tk.Frame(self.window, bg="#242424", highlightbackground="#4a7a8c", 
                        highlightthickness=2, bd=0)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, 
                   relwidth=0.9, relheight=0.9)

        title = tk.Label(frame, text="BG Remover", font=("Segoe UI", 16, "bold"), 
                        bg="#242424", fg="#4a7a8c")
        title.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.message = tk.Label(frame, text="Loading...", font=("Segoe UI", 10), 
                              bg="#242424", fg="#ffffff")
        self.message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.progress = ttk.Progressbar(frame, orient="horizontal", mode="indeterminate", 
                                      style="Splash.Horizontal.TProgressbar")
        self.progress.place(relx=0.5, rely=0.7, anchor=tk.CENTER, relwidth=0.8)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Splash.Horizontal.TProgressbar", 
                      background="#4a7a8c", troughcolor="#2a2a2a")
        
        self.progress.start(10)

        self.window.update()
    
    def update_message(self, message):
        self.message.config(text=message)
        self.window.update()
    
    def close(self):
        self.progress.stop()
        self.window.destroy()

def load_module(module_name, display_name, splash=None):
    if splash:
        splash.update_message(f"Loading {display_name}...")
    
    return importlib.import_module(module_name)

TKDND_AVAILABLE = False
TkinterDnD = None
DND_FILES = None
REMBG_AVAILABLE = False
remove = None

try:
    tkdnd_module = importlib.import_module('tkinterdnd2')
    TKDND_AVAILABLE = True
    TkinterDnD = tkdnd_module.TkinterDnD
    DND_FILES = tkdnd_module.DND_FILES
except ImportError:
    TKDND_AVAILABLE = False
    print("Warning: tkinterdnd2 not installed. Drag and drop will not work.")

try:
    rembg_module = importlib.import_module('rembg')
    remove = rembg_module.remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    print("Warning: rembg not installed. Please install it using 'pip install rembg'.")

class ModernUI(ttk.Frame):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.style = ttk.Style()
        
class ModernButton(tk.Canvas):
    
    def __init__(self, master, text, command, width=130, height=42, bg_color="#4361ee", hover_color="#3a56d4", 
                 icon=None, icon_size=16, radius=12, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, bg="#242424", **kwargs)
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.click_color = self._darken_color(bg_color, 0.15)
        self.command = command
        self.text = text
        self.icon = icon

        shadow_offset = 3
        shadow_color = "#1a1a1a"
        self.shadow_id = self.create_rectangle(shadow_offset, shadow_offset, 
                                              width + shadow_offset - 2, height + shadow_offset - 2, 
                                              fill=shadow_color, outline="", width=0, radius=radius)

        self.rect_id = self.create_rectangle(0, 0, width, height, fill=bg_color, outline="", width=0, radius=radius)

        if icon:

            x_offset = 10  # Padding from left

            if icon == "folder":

                folder_size = icon_size + 2
                self.icon_id = self.create_rectangle(
                    x_offset, height/2 - folder_size/2 + 1, 
                    x_offset + folder_size, height/2 + folder_size/2,
                    fill="white", outline="", width=0, radius=3
                )

                tab_width = folder_size * 0.4
                tab_height = folder_size * 0.25
                self.create_rectangle(
                    x_offset + folder_size/2 - tab_width/2, height/2 - folder_size/2 - tab_height/2 + 1,
                    x_offset + folder_size/2 + tab_width/2, height/2 - folder_size/2 + tab_height/2 + 1,
                    fill="white", outline="", width=0, radius=2
                )
            elif icon == "process":

                cx = x_offset + icon_size/2
                cy = height/2
                r = icon_size/2

                arrow_points = []
                for i in range(0, 270, 5):
                    angle = math.radians(i)
                    x = cx + r * math.cos(angle)
                    y = cy + r * math.sin(angle)
                    arrow_points.append(x)
                    arrow_points.append(y)

                angle = math.radians(270)
                ax = cx + r * math.cos(angle)
                ay = cy + r * math.sin(angle)
                arrow_points.extend([ax, ay, ax-3, ay-4, ax+3, ay-4, ax, ay])
                
                self.icon_id = self.create_line(*arrow_points, fill="white", width=2, smooth=True)
            elif icon == "save":

                save_size = icon_size + 2

                self.icon_id = self.create_rectangle(
                    x_offset, height/2 - save_size/2,
                    x_offset + save_size, height/2 + save_size/2,
                    fill="white", outline="", width=0, radius=2
                )

                inner_margin = 3
                self.create_rectangle(
                    x_offset + inner_margin, height/2 - save_size/2 + inner_margin,
                    x_offset + save_size - inner_margin, height/2 + save_size/2 - inner_margin,
                    fill=bg_color, outline="", width=0, radius=1
                )

                slider_height = 4
                self.create_rectangle(
                    x_offset + save_size/3, height/2 - save_size/2 + inner_margin/2,
                    x_offset + save_size - save_size/3, height/2 - save_size/2 + slider_height,
                    fill="white", outline="", width=0
                )
            elif icon == "palette":

                palette_radius = icon_size/2 + 1

                self.icon_id = self.create_oval(
                    x_offset, height/2 - palette_radius,
                    x_offset + 2 * palette_radius, height/2 + palette_radius,
                    fill="white", outline=""
                )

                center_x = x_offset + palette_radius
                center_y = height/2
                segment_colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6", "#ec4899"]
                
                for i, color in enumerate(segment_colors):
                    angle_start = i * 60
                    angle_end = (i + 1) * 60

                    points = [center_x, center_y]

                    for angle in range(angle_start, angle_end + 1, 10):
                        rad = math.radians(angle)
                        x = center_x + (palette_radius - 3) * math.cos(rad)
                        y = center_y + (palette_radius - 3) * math.sin(rad)
                        points.extend([x, y])

                    self.create_polygon(points, fill=color, outline="", smooth=True)

                inner_radius = palette_radius / 3
                self.create_oval(
                    center_x - inner_radius, center_y - inner_radius,
                    center_x + inner_radius, center_y + inner_radius,
                    fill=bg_color, outline="white"
                )
            elif icon == "download":

                icon_width = icon_size + 2
                icon_height = icon_size + 2

                self.icon_id = self.create_line(
                    x_offset + icon_width/2, height/2 - icon_height/2 + 2,
                    x_offset + icon_width/2, height/2 + icon_height/2 - 5,
                    fill="white", width=2
                )

                arrow_width = icon_width / 2
                arrow_head = [
                    x_offset + icon_width/2 - arrow_width/2, height/2 + icon_height/2 - 8,
                    x_offset + icon_width/2, height/2 + icon_height/2 - 2,
                    x_offset + icon_width/2 + arrow_width/2, height/2 + icon_height/2 - 8
                ]
                self.create_polygon(arrow_head, fill="white", outline="")

                self.create_line(
                    x_offset + 2, height/2 + icon_height/2 - 2,
                    x_offset + icon_width - 2, height/2 + icon_height/2 - 2,
                    fill="white", width=2
                )
            else:

                self.icon_id = self.create_oval(
                    x_offset, height/2 - icon_size/2, 
                    x_offset + icon_size, height/2 + icon_size/2, 
                    fill="white"
                )

            self.text_id = self.create_text(x_offset + icon_size + 8, height/2, 
                                          text=text, fill="white", font=("Segoe UI", 11, "bold"),
                                          anchor="w")
        else:

            self.text_id = self.create_text(width/2, height/2, 
                                          text=text, fill="white", font=("Segoe UI", 11, "bold"))

        self.highlight_id = self.create_rectangle(3, 3, width-3, height/2, 
                                               fill="white", outline="", width=0, radius=radius-2)
        self.itemconfig(self.highlight_id, stipple="gray25")  # Make it translucent

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)
    
    def _on_enter(self, event):
        self.itemconfig(self.rect_id, fill=self.hover_color)

        self.move(self.shadow_id, -1, -1)
    
    def _on_leave(self, event):
        self.itemconfig(self.rect_id, fill=self.bg_color)

        self.move(self.shadow_id, 1, 1)
    
    def _on_click(self, event):
        self.itemconfig(self.rect_id, fill=self.click_color)

        self.move(self.rect_id, 1, 1)
        self.move(self.text_id, 1, 1)
        if hasattr(self, 'icon_id'):
            self.move(self.icon_id, 1, 1)
        self.move(self.highlight_id, 1, 1)
    
    def _on_release(self, event):
        self.itemconfig(self.rect_id, fill=self.hover_color)

        self.move(self.rect_id, -1, -1)
        self.move(self.text_id, -1, -1)
        if hasattr(self, 'icon_id'):
            self.move(self.icon_id, -1, -1)
        self.move(self.highlight_id, -1, -1)
        if self.command:
            self.command()
    
    def _darken_color(self, hex_color, factor=0.1):
        

        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))

        return f"#{r:02x}{g:02x}{b:02x}"
    
    def create_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):

        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BG Remover")

        if sys.platform == "win32":
            self.root.state('zoomed')
        else:
            self.root.attributes('-zoomed', True)
        self.root.minsize(800, 600)

        self.apply_dark_theme()
        
        self.input_image_path = None
        self.output_image_path = None
        self.input_image = None
        self.output_image = None
        self.processing = False
        self.drag_data = {"x": 0, "y": 0, "item": None}
        
        self._create_widgets()

        self.root.update_idletasks()
        self.setup_drag_drop()
        
    def setup_drag_drop(self):
        
        if TKDND_AVAILABLE:

            self.input_canvas.drop_target_register(DND_FILES)
            self.input_canvas.dnd_bind("<<Drop>>", self.on_drop)
        
    def apply_dark_theme(self):

        self.root.configure(bg="#242424")
        style = ttk.Style()

        style.theme_create("modern_dark", parent="alt", settings={
            "TFrame": {"configure": {"background": "#242424"}},
            "TLabel": {"configure": {"background": "#242424", "foreground": "#ffffff", "font": ("Segoe UI", 10)}},
            "TLabelframe": {"configure": {"background": "#242424", "foreground": "#ffffff", "bordercolor": "#3c3c3c"}},
            "TLabelframe.Label": {"configure": {"background": "#242424", "foreground": "#ffffff", "font": ("Segoe UI", 10, "bold")}},
            "TCheckbutton": {
                "configure": {
                    "background": "#242424",
                    "foreground": "#ffffff",
                    "indicatorcolor": "#4a7a8c",
                    "font": ("Segoe UI", 10)
                }
            },
            "Horizontal.TProgressbar": {
                "configure": {
                    "background": "#4a7a8c",
                    "troughcolor": "#2a2a2a"
                }
            }
        })

        style.theme_use("modern_dark")
        
    def _create_widgets(self):

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        self.top_frame = tk.Frame(self.main_frame, bg="#2a2a2a", padx=12, pady=10)
        self.top_frame.pack(fill=tk.X, pady=(0, 15))

        control_title = ttk.Label(self.top_frame, text="IMAGE CONTROLS", 
                               font=("Segoe UI", 12, "bold"), foreground="#7f8c8d")
        control_title.pack(anchor=tk.W, pady=(0, 12))

        buttons_frame = tk.Frame(self.top_frame, bg="#2a2a2a")
        buttons_frame.pack(fill=tk.X, pady=(0, 15))

        self.select_btn = ModernButton(
            buttons_frame, text="Select Image", 
            command=self.select_image, 
            width=150, 
            bg_color="#4361ee",
            icon="folder"
        )
        self.select_btn.pack(side=tk.LEFT, padx=(0, 15))

        self.process_btn = ModernButton(
            buttons_frame, 
            text="Remove Background", 
            command=self.process_image, 
            width=190, 
            bg_color="#10b981",
            icon="process"
        )
        self.process_btn.pack(side=tk.LEFT, padx=(0, 15))

        self.save_btn = ModernButton(
            buttons_frame, 
            text="Save Image", 
            command=self.save_image, 
            width=150, 
            bg_color="#8b5cf6",
            icon="save"
        )
        self.save_btn.pack(side=tk.LEFT, padx=(0, 15))

        settings_frame = tk.Frame(self.top_frame, bg="#323232", padx=10, pady=8)
        settings_frame.pack(fill=tk.X, pady=(5, 0))

        settings_title = ttk.Label(settings_frame, text="SETTINGS", 
                               font=("Segoe UI", 10, "bold"), foreground="#7f8c8d")
        settings_title.pack(anchor=tk.W, pady=(0, 8))

        settings_controls = tk.Frame(settings_frame, bg="#323232")
        settings_controls.pack(fill=tk.X)

        checkbox_container = tk.Frame(settings_controls, bg="#323232")
        checkbox_container.pack(side=tk.LEFT, padx=(0, 20))
        
        self.alpha_matting_var = tk.BooleanVar(value=True)

        self.alpha_check_frame = tk.Frame(checkbox_container, bg="#323232")
        self.alpha_check_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.alpha_check_box = tk.Canvas(self.alpha_check_frame, width=18, height=18, 
                                      bg="#323232", highlightthickness=0)
        self.alpha_check_box.pack(side=tk.LEFT, padx=(0, 6))

        self.check_outline = self.alpha_check_box.create_rectangle(0, 0, 18, 18, 
                                                              outline="#4361ee", width=2, fill="#2a2a2a")
        self.check_fill = self.alpha_check_box.create_rectangle(3, 3, 15, 15, 
                                                           outline="", fill="#4361ee", state="hidden")

        self.checkmark = self.alpha_check_box.create_line(4, 9, 8, 13, 14, 5, 
                                                     fill="white", width=2, state="hidden")

        def toggle_checkbox():
            new_state = not self.alpha_matting_var.get()
            self.alpha_matting_var.set(new_state)
            update_checkbox()
            
        def update_checkbox():
            if self.alpha_matting_var.get():
                self.alpha_check_box.itemconfig(self.check_fill, state="normal")
                self.alpha_check_box.itemconfig(self.checkmark, state="normal")
            else:
                self.alpha_check_box.itemconfig(self.check_fill, state="hidden")
                self.alpha_check_box.itemconfig(self.checkmark, state="hidden")

        update_checkbox()

        self.alpha_check_box.bind("<Button-1>", lambda e: toggle_checkbox())
        
        check_label = ttk.Label(self.alpha_check_frame, text="Enhanced edges", 
                             font=("Segoe UI", 10), foreground="#ffffff")
        check_label.pack(side=tk.LEFT)
        check_label.bind("<Button-1>", lambda e: toggle_checkbox())

        info_label = ttk.Label(checkbox_container, text="Improves edge detection, but slower", 
                            foreground="#7f8c8d", font=("Segoe UI", 9))
        info_label.pack(side=tk.TOP, anchor=tk.W)

        quality_container = tk.Frame(settings_controls, bg="#323232")
        quality_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))

        quality_header = tk.Frame(quality_container, bg="#323232")
        quality_header.pack(side=tk.TOP, fill=tk.X)
        
        quality_title = ttk.Label(quality_header, text="Quality", 
                               font=("Segoe UI", 10), foreground="#ffffff")
        quality_title.pack(side=tk.LEFT)
        
        self.quality_var = tk.IntVar(value=3)  # Default to medium-high quality
        
        self.quality_label = ttk.Label(quality_header, text="Medium", 
                                 width=8, foreground="#4361ee", font=("Segoe UI", 10, "bold"))
        self.quality_label.pack(side=tk.RIGHT)

        slider_height = 6
        slider_bg = "#404040"
        slider_fg = "#4361ee"
        slider_width = 280

        slider_frame = tk.Frame(quality_container, bg="#323232", pady=8)
        slider_frame.pack(fill=tk.X)
        
        self.slider_canvas = tk.Canvas(slider_frame, height=20, width=slider_width,
                                   bg="#323232", highlightthickness=0)
        self.slider_canvas.pack(fill=tk.X)

        self.slider_track = self.slider_canvas.create_rectangle(
            0, 7, slider_width, 7 + slider_height,
            fill=slider_bg, outline="", width=0, stipple="gray50"
        )

        self.slider_fill = self.slider_canvas.create_rectangle(
            0, 7, (self.quality_var.get() / 5) * slider_width, 7 + slider_height,
            fill=slider_fg, outline="", width=0
        )

        handle_radius = 8
        self.slider_handle = self.slider_canvas.create_oval(
            (self.quality_var.get() / 5) * slider_width - handle_radius,
            7 + slider_height/2 - handle_radius,
            (self.quality_var.get() / 5) * slider_width + handle_radius,
            7 + slider_height/2 + handle_radius,
            fill="#ffffff", outline=slider_fg, width=2
        )

        for i in range(1, 6):
            x_pos = (i / 5) * slider_width

            self.slider_canvas.create_line(
                x_pos, 7, x_pos, 7 + slider_height,
                fill="#ffffff", width=1
            )

            self.slider_canvas.create_text(
                x_pos, 7 + slider_height + 8,
                text=str(i),
                fill="#7f8c8d",
                font=("Segoe UI", 8)
            )

        quality_labels_frame = tk.Frame(quality_container, bg="#323232")
        quality_labels_frame.pack(fill=tk.X)
        
        ttk.Label(quality_labels_frame, text="Fast", foreground="#7f8c8d", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        ttk.Label(quality_labels_frame, text="High Quality", foreground="#7f8c8d", font=("Segoe UI", 9)).pack(side=tk.RIGHT)

        def on_slider_press(event):
            self.slider_canvas.bind("<Motion>", on_slider_drag)
            self.slider_canvas.bind("<ButtonRelease-1>", on_slider_release)
            on_slider_drag(event)
        
        def on_slider_drag(event):
            x = min(max(0, event.x), slider_width)
            value = round((x / slider_width) * 5)
            value = max(1, min(5, value))  # Ensure value is between 1-5
            self.quality_var.set(value)
            update_slider()
        
        def on_slider_release(event):
            self.slider_canvas.unbind("<Motion>")
            self.slider_canvas.unbind("<ButtonRelease-1>")
        
        def update_slider():
            value = self.quality_var.get()
            position = (value / 5) * slider_width

            self.slider_canvas.coords(
                self.slider_fill,
                0, 7, position, 7 + slider_height
            )
            self.slider_canvas.coords(
                self.slider_handle,
                position - handle_radius, 7 + slider_height/2 - handle_radius,
                position + handle_radius, 7 + slider_height/2 + handle_radius
            )

            quality_map = {
                1: "Low",
                2: "Medium-",
                3: "Medium",
                4: "High",
                5: "Maximum"
            }
            self.quality_label.config(text=quality_map.get(value, "Medium"))

        self.slider_canvas.bind("<Button-1>", on_slider_press)

        self.quality_var.trace_add("write", lambda *args: update_slider())

        self.progress_var = tk.DoubleVar()
        self.progress_frame = ttk.Frame(self.main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            orient="horizontal",
            mode="indeterminate",
            variable=self.progress_var,
            style="Horizontal.TProgressbar"
        )

        self.images_frame = ttk.Frame(self.main_frame)
        self.images_frame.pack(fill=tk.BOTH, expand=True)

        self.input_frame = ttk.LabelFrame(self.images_frame, text="Input Image", padding=(3,3,3,3))
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        
        self.input_canvas = tk.Canvas(self.input_frame, bg="#1e1e1e", highlightthickness=0)
        self.input_canvas.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        try:
            self.input_placeholder = self.input_canvas.create_text(
                200, 180, 
                text="Drag & Drop\nor Click Select Image", 
                fill="#7f8c8d", 
                font=("Segoe UI", 13, "bold"),
                justify=tk.CENTER
            )
        except:

            self.input_placeholder = None

        self.output_frame = ttk.LabelFrame(self.images_frame, text="Output Image", padding=(3,3,3,3))
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        output_container = ttk.Frame(self.output_frame)
        output_container.pack(fill=tk.BOTH, expand=True)
        
        self.output_canvas = tk.Canvas(output_container, bg="#1e1e1e", highlightthickness=0)
        self.output_canvas.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        output_buttons_frame = tk.Frame(output_container, bg="#1e1e1e")
        output_buttons_frame.pack(fill=tk.X, padx=3, pady=(5, 3))

        self.replace_bg_btn = ModernButton(
            output_buttons_frame, 
            text="Replace Background", 
            command=self.replace_background, 
            width=180, 
            bg_color="#3b82f6",
            icon="palette"
        )
        self.replace_bg_btn.pack(side=tk.LEFT, padx=(0, 20))
        self.replace_bg_btn.config(state=tk.DISABLED)

        self.download_btn = ModernButton(
            output_buttons_frame, 
            text="Download", 
            command=self.download_image, 
            width=120, 
            bg_color="#10b981",
            icon="download"
        )
        self.download_btn.pack(side=tk.LEFT, padx=0)
        self.download_btn.config(state=tk.DISABLED)

        self.loading_elements = []
        self.loading_text_id = None
        self.loading_subtext_id = None
        self.loading_animation_active = False

        try:
            self.output_placeholder = self.output_canvas.create_text(
                200, 180, 
                text="Processed image\nwill appear here", 
                fill="#7f8c8d", 
                font=("Segoe UI", 14, "bold"),
                justify=tk.CENTER
            )
        except:

            self.output_placeholder = None

        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(fill=tk.X, pady=(10, 0))

        self.status_frame = ttk.Frame(self.bottom_frame)
        self.status_frame.pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar(value="Ready - Select an image or drag & drop to start")
        self.status_label = ttk.Label(
            self.status_frame, 
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            foreground="#bdc3c7"
        )
        self.status_label.pack(side=tk.LEFT)

        version_frame = ttk.Frame(self.bottom_frame)
        version_frame.pack(side=tk.LEFT, padx=15)
        
        version_label = ttk.Label(
            version_frame,
            text="v1.2",
            font=("Segoe UI", 9, "bold"),
            foreground="#4361ee"
        )
        version_label.pack(side=tk.LEFT)

        dev_frame = ttk.Frame(self.bottom_frame)
        dev_frame.pack(side=tk.RIGHT, padx=20)
        
        dev_text = ttk.Label(
            dev_frame,
            text="Developed by ",
            font=("Segoe UI", 9),
            foreground="#7f8c8d"
        )
        dev_text.pack(side=tk.LEFT)

        dev_name = ttk.Label(
            dev_frame,
            text="Muhammad Izhan",
            font=("Segoe UI", 9, "underline"),
            foreground="#4361ee",
            cursor="hand2"  # Hand cursor on hover
        )
        dev_name.pack(side=tk.LEFT)

        def open_linkedin(event):

            import webbrowser
            webbrowser.open("https://www.linkedin.com/in/muhammad-izhan-a404752a6/")
            
        dev_name.bind("<Button-1>", open_linkedin)

        self.timestamp_var = tk.StringVar()
        self.update_timestamp()
        
        self.timestamp_label = ttk.Label(
            self.bottom_frame,
            textvariable=self.timestamp_var,
            font=("Segoe UI", 9),
            foreground="#7f8c8d"
        )
        self.timestamp_label.pack(side=tk.RIGHT, padx=(20, 0))

        self.root.after(1000, self.update_timestamp)

        self.process_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)

        self.root.after(100, self.add_placeholder_texts)
    
    def add_placeholder_texts(self):
        
        if self.input_placeholder is None:
            self.input_placeholder = self.input_canvas.create_text(
                self.input_canvas.winfo_width() // 2, self.input_canvas.winfo_height() // 2, 
                text="Drag & Drop\nor Click Select Image", 
                fill="#7f8c8d", 
                font=("Segoe UI", 14, "bold"),
                justify=tk.CENTER
            )
        
        if self.output_placeholder is None:
            self.output_placeholder = self.output_canvas.create_text(
                self.output_canvas.winfo_width() // 2, self.output_canvas.winfo_height() // 2, 
                text="Processed image\nwill appear here", 
                fill="#7f8c8d", 
                font=("Segoe UI", 14, "bold"),
                justify=tk.CENTER
            )
    
    def update_timestamp(self):
        
        self.timestamp_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self.update_timestamp)
    
    def on_drop(self, event):
        

        filepath = event.data

        if filepath.startswith("{") and filepath.endswith("}"):
            filepath = filepath[1:-1]

        if filepath and os.path.isfile(filepath):
            try:

                Image.open(filepath)

                self.load_image(filepath)
            except Exception as e:

                messagebox.showerror("Error", f"The dropped file is not a valid image: {str(e)}")
    
    def select_image(self):
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Select Image",
            filetypes=filetypes
        )
        
        if not filepath:
            return
        
        self.load_image(filepath)
    
    def load_image(self, filepath):
        
        try:
            self.input_image_path = filepath
            self.input_image = Image.open(filepath)

            self.display_image(self.input_canvas, self.input_image, is_input=True)

            self.process_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.DISABLED)
            self.output_image = None
            self.output_image_path = None
            self.status_var.set(f"Loaded: {os.path.basename(filepath)}")

            self.output_canvas.delete("all")

            try:
                self.output_placeholder = self.output_canvas.create_text(
                    self.output_canvas.winfo_width() // 2, self.output_canvas.winfo_height() // 2, 
                    text="Click 'Remove Background'\nto process image", 
                    fill="#7f8c8d", 
                    font=("Segoe UI", 14, "bold"),
                    justify=tk.CENTER
                )
            except:
                pass
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {str(e)}")
            self.status_var.set("Error loading image")
    
    def display_image(self, canvas, image, is_input=False):

        self.root.update_idletasks()

        canvas.delete("all")

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if canvas_width <= 1:
            canvas_width = 450
        if canvas_height <= 1:
            canvas_height = 450

        img_width, img_height = image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        resized_img = image.resize((new_width, new_height), Image.LANCZOS)

        photo = ImageTk.PhotoImage(resized_img)

        canvas.photo = photo

        image_item = canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=photo,
            anchor=tk.CENTER
        )

        if is_input:
            canvas.create_rectangle(
                (canvas_width - new_width) // 2 - 2,
                (canvas_height - new_height) // 2 - 2,
                (canvas_width + new_width) // 2 + 2,
                (canvas_height + new_height) // 2 + 2,
                outline="#4a7a8c",
                width=1
            )
        else:

            self.draw_transparency_grid(canvas, 
                                       (canvas_width - new_width) // 2,
                                       (canvas_height - new_height) // 2,
                                       new_width, new_height)

            canvas.tag_raise(image_item)
    
    def draw_transparency_grid(self, canvas, x, y, width, height):
        
        square_size = 10
        for row in range(0, height, square_size):
            for col in range(0, width, square_size):
                color = "#3c3c3c" if (row // square_size + col // square_size) % 2 == 0 else "#323232"
                canvas.create_rectangle(
                    x + col, y + row, 
                    x + col + square_size, y + row + square_size, 
                    fill=color, outline="", width=0
                )
    
    def process_image(self):
        if not self.input_image or self.processing:
            return

        if not REMBG_AVAILABLE:
            messagebox.showerror("Module Error", 
                               "The rembg module is not installed. Please run 'pip install rembg' and restart the application.")
            return

        self.processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.select_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)

        self.select_btn.itemconfig(self.select_btn.rect_id, fill="#6b7280")  # Gray out
        self.process_btn.itemconfig(self.process_btn.rect_id, fill="#6b7280")
        self.save_btn.itemconfig(self.save_btn.rect_id, fill="#6b7280")

        self.status_var.set("Processing image...")

        self.output_canvas.delete("all")
        self.show_advanced_loading_animation()

        thread = threading.Thread(target=self._process_image_thread)
        thread.daemon = True
        thread.start()

        
    def _process_image_thread(self):
        try:

            self.root.after(0, lambda: self.status_var.set("Preparing AI model..."))

            alpha_matting = self.alpha_matting_var.get()
            quality_level = self.quality_var.get()

            if quality_level == 1:  # Low quality but fast
                params = {
                    "alpha_matting_foreground_threshold": 250,
                    "alpha_matting_background_threshold": 20,
                    "alpha_matting_erode_size": 5,
                }

                img_width, img_height = self.input_image.size
                max_size = 1000  # Max dimension for low quality processing
                if img_width > max_size or img_height > max_size:
                    ratio = min(max_size / img_width, max_size / img_height)
                    new_size = (int(img_width * ratio), int(img_height * ratio))
                    self.root.after(0, lambda: self.status_var.set("Resizing image for faster processing..."))
                    processing_image = self.input_image.resize(new_size, Image.LANCZOS)
                else:
                    processing_image = self.input_image
            else:
                processing_image = self.input_image
                
                if quality_level == 2:  # Medium-Low
                    params = {
                        "alpha_matting_foreground_threshold": 245,
                        "alpha_matting_background_threshold": 15,
                        "alpha_matting_erode_size": 10,
                    }
                elif quality_level == 3:  # Medium-High (default)
                    params = {
                        "alpha_matting_foreground_threshold": 240,
                        "alpha_matting_background_threshold": 10,
                        "alpha_matting_erode_size": 15,
                    }
                elif quality_level == 4:  # High
                    params = {
                        "alpha_matting_foreground_threshold": 235,
                        "alpha_matting_background_threshold": 8,
                        "alpha_matting_erode_size": 20,
                    }
                else:  # Maximum quality (level 5)
                    params = {
                        "alpha_matting_foreground_threshold": 230,
                        "alpha_matting_background_threshold": 5,
                        "alpha_matting_erode_size": 30,
                    }

            self.root.after(0, lambda: self.status_var.set("Removing background..."))

            output_image = remove(
                processing_image, 
                alpha_matting=alpha_matting,
                alpha_matting_foreground_threshold=params["alpha_matting_foreground_threshold"],
                alpha_matting_background_threshold=params["alpha_matting_background_threshold"],
                alpha_matting_erode_size=params["alpha_matting_erode_size"],
                post_process_mask=True  # Enable post-processing for cleaner edges
            )

            if quality_level == 1 and processing_image is not self.input_image:
                self.root.after(0, lambda: self.status_var.set("Restoring original size..."))
                self.output_image = output_image.resize(self.input_image.size, Image.LANCZOS)
            else:
                self.output_image = output_image

            self.root.after(0, self._processing_complete)
        except Exception as e:

            self.root.after(0, lambda: self._processing_failed(str(e)))
    
    def _processing_complete(self):

        self.clear_loading_animation()

        self.display_image(self.output_canvas, self.output_image)

        self.processing = False
        self.select_btn.config(state=tk.NORMAL)
        self.process_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)

        self.replace_bg_btn.config(state=tk.NORMAL)
        self.download_btn.config(state=tk.NORMAL)

        self.select_btn.itemconfig(self.select_btn.rect_id, fill="#4361ee")
        self.process_btn.itemconfig(self.process_btn.rect_id, fill="#10b981")
        self.save_btn.itemconfig(self.save_btn.rect_id, fill="#8b5cf6")

        self.status_var.set("Background removed successfully!")

        for i in range(3):
            self.root.after(i * 300, lambda i=i: self.save_btn.itemconfig(self.save_btn.rect_id, fill="#a855f7"))
            self.root.after(i * 300 + 150, lambda i=i: self.save_btn.itemconfig(self.save_btn.rect_id, fill="#8b5cf6"))
    
    def _processing_failed(self, error_message):

        self.clear_loading_animation()

        self.processing = False
        self.select_btn.config(state=tk.NORMAL)
        self.process_btn.config(state=tk.NORMAL)

        self.select_btn.itemconfig(self.select_btn.rect_id, fill="#4361ee")

        messagebox.showerror("Processing Error", f"Failed to remove background: {error_message}")

        self.status_var.set("Error during processing")
        self.process_btn.itemconfig(self.process_btn.rect_id, fill="#ef4444")  # Red error color
        self.root.after(2000, lambda: self.process_btn.itemconfig(self.process_btn.rect_id, fill="#10b981"))

        width = self.output_canvas.winfo_width()
        height = self.output_canvas.winfo_height()
        
        self.output_canvas.create_text(
            width // 2, height // 2 - 20,
            text="Processing Failed",
            fill="#ef4444",
            font=("Segoe UI", 16, "bold"),
            justify=tk.CENTER
        )
        
        self.output_canvas.create_text(
            width // 2, height // 2 + 20,
            text="Please try again or select a different image",
            fill="#7f8c8d",
            font=("Segoe UI", 11),
            justify=tk.CENTER
        )
    
    def save_image(self):
        if not self.output_image:
            return

        if hasattr(self, 'preview_bg_color') and self.preview_bg_color:

            self.status_var.set("Applying current color before saving...")
            self._apply_background_color(self.preview_bg_color)

            self.save_after_color_applied = True
            return

        original_ext = os.path.splitext(self.input_image_path)[1].lower()

        if original_ext in ['.jpg', '.jpeg']:
            default_ext = '.png'  # Save with transparency
            file_type = 'PNG'
        else:
            default_ext = original_ext
            file_type = original_ext[1:].upper()

        input_filename = os.path.basename(self.input_image_path)
        suggested_name = f"{os.path.splitext(input_filename)[0]}_no_bg{default_ext}"

        filetypes = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("WebP files", "*.webp"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=default_ext,
            filetypes=filetypes,
            initialfile=suggested_name
        )
        
        if not filepath:
            return
        
        try:

            self.status_var.set("Saving image...")

            save_thread = threading.Thread(target=self._save_image_thread, args=(filepath,))
            save_thread.daemon = True
            save_thread.start()
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save image: {str(e)}")
            self.status_var.set("Error saving image")
    
    def _save_image_thread(self, filepath):
        try:

            current_image = self.output_image


            if current_image.mode == 'RGBA' and hasattr(self, 'original_output_image'):


                bg_color = (255, 255, 255, 255)  # White background

                background = Image.new('RGBA', current_image.size, bg_color)
                composite = Image.alpha_composite(background, current_image)
                current_image = composite.convert('RGB')

            current_image.save(filepath)
            self.output_image_path = filepath

            self.root.after(0, lambda: self._save_complete(filepath))
        except Exception as e:

            self.root.after(0, lambda: self._save_failed(str(e)))
    
    def _save_complete(self, filepath):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.status_var.set(f"Saved to: {os.path.basename(filepath)}")
    
    def _save_failed(self, error_message):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        messagebox.showerror("Save Error", f"Failed to save image: {error_message}")
        self.status_var.set("Error saving image")

    def show_advanced_loading_animation(self):
        

        self.clear_loading_animation()

        self.loading_animation_active = True

        width = self.output_canvas.winfo_width()
        height = self.output_canvas.winfo_height()
        center_x = width // 2
        center_y = height // 2

        backdrop = self.output_canvas.create_rectangle(
            0, 0, width, height,
            fill="#141414", outline="", stipple="gray25"
        )
        self.loading_elements.append(backdrop)

        radius = 25
        num_circles = 6
        base_colors = ["#4361ee", "#3a56d4", "#304acb", "#263fc3", "#1c35bb", "#122ab3"]
        
        for i in range(num_circles):
            circle = self.output_canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=base_colors[i % len(base_colors)],
                width=3,
                fill=""
            )
            self.loading_elements.append(circle)

        glow_size = 20
        for offset in range(3):
            glow = self.output_canvas.create_text(
                center_x, center_y - 70 - offset,
                text="PROCESSING IMAGE",
                fill=f"#{2+offset*2:02x}{2+offset*2:02x}{2+offset*2:02x}",
                font=("Segoe UI", 16, "bold"),
                justify=tk.CENTER
            )
            self.loading_elements.append(glow)
            
        self.loading_text_id = self.output_canvas.create_text(
            center_x, center_y - 70,
            text="PROCESSING IMAGE",
            fill="#ffffff",
            font=("Segoe UI", 16, "bold"),
            justify=tk.CENTER
        )
        self.loading_elements.append(self.loading_text_id)

        self.loading_subtext_id = self.output_canvas.create_text(
            center_x, center_y + 70,
            text="AI model is analyzing and removing the background...",
            fill="#7f8c8d",
            font=("Segoe UI", 10),
            justify=tk.CENTER
        )
        self.loading_elements.append(self.loading_subtext_id)

        self._animate_loading(0, num_circles, radius, center_x, center_y, base_colors)
    
    def _animate_loading(self, frame, num_circles, radius, cx, cy, colors):
        
        if not self.loading_animation_active:
            return

        for i in range(num_circles):

            angle = 2 * math.pi * ((i / num_circles) + (frame % 100) / 100)
            pulse = math.sin(frame / 10 + i) * 0.2 + 0.8  # Value between 0.6 and 1.0

            distance = radius * 2.5 * pulse
            x = cx + distance * math.cos(angle)
            y = cy + distance * math.sin(angle)
            size = radius * pulse

            circle_id = self.loading_elements[i + 1]  # +1 to skip backdrop
            self.output_canvas.coords(
                circle_id,
                x - size, y - size,
                x + size, y + size
            )

            opacity = int(200 * pulse)
            color_index = (i + frame // 10) % len(colors)
            color = colors[color_index]
            self.output_canvas.itemconfig(circle_id, outline=color)

        if frame % 40 < 10:
            self.output_canvas.itemconfig(self.loading_text_id, text="PROCESSING IMAGE")
        elif frame % 40 < 20:
            self.output_canvas.itemconfig(self.loading_text_id, text="PROCESSING IMAGE.")
        elif frame % 40 < 30:
            self.output_canvas.itemconfig(self.loading_text_id, text="PROCESSING IMAGE..")
        else:
            self.output_canvas.itemconfig(self.loading_text_id, text="PROCESSING IMAGE...")

        if frame % 150 == 0:
            messages = [
                "AI model is analyzing and removing the background...",
                "Detecting objects and subject edges...",
                "Applying advanced masking algorithm...",
                "Refining edge details...",
                "Optimizing transparency mask..."
            ]
            msg_index = (frame // 150) % len(messages)
            self.output_canvas.itemconfig(self.loading_subtext_id, text=messages[msg_index])

        if self.loading_animation_active:
            self.root.after(40, lambda: self._animate_loading(frame + 1, num_circles, radius, cx, cy, colors))
    
    def clear_loading_animation(self):
        
        self.loading_animation_active = False
        for element in self.loading_elements:
            self.output_canvas.delete(element)
        self.loading_elements = []
        self.loading_text_id = None
        self.loading_subtext_id = None

    def replace_background(self):
        
        if not self.output_image:
            return

        color_dialog = tk.Toplevel(self.root)
        color_dialog.title("Select Background Color")
        color_dialog.geometry("400x300")
        color_dialog.resizable(False, False)
        color_dialog.transient(self.root)
        color_dialog.grab_set()

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 150
        color_dialog.geometry(f"+{x}+{y}")

        color_dialog.configure(bg="#1a1a1a")

        title_label = ttk.Label(color_dialog, text="Choose Background Color", 
                               font=("Segoe UI", 14, "bold"), foreground="#ffffff")
        title_label.pack(pady=(15, 20))

        selected_color_var = tk.StringVar(value="#000000")  # Default black

        def update_color_preview(color_hex):
            selected_color_var.set(color_hex)
            color_preview.config(bg=color_hex)

            self.preview_background_color(color_hex)

        preview_frame = tk.Frame(color_dialog, bg="#1a1a1a")
        preview_frame.pack(pady=(0, 15))
        
        ttk.Label(preview_frame, text="Preview:", foreground="#ffffff").pack(side=tk.LEFT, padx=(0, 10))
        
        color_preview = tk.Label(preview_frame, width=12, height=2, bg="#000000")
        color_preview.pack(side=tk.LEFT)

        predef_frame = tk.Frame(color_dialog, bg="#1a1a1a")
        predef_frame.pack(pady=(0, 15))
        
        ttk.Label(predef_frame, text="Quick Colors:", foreground="#ffffff").pack(anchor=tk.W, padx=10, pady=(0, 5))

        colors_frame = tk.Frame(predef_frame, bg="#1a1a1a")
        colors_frame.pack(padx=10)
        
        predefined_colors = [
            {"name": "Black", "hex": "#000000"}, 
            {"name": "White", "hex": "#FFFFFF"},
            {"name": "Red", "hex": "#FF0000"}, 
            {"name": "Green", "hex": "#00FF00"},
            {"name": "Blue", "hex": "#0000FF"}, 
            {"name": "Yellow", "hex": "#FFFF00"}
        ]

        color_buttons = []

        def select_color_and_preview(color_hex, button_index):

            update_color_preview(color_hex)

            for i, btn in enumerate(color_buttons):
                if i == button_index:
                    btn.config(relief=tk.SUNKEN, bd=3)
                else:
                    btn.config(relief=tk.RAISED, bd=2)

            apply_btn.config(state=tk.NORMAL)

            show_preview_overlay(color_hex)

        def show_preview_overlay(color_hex):

            if not self.output_image:
                return

            width = self.output_canvas.winfo_width()
            height = self.output_canvas.winfo_height()

            self.output_canvas.delete("preview_overlay")
        
        for i, color_info in enumerate(predefined_colors):
            btn = tk.Button(
                colors_frame, 
                bg=color_info["hex"], 
                width=6, height=2,
                bd=2, relief=tk.RAISED,
                command=lambda c=color_info["hex"], idx=i: select_color_and_preview(c, idx)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            color_buttons.append(btn)

            tk.Label(colors_frame, text=color_info["name"], bg="#1a1a1a", fg="#ffffff", 
                   font=("Segoe UI", 8)).grid(row=i//3, column=i%3, padx=5, pady=(0, 5), sticky="n")

        custom_frame = tk.Frame(color_dialog, bg="#1a1a1a")
        custom_frame.pack(pady=(10, 0))
        
        def choose_custom_color():

            color = colorchooser.askcolor(initialcolor=selected_color_var.get())
            if color[1]:  # If a color was selected
                update_color_preview(color[1])
        
        custom_btn = tk.Button(custom_frame, text="Custom Color...", command=choose_custom_color,
                            bg="#2a2a2a", fg="#ffffff", padx=10, pady=5)
        custom_btn.pack()

        btn_frame = tk.Frame(color_dialog, bg="#1a1a1a")
        btn_frame.pack(pady=15, fill=tk.X, padx=20)

        instructions = ttk.Label(btn_frame, text="Click 'Apply Color' to set background", 
                               foreground="#ffffff", font=("Segoe UI", 10))
        instructions.pack(side=tk.LEFT, pady=10)

        def apply_color():

            color_hex = selected_color_var.get()

            self.status_var.set("Applying background color...")

            self.output_canvas.delete("all")
            self.show_advanced_loading_animation()

            self.replace_bg_btn.config(state=tk.DISABLED)
            self.download_btn.config(state=tk.DISABLED)
            self.save_btn.config(state=tk.DISABLED)

            thread = threading.Thread(target=lambda: self._apply_background_color(color_hex))
            thread.daemon = True
            thread.start()

            color_dialog.destroy()

        def cancel():
            color_dialog.destroy()


        apply_btn = tk.Button(btn_frame, text="Apply Color", command=apply_color,
                           bg="#3b82f6", fg="#ffffff", font=("Segoe UI", 10, "bold"),
                           padx=20, pady=5, bd=0, relief="flat",
                           activebackground="#2563eb", activeforeground="#ffffff")
        apply_btn.pack(side=tk.RIGHT, padx=10)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=cancel,
                            bg="#6b7280", fg="#ffffff", font=("Segoe UI", 10),
                            padx=15, pady=5, bd=0, relief="flat",
                            activebackground="#4b5563", activeforeground="#ffffff")
        cancel_btn.pack(side=tk.RIGHT, padx=10)

        color_dialog.wait_window()
    
    def _apply_background_color(self, color_hex):
        
        try:

            self.status_var.set("Applying background color...")

            if hasattr(self, 'original_output_image'):
                img = self.original_output_image.copy()
            else:

                img = self.output_image.copy()

            if img.mode != 'RGBA':


                img = img.convert('RGBA')

            bg_color = ImageColor.getrgb(color_hex)
            background = Image.new('RGBA', img.size, bg_color + (255,))  # Adding alpha=255


            composite = Image.alpha_composite(background, img)

            self.output_image = composite.convert('RGB')

            self.last_applied_bg_color = color_hex

            self.original_output_image = img

            self.root.after(0, lambda: self._background_color_applied())
            
        except Exception as e:
            self.root.after(0, lambda: self._processing_failed(str(e)))
    
    def _background_color_applied(self):
        

        self.clear_loading_animation()

        self.display_image(self.output_canvas, self.output_image)

        self.replace_bg_btn.config(state=tk.NORMAL)
        self.download_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)

        self.status_var.set("Background color applied successfully!")

        if hasattr(self, 'save_after_color_applied') and self.save_after_color_applied:
            self.save_after_color_applied = False  # Reset flag

            self.preview_bg_color = None

            self.root.after(500, self.save_image)  # Short delay then save

        elif hasattr(self, 'download_after_color_applied') and self.download_after_color_applied:
            self.download_after_color_applied = False  # Reset flag

            self.preview_bg_color = None

            self.root.after(500, self.save_image)  # Short delay then download
    
    def download_image(self):
        
        if not self.output_image:
            return

        if hasattr(self, 'preview_bg_color') and self.preview_bg_color:

            self.status_var.set("Applying current color before download...")
            self._apply_background_color(self.preview_bg_color)

            self.download_after_color_applied = True
        else:

            self.save_image()

    def preview_background_color(self, color_hex):
        
        if not self.output_image:
            return
            
        try:

            self.status_var.set(f"Applying color... Click Apply Color button when ready")

            if not hasattr(self, 'original_output_image'):
                self.original_output_image = self.output_image.copy()
            else:

                img = self.original_output_image.copy()

                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                bg_color = ImageColor.getrgb(color_hex)
                background = Image.new('RGBA', img.size, bg_color + (255,))

                preview_composite = Image.alpha_composite(background, img)
                preview_image = preview_composite.convert('RGB')

                self.preview_bg_color = color_hex

                self._display_preview(preview_image)
        except Exception as e:

            print(f"Preview error: {e}")
    
    def _display_preview(self, preview_image):
        

        img_width, img_height = preview_image.size
        canvas_width = self.output_canvas.winfo_width()
        canvas_height = self.output_canvas.winfo_height()

        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        resized_preview = preview_image.resize((new_width, new_height), Image.LANCZOS)

        photo = ImageTk.PhotoImage(resized_preview)

        self.output_canvas.delete("preview_item")

        self.preview_photo = photo

        self.output_canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=photo,
            anchor=tk.CENTER,
            tags="preview_item"
        )


def center_window(root, width, height):
    

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":

    if TKDND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()

    root.withdraw()

    splash_win = tk.Toplevel(root)
    splash = SplashScreen(splash_win)

    splash.update_message("Loading modules...")

    def initialize_app():
        splash.update_message("Initializing user interface...")

        center_window(root, 1000, 700)

        app = BackgroundRemoverApp(root)

        splash.close()
        root.deiconify()

    root.after(1000, initialize_app)

    root.mainloop() 