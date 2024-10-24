import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import os
import re
import io
from PIL import Image
import pytesseract

# Configure Tesseract path (IMPORTANT: Change this!)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path

class PDFSplitterApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Splitter")

        self.pdf_file_path = ""
        self.output_dir = ""

        # --- File and Directory Selection UI ---
        self.label_pdf = tk.Label(master, text="Select PDF File:")
        self.label_pdf.grid(row=0, column=0, padx=5, pady=5)

        self.entry_pdf = tk.Entry(master, width=50)
        self.entry_pdf.grid(row=0, column=1, padx=5, pady=5)

        self.button_browse_pdf = tk.Button(master, text="Browse", command=self.browse_pdf)
        self.button_browse_pdf.grid(row=0, column=2, padx=5, pady=5)

        self.label_output = tk.Label(master, text="Output Directory:")
        self.label_output.grid(row=1, column=0, padx=5, pady=5)

        self.entry_output = tk.Entry(master, width=50)
        self.entry_output.grid(row=1, column=1, padx=5, pady=5)

        self.button_browse_output = tk.Button(master, text="Browse", command=self.browse_output)
        self.button_browse_output.grid(row=1, column=2, padx=5, pady=5)

        self.button_split = tk.Button(master, text="Split PDF", command=self.split_pdf)
        self.button_split.grid(row=2, column=1, padx=5, pady=10)

    def browse_pdf(self):
        self.pdf_file_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select PDF File",
            filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*")),
        )
        self.entry_pdf.delete(0, tk.END)
        self.entry_pdf.insert(0, self.pdf_file_path)

    def browse_output(self):
        self.output_dir = filedialog.askdirectory(initialdir="/", title="Select Output Directory")
        self.entry_output.delete(0, tk.END)
        self.entry_output.insert(0, self.output_dir)

    def split_pdf(self):
        if not self.pdf_file_path or not self.output_dir:
            messagebox.showerror("Error", "Please select a PDF file and output directory.")
            return

        x_coord = 415  # Adjust these values if needed
        y_coord = 120
        area_width = 127
        area_height = 25

        try:
            highlight_and_save_pdfs(
                self.pdf_file_path, x_coord, y_coord, area_width, area_height, self.output_dir
            )
            messagebox.showinfo("Success", "PDF split complete!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def highlight_and_save_pdfs(pdf_path, x, y, width, height, output_dir):
    """
    Highlights a specific location on each page of a PDF with a rectangle
    and saves each page as a separate file named 'tempfile_page_{page_number}.pdf'.

    Args:
        pdf_path: Path to the PDF file.
        x: The x-coordinate of the top-left corner of the area.
        y: The y-coordinate of the top-left corner of the area.
        width: The width of the area.
        height: The height of the area.
        output_dir: The directory to save the highlighted PDF files.
    """
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc[page_num]
        rect = fitz.Rect(x, y, x + width, y + height)

        # Draw rectangle around the specified area
        highlight = page.add_highlight_annot(rect) 
        highlight.update()

        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Save the page as a separate PDF file
        output_pdf_path = os.path.join(output_dir, f"tempfile_page_{page_num + 1}.pdf")
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        new_doc.save(output_pdf_path)

# --- Main Application ---
root = tk.Tk()
app = PDFSplitterApp(root)
root.mainloop()