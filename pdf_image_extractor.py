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
        
        # Language dictionary
        self.translations = {
            'en': {
                'title': 'PDF Image Extractor',
                'drag_drop': 'Drag PDF files here or click to select',
                'selected_files': 'Selected PDF Files',
                'select_files': 'Select Files',
                'select_folder': 'Select Folder',
                'clear_list': 'Clear List',
                'output_config': 'Output Configuration',
                'output_folder': 'Output folder:',
                'format': 'Format:',
                'png': 'PNG',
                'jpg': 'JPG',
                'select_folder_btn': 'Select Folder',
                'start_process': 'START EXTRACTION PROCESS',
                'processing': 'PROCESSING... PLEASE WAIT',
                'error_no_files': 'Please select at least one PDF file',
                'error_no_output': 'Please select an output folder',
                'error_create_folder': 'Cannot create output folder',
                'completed': 'Completed',
                'process_completed': 'Processed {count} PDF files',
                'language': 'Language:',
                'spanish': 'Spanish',
                'english': 'English'
            },
            'es': {
                'title': 'Extractor de Imágenes de PDF',
                'drag_drop': 'Arrastra archivos PDF aquí o haz clic para seleccionar',
                'selected_files': 'Archivos PDF seleccionados',
                'select_files': 'Seleccionar Archivos',
                'select_folder': 'Seleccionar Carpeta',
                'clear_list': 'Limpiar Lista',
                'output_config': 'Configuración de Salida',
                'output_folder': 'Carpeta de salida:',
                'format': 'Formato:',
                'png': 'PNG',
                'jpg': 'JPG',
                'select_folder_btn': 'Seleccionar Carpeta',
                'start_process': 'INICIAR PROCESO DE EXTRACCIÓN',
                'processing': 'PROCESANDO... ESPERE',
                'error_no_files': 'Por favor selecciona al menos un archivo PDF',
                'error_no_output': 'Por favor selecciona una carpeta de salida',
                'error_create_folder': 'No se puede crear la carpeta de salida',
                'completed': 'Completado',
                'process_completed': 'Se han procesado {count} archivos PDF',
                'language': 'Idioma:',
                'spanish': 'Español',
                'english': 'Inglés'
            }
        }
        
        # Default language is English
        self.current_language = tk.StringVar(value='en')
        
        self.root.title(self.translations['en']['title'])
        self.root.geometry("500x750")
        self.root.configure(bg='#f0f0f0')
        self.root.minsize(450, 700)
        
        self.pdf_files = []
        self.output_path = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.image_format = tk.StringVar(value="PNG")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Título
        self.title_label = tk.Label(self.root, text=self.translations[self.current_language.get()]['title'], 
                               font=("Arial", 16, "bold"), bg='#f0f0f0')
        self.title_label.pack(pady=15)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear dos columnas principales
        left_column = ttk.Frame(main_frame)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_column = ttk.Frame(main_frame)
        right_column.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # COLUMNA IZQUIERDA: Archivos y configuración
        
        # Language selection
        language_frame = ttk.Frame(left_column)
        language_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Center container for language selection
        center_frame = ttk.Frame(language_frame)
        center_frame.pack(expand=True)
        
        self.language_label = ttk.Label(center_frame, text=self.translations[self.current_language.get()]['language'])
        self.language_label.pack(side=tk.LEFT)
        self.spanish_radio = ttk.Radiobutton(center_frame, text=self.translations[self.current_language.get()]['spanish'], 
                       variable=self.current_language, value="es",
                       command=self.change_language)
        self.spanish_radio.pack(side=tk.LEFT, padx=(10, 5))
        self.english_radio = ttk.Radiobutton(center_frame, text=self.translations[self.current_language.get()]['english'], 
                       variable=self.current_language, value="en",
                       command=self.change_language)
        self.english_radio.pack(side=tk.LEFT)
        
        # Área de arrastre de archivos
        self.drop_frame = tk.Frame(left_column, height=100, bg='#e0e0e0', 
                                   relief=tk.RIDGE, borderwidth=2)
        self.drop_frame.pack(fill=tk.X, pady=(0, 15))
        self.drop_frame.pack_propagate(False)
        
        self.drop_label = tk.Label(self.drop_frame, 
                             text=self.translations[self.current_language.get()]['drag_drop'],
                             font=("Arial", 11), bg='#e0e0e0')
        self.drop_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Configurar drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_frame.bind('<Button-1>', self.browse_files)
        
        # Lista de archivos
        files_frame = ttk.LabelFrame(left_column, text=self.translations[self.current_language.get()]['selected_files'], padding="8")
        self.files_label = files_frame
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
        
        self.select_folder_file_btn = tk.Button(file_buttons_frame, text=self.translations[self.current_language.get()]['select_folder'], 
                command=self.browse_folder, width=18,
                bg='#4CAF50', fg='white', font=("Arial", 9, "bold"))
        self.select_folder_file_btn.pack(side=tk.LEFT, padx=(0, 8))
        self.clear_list_btn = tk.Button(file_buttons_frame, text=self.translations[self.current_language.get()]['clear_list'], 
                command=self.clear_files, width=18,
                bg='#f44336', fg='white', font=("Arial", 9, "bold"))
        self.clear_list_btn.pack(side=tk.LEFT)
        
        # Configuración de salida
        config_frame = ttk.LabelFrame(left_column, text=self.translations[self.current_language.get()]['output_config'], padding="10")
        self.config_label = config_frame
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Ruta de salida
        output_frame = ttk.Frame(config_frame)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.output_label = ttk.Label(output_frame, text=self.translations[self.current_language.get()]['output_folder'])
        self.output_label.pack(anchor=tk.W)
        self.output_display = tk.Label(output_frame, text=f"{self.output_path.get()}", 
                                     font=("Arial", 9), bg='#f0f0f0', fg='#666666', wraplength=400, anchor=tk.W)
        self.output_display.pack(fill=tk.X, pady=(2, 0))
        
        # Formato de imagen y botón de selección en la misma fila
        format_frame = ttk.Frame(config_frame)
        format_frame.pack(fill=tk.X)
        
        self.format_label = ttk.Label(format_frame, text=self.translations[self.current_language.get()]['format'])
        self.format_label.pack(side=tk.LEFT)
        self.png_radio = ttk.Radiobutton(format_frame, text=self.translations[self.current_language.get()]['png'], variable=self.image_format, 
                       value="PNG")
        self.png_radio.pack(side=tk.LEFT, padx=(10, 15))
        self.jpg_radio = ttk.Radiobutton(format_frame, text=self.translations[self.current_language.get()]['jpg'], variable=self.image_format, 
                       value="JPG")
        self.jpg_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        # Botón para seleccionar carpeta de salida
        self.select_folder_btn = tk.Button(format_frame, text=self.translations[self.current_language.get()]['select_folder_btn'], 
                                      command=self.select_output_folder, width=18,
                                      bg='#4CAF50', fg='white', font=("Arial", 9, "bold"))
        self.select_folder_btn.pack(side=tk.RIGHT)
        
        # Botón para iniciar proceso fuera de configuración
        self.start_btn = tk.Button(left_column, text=self.translations[self.current_language.get()]['start_process'], 
                                   command=self.start_process, height=2,
                                   bg='#2196F3', fg='white', font=("Arial", 11, "bold"))
        self.start_btn.pack(fill=tk.X, pady=(15, 10))
        
        # Barra de progreso debajo del botón de inicio
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(left_column, variable=self.progress_var, 
                                           maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 15))
        
        # COLUMNA DERECHA: Espacio libre (eliminado)
        
    def change_language(self):
        """Change the interface language"""
        lang = self.current_language.get()
        self.root.title(self.translations[lang]['title'])
        self.title_label.config(text=self.translations[lang]['title'])
        self.update_ui_text()
    
    def update_ui_text(self):
        """Update all UI text elements with the current language"""
        lang = self.current_language.get()
        
        # Update language selection labels
        self.language_label.config(text=self.translations[lang]['language'])
        self.spanish_radio.config(text=self.translations[lang]['spanish'])
        self.english_radio.config(text=self.translations[lang]['english'])
        
        # Update drop area label
        self.drop_label.config(text=self.translations[lang]['drag_drop'])
        
        # Update other labels and buttons
        self.files_label.config(text=self.translations[lang]['selected_files'])
        self.config_label.config(text=self.translations[lang]['output_config'])
        self.output_label.config(text=self.translations[lang]['output_folder'])
        self.format_label.config(text=self.translations[lang]['format'])
        
        # Update radio buttons for format
        self.png_radio.config(text=self.translations[lang]['png'])
        self.jpg_radio.config(text=self.translations[lang]['jpg'])
        
        # Update buttons
        self.select_folder_btn.config(text=self.translations[lang]['select_folder_btn'])
        self.start_btn.config(text=self.translations[lang]['start_process'])
        
        # Update file buttons
        self.select_folder_file_btn.config(text=self.translations[lang]['select_folder'])
        self.clear_list_btn.config(text=self.translations[lang]['clear_list'])
        
        # Update output display
        current_output = self.output_path.get()
        self.output_display.config(text=f"{self.translations[lang]['output_folder']} {current_output}")
    
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for file_path in files:
            if file_path.lower().endswith('.pdf'):
                if file_path not in self.pdf_files:
                    self.pdf_files.append(file_path)
                    self.files_listbox.insert(tk.END, os.path.basename(file_path))
        
    def browse_files(self, event=None):
        files = filedialog.askopenfilenames(
            title=self.translations[self.current_language.get()]['select_files'],
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        for file_path in files:
            if file_path not in self.pdf_files:
                self.pdf_files.append(file_path)
                self.files_listbox.insert(tk.END, os.path.basename(file_path))
    
    def browse_folder(self):
        folder = filedialog.askdirectory(title=self.translations[self.current_language.get()]['select_folder'])
        if folder:
            for file_name in os.listdir(folder):
                if file_name.lower().endswith('.pdf'):
                    file_path = os.path.join(folder, file_name)
                    if file_path not in self.pdf_files:
                        self.pdf_files.append(file_path)
                        self.files_listbox.insert(tk.END, file_name)
    
    def select_output_folder(self):
        """Selecciona la carpeta de salida y la muestra en la interfaz"""
        folder = filedialog.askdirectory(title=self.translations[self.current_language.get()]['select_folder_btn'])
        if folder:
            self.output_path.set(folder)
            self.output_display.config(text=f"{self.translations[self.current_language.get()]['output_folder']} {folder}")
    
    def start_process(self):
        """Inicia el proceso de extracción de imágenes"""
        if not self.pdf_files:
            messagebox.showerror("Error", self.translations[self.current_language.get()]['error_no_files'])
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", self.translations[self.current_language.get()]['error_no_output'])
            return
        
        # Deshabilitar botón durante el proceso
        self.start_btn.config(state="disabled", text=self.translations[self.current_language.get()]['processing'])
        
        output_folder = self.output_path.get()
        if not os.path.exists(output_folder):
            try:
                os.makedirs(output_folder)
            except Exception as e:
                messagebox.showerror("Error", f"{self.translations[self.current_language.get()]['error_create_folder']}: {e}")
                self.start_btn.config(state="normal", text=self.translations[self.current_language.get()]['start_process'])
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
                self.root.after(0, lambda: self.start_btn.config(state="normal", text=self.translations[self.current_language.get()]['start_process']))
        
        # Finalizar - status_label eliminada
        # self.root.after(0, lambda: self.status_label.config(text="¡Proceso completado!"))
        self.root.after(0, lambda: self.start_btn.config(state="normal", text=self.translations[self.current_language.get()]['start_process']))
        self.root.after(0, lambda: messagebox.showinfo(self.translations[self.current_language.get()]['completed'], self.translations[self.current_language.get()]['process_completed'].format(count=total_files)))
    
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
