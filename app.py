import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk
import os
import threading


class ImageToPdfConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.overlay_label = None  # To hold reference to the overlay label

        self.initialize_ui()

    def initialize_ui(self):
        title_label = tk.Label(self.root, text="Image to PDF", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_images_button.pack(pady=(0, 10))

        # Create a frame to contain the canvas and scrollbar
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Create a canvas widget with a vertical scrollbar
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to contain the thumbnails
        self.thumbnail_frame = tk.Frame(self.canvas, bg="white")  
        self.canvas.create_window((0, 0), window=self.thumbnail_frame, anchor=tk.NW)

        label = tk.Label(self.root, text="Enter Output PDF name:")
        label.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify='center')
        pdf_name_entry.pack()

        convert_button = tk.Button(self.root, text="Convert PDF", command=self.start_conversion_thread)
        convert_button.pack(pady=(20, 40))

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images",
                                                        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        # Clear previous thumbnails in the frame
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()

        for image_path in self.image_paths:
            # Create a frame for the thumbnail
            thumbnail_frame = tk.Frame(self.thumbnail_frame, pady=10, bg="white")
            thumbnail_frame.pack(fill=tk.X)

            # Display thumbnail image on the left
            img = Image.open(image_path)
            img.thumbnail((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            thumbnail_label = tk.Label(thumbnail_frame, image=img_tk)
            thumbnail_label.image = img_tk  

            # Bind mouse wheel event to the thumbnail frame
            thumbnail_frame.bind("<MouseWheel>", lambda event: self.on_mousewheel(event, self.canvas))

            thumbnail_label.pack(side=tk.LEFT, padx=(10, 20))

            # Display image name on the right
            _, filename = os.path.split(image_path)
            filename_label = tk.Label(thumbnail_frame, text=filename)
            filename_label.pack(side=tk.LEFT, padx=(10, 20))

        # Update canvas scroll region
        self.thumbnail_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event, canvas):
        canvas.yview_scroll(-1*(event.delta//120), "units")

    def start_conversion_thread(self):
        # Show overlay with loading message
        self.show_overlay("Processing images... Please wait.")

        # Start conversion in a separate thread
        convert_thread = threading.Thread(target=self.convert_images_to_pdf_with_loader)
        convert_thread.start()

    def show_overlay(self, message, width=30, height=10):
    # Create or update the overlay label with the given message
        if self.overlay_label:
            self.overlay_label.config(text=message, width=width, height=height)
        else:
            # Create the main overlay label
            self.overlay_label = tk.Label(self.root, text=message, bg="grey", fg="white", font=("Helvetica", 12), width=width, height=height)
            self.overlay_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
           

    def hide_overlay(self):
        # Remove the overlay label
        if self.overlay_label:
            self.overlay_label.destroy()
            self.overlay_label = None

    def convert_images_to_pdf_with_loader(self):
        if not self.image_paths:
            return
        
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"

        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))

        for image_path in self.image_paths:
            img = Image.open(image_path)
            available_width = 540
            available_height = 720
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            x_centered = (612 - new_width) / 2
            y_centered = (792 - new_height) / 2

            pdf.setFillColorRGB(255, 255, 255)
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(img, x_centered, y_centered, width=new_width, height=new_height)
            pdf.showPage()

        pdf.save()

        # Hide overlay and display process complete message
        self.hide_overlay()
        self.show_overlay("PDF creation finished.")
        # Destroy overlay after 2 seconds
        self.root.after(2000, self.hide_overlay)


def main():
    root = tk.Tk()
    root.title("Image 2 PDF")
    root.geometry("400x600")
    converter = ImageToPdfConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
