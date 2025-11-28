import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import numpy as np
from ultralytics import YOLO
import time
import colorsys

class ObjectDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection Studio")
        self.root.geometry("1024x768")
        
        # Create canvas for animated background
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Initialize animation variables
        self.hue = 0
        self.animation_speed = 0.002
        self.gradient_steps = 10
        
        # Start background animation
        self.animate_background()

        # Initialize YOLO model
        self.model = YOLO('yolov8n.pt')

        # Create main frame with modern styling
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=30, pady=30, fill="both", expand=True)

        # Title Label with enhanced styling
        title_label = ttk.Label(
            self.main_frame,
            text="Object Detection Studio",
            font=("Helvetica", 28, "bold"),
            foreground="#ECF0F1",
            background="#2C3E50"
        )
        title_label.pack(pady=(0, 30))

        # Image display area with enhanced border and shadow effect
        self.image_frame = ttk.Frame(self.main_frame, style="Image.TFrame")
        self.image_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.image_label = ttk.Label(self.image_frame, background="#2C3E50")
        self.image_label.pack(pady=15, padx=15, fill="both", expand=True)

        # Enhanced button styles
        style = ttk.Style()
        style.configure("Image.TFrame",
            background="#2C3E50",
            borderwidth=3,
            relief="solid"
        )
        style.configure("Action.TButton",
            padding=(25, 12),
            font=("Helvetica", 12, "bold"),
            background="#1E272E",
            foreground="#ECF0F1"
        )
        style.map("Action.TButton",
            background=[("active", "#2C3E50"), ("pressed", "#1f618d")],
            foreground=[("active", "#FFFFFF")]
        )

        # Buttons frame with improved layout
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=40)

        # Create buttons with enhanced styling
        self.select_button = ttk.Button(
            self.button_frame,
            text="📁 Select Image",
            command=self.select_image,
            style="Action.TButton"
        )
        self.select_button.pack(side="left", padx=20)

        self.camera_button = ttk.Button(
            self.button_frame,
            text="📸 Take Photo",
            command=self.take_photo,
            style="Action.TButton"
        )
        self.camera_button.pack(side="left", padx=20)

        self.detect_button = ttk.Button(
            self.button_frame,
            text="🔍 Detect Objects",
            command=self.detect_objects,
            style="Action.TButton"
        )
        self.detect_button.pack(side="left", padx=20)

        # Add Delete Image button
        self.delete_button = ttk.Button(
            self.button_frame,
            text="🗑️ Delete Image",
            command=self.delete_image,
            style="Action.TButton",
            state="disabled"  # Initially disabled
        )
        self.delete_button.pack(side="left", padx=20)

        # Enhanced status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            font=("Helvetica", 11),
            foreground="#ECF0F1",
            background="#2C3E50",
            padding=(10, 5)
        )
        self.status_bar.pack(pady=(30, 0), fill="x")

        self.current_image_path = None
        
    def animate_background(self):
        # Clear previous gradient
        self.bg_canvas.delete("gradient")
        
        # Calculate colors for gradient
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        for i in range(self.gradient_steps):
            # Create smooth color transition with darker theme
            hue = (self.hue + i/self.gradient_steps) % 1.0
            # Reduced saturation and brightness for darker theme
            rgb = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.3, 0.3))
            color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
            
            # Draw gradient rectangle
            y1 = height * i / self.gradient_steps
            y2 = height * (i + 1) / self.gradient_steps
            self.bg_canvas.create_rectangle(
                0, y1, width, y2,
                fill=color, outline=color,
                tags="gradient"
            )
        
        # Slower animation for smoother transitions
        self.hue = (self.hue + 0.001) % 1.0
        
        # Schedule next animation frame
        self.root.after(50, self.animate_background)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)

    def take_photo(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not access the camera!")
            return

        # Create a window with a specific size
        cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Camera", 800, 600)

        # Create button regions with improved styling
        button_height = 40
        button_width = 120
        button_color = (45, 45, 45)
        button_hover_color = (60, 60, 60)
        text_color = (255, 255, 255)
        button_pressed = False
        mouse_over_exit = False

        while True:
            ret, frame = cap.read()
            if not ret:
                cap.release()
                cap = cv2.VideoCapture(0)
                continue

            height, width = frame.shape[:2]

            # Draw exit button with hover effect
            exit_color = button_hover_color if mouse_over_exit else button_color
            cv2.rectangle(frame, (width - button_width - 10, 10),
                        (width - 10, button_height + 10), exit_color, -1)
            cv2.rectangle(frame, (width - button_width - 10, 10),
                        (width - 10, button_height + 10), (70, 70, 70), 1)
            text_size = cv2.getTextSize("Exit", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            text_x = width - button_width - 10 + (button_width - text_size[0]) // 2
            text_y = 10 + (button_height + text_size[1]) // 2
            cv2.putText(frame, "Exit", (text_x, text_y),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)

            # Process YOLO detection
            results = self.model(frame)
            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id]
                    conf = float(box.conf[0])
                    if conf > 0.2:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        color = (
                            (hash(class_name) * 123) % 256,
                            (hash(class_name) * 147) % 256,
                            (hash(class_name) * 189) % 256
                        )
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
                        label = f'{class_name} ({conf:.1%})'
                        (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)
                        cv2.rectangle(frame, (x1, y1 - label_h - 15), (x1 + label_w + 10, y1), color, -1)
                        cv2.putText(frame, label, (x1 + 5, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

            cv2.imshow("Camera", frame)
            cv2.waitKey(1)

            def mouse_callback(event, x, y, flags, param):
                nonlocal mouse_over_exit, button_pressed
                # Check if mouse is over exit button
                mouse_over_exit = (width - button_width - 10 <= x <= width - 10 and
                                10 <= y <= button_height + 10)

                if event == cv2.EVENT_LBUTTONDOWN:
                    if mouse_over_exit:
                        button_pressed = True
                elif event == cv2.EVENT_LBUTTONUP:
                    if button_pressed and mouse_over_exit:
                        cap.release()
                        cv2.destroyAllWindows()
                        return True  # Signal to break the main loop
                    button_pressed = False
                return False  # Continue the main loop

            cv2.setMouseCallback("Camera", mouse_callback)
            
            # Check if we should exit the loop
            if cv2.waitKey(1) & 0xFF == 27 or mouse_callback(cv2.EVENT_LBUTTONUP, width-button_width-5, 15, 0, None):
                break

        cap.release()
        cv2.destroyAllWindows()

    def display_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((600, 400))
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=self.tk_image)
        self.image_label.image = self.tk_image
        # Enable delete button when image is displayed
        self.delete_button.configure(state="normal")

    def detect_objects(self):
        if self.current_image_path is None:
            messagebox.showwarning("Warning", "Please select an image first!")
            return

        results = self.model(self.current_image_path)
        image = cv2.imread(self.current_image_path)
        colors = {}
        objects_detected = False

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                conf = float(box.conf[0])
                if conf > 0.2:  # Lower threshold for more detections
                    objects_detected = True
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    if class_name not in colors:
                        colors[class_name] = (
                            (hash(str(class_name)) * 123) % 256,
                            (hash(str(class_name)) * 147) % 256,
                            (hash(str(class_name)) * 189) % 256
                        )
                    color = colors[class_name]
                    # Draw thicker bounding box
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, 4)
                    # Enhanced label with confidence percentage
                    label = f'{class_name} ({conf:.1%})'
                    # Add background to text with larger font
                    (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)
                    cv2.rectangle(image, (x1, y1 - label_h - 15), (x1 + label_w + 10, y1), color, -1)
                    cv2.putText(image, label, (x1 + 5, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

        if not objects_detected:
            messagebox.showinfo("Result", "No objects detected in this image!")
            return

        result_path = "detection_result.jpg"
        cv2.imwrite(result_path, image)
        self.display_image(result_path)

    def delete_image(self):
        if self.current_image_path:
            # Clear the display
            self.image_label.configure(image="")
            self.current_image_path = None
            # Disable delete button
            self.delete_button.configure(state="disabled")
            # Update status
            self.status_var.set("Image cleared from display")

    def apply_laplace_transform(self, image_path):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        laplace = cv2.Laplacian(image, cv2.CV_64F)
        laplace_abs = cv2.convertScaleAbs(laplace)
        result_path = "laplace_transform.jpg"
        cv2.imwrite(result_path, laplace_abs)
        self.display_image(result_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectDetectionApp(root)
    root.mainloop()
