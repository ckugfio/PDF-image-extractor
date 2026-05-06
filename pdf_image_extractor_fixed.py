import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import fitz  # PyMuPDF
from PIL import Image
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD


class PDFImageExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor de Imágenes de PDF")
        self.root.geometry("800x650")
        self.root.configure(bg='#f0f0f0')
        self.root.minsize(750, 600)
        
        self.pdf_files = []
        self.output_path = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.image_format = tk.StringVar(value="PNG")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Título
        title_label = tk.Label(self.root, text="Extractor de Imágenes de PDF", 
                               font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=15)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear dos columnas principales
        left_column = ttk.Frame(main_frame)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_column = ttk.Frame(main_frame)
        right_column.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # COLUMNA IZQUIERDA: Archivos y configuración
        
        # Área de arrastre de archivos
        self.drop_frame = tk.Frame(left_column, height=100, bg='#e0e0e0', 
                                   relief=tk.RIDGE, borderwidth=2)
        self.drop_frame.pack(fill=tk.X, pady=(0, 15))
        self.drop_frame.pack_propagate(False)
        
        drop_label = tk.Label(self.drop_frame, 
                             text="Arrastra archivos PDF aquí o haz clic para seleccionar",
                             font=("Arial", 11), bg='#e0e0e0')
        drop_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Configurar drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_frame.bind('<Button-1>', self.browse_files)
        
        # Lista de archivos
        files_frame = ttk.LabelFrame(left_column, text="Archivos PDF seleccionados", padding="8")
        files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(files_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(files_frame, yscrollcommand=scrollbar.set, height=8)
        self.files_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        # Botones de archivo (en una fila)
        file_buttons_frame = ttk.Frame(left_column)
        file_buttons_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(file_buttons_frame, text="Seleccionar Archivos", 
                  command=self.browse_files).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(file_buttons_frame, text="Seleccionar Carpeta", 
                  command=self.browse_folder).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(file_buttons_frame, text="Limpiar Lista", 
                  command=self.clear_files).pack(side=tk.LEFT)
        
        # Configuración de salida
        config_frame = ttk.LabelFrame(left_column, text="Configuración de Salida", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Ruta de salida
        output_frame = ttk.Frame(config_frame)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(output_frame, text="Carpeta de salida:").pack(anchor=tk.W)
        self.output_display = tk.Label(output_frame, text=f"{self.output_path.get()}", 
                                     font=("Arial", 9), bg='#f0f0f0', fg='#666666', wraplength=400, anchor=tk.W)
        self.output_display.pack(fill=tk.X, pady=(2, 0))
        
        # Formato de imagen y botón de selección en la misma fila
        format_frame = ttk.Frame(config_frame)
        format_frame.pack(fill=tk.X)
        
        ttk.Label(format_frame, text="Formato:").pack(side=tk.LEFT)
        ttk.Radiobutton(format_frame, text="PNG", variable=self.image_format, 
                       value="PNG").pack(side=tk.LEFT, padx=(10, 15))
        ttk.Radiobutton(format_frame, text="JPG", variable=self.image_format, 
                       value="JPG").pack(side=tk.LEFT, padx=(0, 20))
        
        # Botón para seleccionar carpeta de salida
        select_output_btn = tk.Button(format_frame, text="Seleccionar Carpeta", 
                                      command=self.select_output_folder, width=18,
                                      bg='#4CAF50', fg='white', font=("Arial", 9, "bold"))
        select_output_btn.pack(side=tk.RIGHT)
        
        # Botón para iniciar proceso fuera de configuración
        self.start_btn = tk.Button(left_column, text="INICIAR PROCESO DE EXTRACCIÓN", 
                                   command=self.start_process, height=2,
                                   bg='#2196F3', fg='white', font=("Arial", 11, "bold"))
        self.start_btn.pack(fill=tk.X, pady=(15, 0))
        
        # COLUMNA DERECHA: Espacio libre (eliminado)
        
        # Frame inferior solo para barra de progreso
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(15, 0))
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(bottom_frame, variable=self.progress_var, 
                                           maximum=100, length=750)
        self.progress_bar.pack()
        
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for file_path in files:
            if file_path.lower().endswith('.pdf'):
                if file_path not in self.pdf_files:
                    self.pdf_files.append(file_path)
                    self.files_listbox.insert(tk.END, os.path.basename(file_path))
        
    def browse_files(self, event=None):
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        for file_path in files:
            if file_path not in self.pdf_files:
                self.pdf_files.append(file_path)
                self.files_listbox.insert(tk.END, os.path.basename(file_path))
    
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta con PDFs")
        if folder:
            for file_name in os.listdir(folder):
                if file_name.lower().endswith('.pdf'):
                    file_path = os.path.join(folder, file_name)
                    if file_path not in self.pdf_files:
                        self.pdf_files.append(file_path)
                        self.files_listbox.insert(tk.END, file_name)
    
    def select_output_folder(self):
        """Selecciona la carpeta de salida y la muestra en la interfaz"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta donde se guardarán los archivos")
        if folder:
            self.output_path.set(folder)
            self.output_display.config(text=f"Carpeta de salida: {folder}")
    
    def start_process(self):
        """Inicia el proceso de extracción de imágenes"""
        if not self.pdf_files:
            messagebox.showerror("Error", "Por favor selecciona al menos un archivo PDF")
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Por favor selecciona una carpeta de salida")
            return
        
        # Deshabilitar botón durante el proceso
        self.start_btn.config(state="disabled", text="PROCESANDO... ESPERE")
        
        output_folder = self.output_path.get()
        if not os.path.exists(output_folder):
            try:
                os.makedirs(output_folder)
            except Exception as e:
                messagebox.showerror("Error", f"No se puede crear la carpeta de salida: {e}")
                self.start_btn.config(state="normal", text="INICIAR PROCESO DE EXTRACCIÓN")
                return
        
        # Ejecutar en un hilo separado para no bloquear la interfaz
        thread = threading.Thread(target=self._extract_images_thread, args=(output_folder,))
        thread.daemon = True
        thread.start()
    
    def clear_all(self):
        """Limpia toda la interfaz"""
        self.pdf_files.clear()
        self.files_listbox.delete(0, tk.END)
        self.progress_var.set(0)
        # status_label eliminada, no se actualiza
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if folder:
            self.output_path.set(folder)
            self.output_display.config(text=f"Carpeta de salida: {folder}")
    
    def clear_files(self):
        self.pdf_files.clear()
        self.files_listbox.delete(0, tk.END)
        self.progress_var.set(0)
        # status_label eliminada, no se actualiza
    
    def extract_images(self):
        """Método antiguo mantenido por compatibilidad"""
        self.start_process()
    
    def _extract_images_thread(self, output_folder):
        total_files = len(self.pdf_files)
        
        for i, pdf_path in enumerate(self.pdf_files):
            try:
                # Actualizar estado - status_label eliminada
                # self.root.after(0, lambda p=pdf_path: self.status_label.config(text=f"Procesando: {os.path.basename(p)}"))
                
                # Crear carpeta para este PDF
                pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
                pdf_output_folder = os.path.join(output_folder, pdf_name)
                os.makedirs(pdf_output_folder, exist_ok=True)
                
                # Extraer imágenes del PDF
                self._extract_from_pdf(pdf_path, pdf_output_folder)
                
                # Actualizar progreso
                progress = ((i + 1) / total_files) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                
            except Exception as e:
                self.root.after(0, lambda err=str(e): messagebox.showerror("Error", f"Error procesando {os.path.basename(pdf_path)}: {err}"))
                self.root.after(0, lambda: self.start_btn.config(state="normal", text="INICIAR PROCESO DE EXTRACCIÓN"))
        
        # Finalizar - status_label eliminada
        # self.root.after(0, lambda: self.status_label.config(text="¡Proceso completado!"))
        self.root.after(0, lambda: self.start_btn.config(state="normal", text="INICIAR PROCESO DE EXTRACCIÓN"))
        self.root.after(0, lambda: messagebox.showinfo("Completado", f"Se han procesado {total_files} archivos PDF"))
    
    def _extract_from_pdf(self, pdf_path, output_folder):
        pdf_document = fitz.open(pdf_path)
        image_count = 0
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # Extraer imágenes de la página
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                # Obtener la imagen
                xref = img[0]
                pix = fitz.Pixmap(pdf_document, xref)
                
                if pix.n - pix.alpha < 4:  # GRAY o RGB
                    # Guardar imagen
                    image_count += 1
                    image_format = self.image_format.get().lower()
                    
                    if image_format == 'jpg':
                        # Convertir a RGB para JPG
                        if pix.n > 3:  # RGBA
                            pix = fitz.Pixmap(fitz.csRGB, pix)
                        
                        img_data = pix.tobytes("jpeg")
                        filename = f"{image_count}.jpg"
                    else:
                        img_data = pix.tobytes("png")
                        filename = f"{image_count}.png"
                    
                    output_path = os.path.join(output_folder, filename)
                    with open(output_path, "wb") as img_file:
                        img_file.write(img_data)
                
                pix = None
        
        pdf_document.close()
        
        if image_count == 0:
            # Si no se encontraron imágenes, crear imágenes de las páginas
            self._create_page_images(pdf_path, output_folder)
    
    def _create_page_images(self, pdf_path, output_folder):
        pdf_document = fitz.open(pdf_path)
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # Renderizar página como imagen
            mat = fitz.Matrix(2.0, 2.0)  # Escalar para mejor calidad
            pix = page.get_pixmap(matrix=mat)
            
            image_format = self.image_format.get().lower()
            page_num_str = str(page_num + 1)
            
            if image_format == 'jpg':
                if pix.n > 3:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                img_data = pix.tobytes("jpeg")
                filename = f"{page_num_str}.jpg"
            else:
                img_data = pix.tobytes("png")
                filename = f"{page_num_str}.png"
            
            output_path = os.path.join(output_folder, filename)
            with open(output_path, "wb") as img_file:
                img_file.write(img_data)
            
            pix = None
        
        pdf_document.close()


def main():
    root = TkinterDnD.Tk()
    app = PDFImageExtractor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
