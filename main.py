import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
import PyPDF2
import fitz
from PIL import Image, ImageTk
import io

def combine_pdfs(pdf_list, output_path):
    pdf_merger = PyPDF2.PdfMerger()

    for pdf in pdf_list:
        try:
            pdf_merger.append(pdf)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add {pdf}: {e}")
            return

    try:
        with open(output_path, 'wb') as output_file:
            pdf_merger.write(output_file)
        messagebox.showinfo("Success", "PDF files combined successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write output file: {e}")

def select_files():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if files:
        file_list.delete(0, tk.END)
        for file in files:
            file_list.insert(tk.END, file)
            file_list.see(tk.END)
        preview_pdf(files[0])

def save_combined_pdf():
    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if output_file:
        pdf_files = file_list.get(0, tk.END)
        if pdf_files:
            combine_pdfs(pdf_files, output_file)
        else:
            messagebox.showwarning("Warning", "No PDF files selected")

def move_up():
    try:
        selected_indices = file_list.curselection()
        for index in selected_indices:
            if index == 0:
                return
            file = file_list.get(index)
            file_list.delete(index)
            file_list.insert(index - 1, file)
            file_list.select_set(index - 1)
            file_list.see(index - 1)
    except:
        pass

def move_down():
    try:
        selected_indices = file_list.curselection()
        for index in reversed(selected_indices):
            if index == file_list.size() - 1:
                return
            file = file_list.get(index)
            file_list.delete(index)
            file_list.insert(index + 1, file)
            file_list.select_set(index + 1)
            file_list.see(index + 1)
    except:
        pass

def preview_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        img = img.resize((200, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        preview_label.config(image=img_tk)
        preview_label.image = img_tk
    except Exception as e:
        messagebox.showerror("Error", f"Failed to preview PDF: {e}")

def on_file_list_select(event):
    selected_index = file_list.curselection()
    if selected_index:
        selected_pdf = file_list.get(selected_index)
        preview_pdf(selected_pdf)

def on_drop(event):
    files = app.tk.splitlist(event.data)
    for file in files:
        if file.endswith('.pdf'):
            file_list.insert(tk.END, file)
            file_list.see(tk.END)
    if files:
        preview_pdf(files[0])

app = TkinterDnD.Tk()
app.title("PDF Combiner")

frame = tk.Frame(app)
frame.pack(pady=20, padx=20)

select_button = tk.Button(frame, text="Select PDF Files", command=select_files)
select_button.pack()

file_list = tk.Listbox(frame, selectmode=tk.SINGLE, width=50, height=10)
file_list.pack(pady=10)
file_list.bind('<<ListboxSelect>>', on_file_list_select)

button_frame = tk.Frame(frame)
button_frame.pack(pady=10)

up_button = tk.Button(button_frame, text="Move Up", command=move_up)
up_button.grid(row=0, column=0, padx=5)

down_button = tk.Button(button_frame, text="Move Down", command=move_down)
down_button.grid(row=0, column=1, padx=5)

combine_button = tk.Button(frame, text="Combine PDFs", command=save_combined_pdf)
combine_button.pack()

preview_frame = tk.Frame(app)
preview_frame.pack(pady=10)

preview_label = tk.Label(preview_frame, text="PDF Preview", width=40, height=15, bg="gray")
preview_label.pack()
preview_label.config(width=300, height=400)

app.drop_target_register(DND_FILES)
app.dnd_bind('<<Drop>>', on_drop)

app.mainloop()
