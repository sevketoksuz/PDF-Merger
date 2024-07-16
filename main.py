import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

def combine_pdfs(pdf_list, output_path):
    pdf_merger = PyPDF2.PdfFileMerger()

    for pdf in pdf_list:
        pdf_merger.append(pdf)

    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)

def select_files():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if files:
        file_list.delete(0, tk.END)
        for file in files:
            file_list.insert(tk.END, file)

def save_combined_pdf():
    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if output_file:
        pdf_files = file_list.get(0, tk.END)
        if pdf_files:
            combine_pdfs(pdf_files, output_file)
            messagebox.showinfo("Success", "PDF files combined successfully!")
        else:
            messagebox.showwarning("Warning", "No PDF files selected")

app = tk.Tk()
app.title("PDF Combiner")

frame = tk.Frame(app)
frame.pack(pady=20, padx=20)

select_button = tk.Button(frame, text="Select PDF Files", command=select_files)
select_button.pack()

file_list = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=50, height=10)
file_list.pack(pady=10)

combine_button = tk.Button(frame, text="Combine PDFs", command=save_combined_pdf)
combine_button.pack()

app.mainloop()
