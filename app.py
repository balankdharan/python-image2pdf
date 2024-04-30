import tkinter as tk
from tkinter import filedialog
import os


# class to convert 

class ImageToPdfConverter:
    def __init__(self,root):
        self.root = root
        self.image_path = []
        self.output_pdf_name =tk.StringVar()
        self.selected_images_listbox =tk.Listbox(root, selectmode=tk.MULTIPLE)

        self.initialize_ui()
    def initialize_ui(self):
        title_label =tk.Label(self.root, text="Image to PDF", font=("Helvetica",16,"bold"))
        title_label.pack(pady=10)

def main():
    root= tk.Tk()
    root.title("Image 2 PDF")
    root.geometry("400x600")
    root.mainloop()

if __name__ == "__main__":
    main()
