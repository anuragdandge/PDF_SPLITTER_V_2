# import fitz  # PyMuPDF
# import tkinter as tk
# from tkinter import filedialog, messagebox
# from PIL import Image, ImageTk

# class PDFDisplayWindow:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("PDF Display")
#         self.canvas = tk.Canvas(master, cursor="cross")
#         self.canvas.pack(fill=tk.BOTH, expand=True)
#         self.canvas.bind("<ButtonPress-1>", self.on_button_press)
#         self.canvas.bind("<B1-Motion>", self.on_move_press)
#         self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
#         self.rect = None
#         self.start_x = None
#         self.start_y = None
#         self.end_x = None
#         self.end_y = None
#         self.image = None

#     def display_pdf(self, pdf_path):
#         doc = fitz.open(pdf_path)
#         page = doc.load_page(0)
#         pix = page.get_pixmap()
#         img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#         self.image = ImageTk.PhotoImage(image=img)
#         self.canvas.config(width=img.width, height=img.height)
#         self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
    
#     def on_button_press(self, event):
#         self.start_x = event.x
#         self.start_y = event.y
#         if not self.rect:
#             self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red')
        
#     def on_move_press(self, event):
#         cur_x, cur_y = (event.x, event.y)
#         self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
    
#     def on_button_release(self, event):
#         self.end_x = event.x
#         self.end_y = event.y
    
#     def extract_coordinates(self):
#         if self.rect:
#             x1, y1, x2, y2 = self.canvas.coords(self.rect)
#             return x1, y1, x2, y2
#         return None

# class ButtonControlWindow:
#     def __init__(self, master, pdf_display_window):
#         self.master = master
#         self.master.title("Control Panel")
#         self.pdf_display_window = pdf_display_window
#         self.pdf_file_path = ""
        
#         # Buttons
#         self.load_pdf_button = tk.Button(master, text="Load PDF", command=self.load_pdf)
#         self.load_pdf_button.pack(side=tk.TOP, padx=10, pady=5)
        
#         self.extract_coords_button = tk.Button(master, text="Extract Coordinates", command=self.extract_coordinates)
#         self.extract_coords_button.pack(side=tk.TOP, padx=10, pady=5)
        
#     def load_pdf(self):
#         self.pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
#         if self.pdf_file_path:
#             self.pdf_display_window.display_pdf(self.pdf_file_path)
    
#     def extract_coordinates(self):
#         coords = self.pdf_display_window.extract_coordinates()
#         if coords:
#             x1, y1, x2, y2 = coords
#             messagebox.showinfo("Coordinates", f"Start: ({x1}, {y1})\nEnd: ({x2}, {y2})")
#         else:
#             messagebox.showerror("Error", "No rectangle drawn!")

# # Create two separate windows
# root_pdf = tk.Tk()
# root_control = tk.Tk()

# pdf_display_window = PDFDisplayWindow(root_pdf)
# button_control_window = ButtonControlWindow(root_control, pdf_display_window)

# # Start both windows
# root_pdf.mainloop()
# root_control.mainloop()
# ----------------v2----------------------
# import fitz  # PyMuPDF
# import tkinter as tk
# from tkinter import filedialog, messagebox
# from PIL import Image, ImageTk

# class PDFDisplayWindow:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("PDF Display")
#         self.canvas = tk.Canvas(master, cursor="cross")
#         self.canvas.pack(fill=tk.BOTH, expand=True)
#         self.canvas.bind("<ButtonPress-1>", self.on_button_press)
#         self.canvas.bind("<B1-Motion>", self.on_move_press)
#         self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
#         self.rect = None
#         self.start_x = None
#         self.start_y = None
#         self.end_x = None
#         self.end_y = None
#         self.image = None

#     def display_pdf(self, pdf_path):
#         doc = fitz.open(pdf_path)
#         page = doc.load_page(0)
#         pix = page.get_pixmap()
#         img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#         self.image = ImageTk.PhotoImage(image=img)
#         self.canvas.config(width=img.width, height=img.height)
#         self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
    
#     def on_button_press(self, event):
#         self.start_x = event.x
#         self.start_y = event.y
#         if not self.rect:
#             self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red')
        
#     def on_move_press(self, event):
#         cur_x, cur_y = (event.x, event.y)
#         self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
    
#     def on_button_release(self, event):
#         self.end_x = event.x
#         self.end_y = event.y
    
#     def extract_coordinates(self):
#         if self.rect:
#             x1, y1, x2, y2 = self.canvas.coords(self.rect)
#             return x1, y1, x2, y2
#         return None

# class ButtonControlWindow:
#     def __init__(self, master, pdf_display_window):
#         self.master = master
#         self.master.title("Control Panel")
#         self.pdf_display_window = pdf_display_window
#         self.pdf_file_path = ""
        
#         # Buttons
#         self.load_pdf_button = tk.Button(master, text="Load PDF", command=self.load_pdf)
#         self.load_pdf_button.pack(side=tk.TOP, padx=10, pady=5)
        
#         self.extract_coords_button = tk.Button(master, text="Extract Coordinates", command=self.extract_coordinates)
#         self.extract_coords_button.pack(side=tk.TOP, padx=10, pady=5)
        
#     def load_pdf(self):
#         self.pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
#         if self.pdf_file_path:
#             self.pdf_display_window.display_pdf(self.pdf_file_path)
    
#     def extract_coordinates(self):
#         coords = self.pdf_display_window.extract_coordinates()
#         if coords:
#             x1, y1, x2, y2 = coords
#             messagebox.showinfo("Coordinates", f"Start: ({x1}, {y1})\nEnd: ({x2}, {y2})")
#         else:
#             messagebox.showerror("Error", "No rectangle drawn!")

# # Create two separate windows
# root_pdf = tk.Tk()
# root_control = tk.Tk()

# pdf_display_window = PDFDisplayWindow(root_pdf)
# button_control_window = ButtonControlWindow(root_control, pdf_display_window)

# # Start both windows
# root_pdf.mainloop()
# root_control.mainloop()
# ---------------------------v3---------------------------------
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class PDFDisplayWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Display")
        self.canvas = tk.Canvas(master, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.image = None

    def display_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.image = ImageTk.PhotoImage(image=img)
        self.canvas.config(width=img.width, height=img.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
    
    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red')
        
    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
    
    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
    
    def extract_coordinates(self):
        if self.rect:
            x1, y1, x2, y2 = self.canvas.coords(self.rect)
            width = x2 - x1
            height = y2 - y1
            return x1, y1, width, height
        return None

class ButtonControlWindow:
    def __init__(self, master, pdf_display_window):
        self.master = master
        self.master.title("Control Panel")
        self.pdf_display_window = pdf_display_window
        self.pdf_file_path = ""
        
        # Buttons
        self.load_pdf_button = tk.Button(master, text="Load PDF", command=self.load_pdf)
        self.load_pdf_button.pack(side=tk.TOP, padx=10, pady=5)
        
        self.extract_coords_button = tk.Button(master, text="Extract Coordinates", command=self.extract_coordinates)
        self.extract_coords_button.pack(side=tk.TOP, padx=10, pady=5)
        
    def load_pdf(self):
        self.pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_file_path:
            self.pdf_display_window.display_pdf(self.pdf_file_path)
    
    def extract_coordinates(self):
        coords = self.pdf_display_window.extract_coordinates()
        if coords:
            x1, y1, width, height = coords
            print(f"Coordinates: x={x1}, y={y1}, width={width}, height={height}")
            messagebox.showinfo("Coordinates", f"Start: ({x1}, {y1})\nWidth: {width}\nHeight: {height}")
        else:
            messagebox.showerror("Error", "No rectangle drawn!")

# Create two separate windows
root_pdf = tk.Tk()
root_control = tk.Tk()

pdf_display_window = PDFDisplayWindow(root_pdf)
button_control_window = ButtonControlWindow(root_control, pdf_display_window)

# Start both windows
root_pdf.mainloop()
root_control.mainloop()
