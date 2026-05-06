# Extractor de Imágenes de PDF

Una aplicación de escritorio multilingüe para extraer imágenes de archivos PDF con soporte para idiomas español e inglés.

## Características

- **Soporte Arrastrar y Soltar**: Simplemente arrastra archivos PDF a la aplicación o haz clic para explorar
- **Procesamiento por Lotes**: Procesa múltiples archivos PDF a la vez
- **Selección de Formato de Imagen**: Elige entre formatos de salida PNG y JPG
- **Interfaz Multilingüe**: Cambia entre inglés y español
- **Seguimiento de Progreso**: Barra de progreso visual durante la extracción
- **Creación Automática de Carpetas**: Crea subcarpetas para cada archivo PDF
- **Opción de Respaldo**: Si no se encuentran imágenes, convierte las páginas del PDF en imágenes

## Requisitos

### Dependencias de Python
Instala los paquetes requeridos usando:
```bash
pip install -r requirements.txt
```

O instala manualmente:
```bash
pip install PyMuPDF Pillow tkinterdnd2
```

### Requisitos del Sistema
- Python 3.7 o superior
- Windows, macOS o Linux
- Tkinter (usualmente incluido con Python)

## Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias requeridas:
   ```bash
   pip install PyMuPDF Pillow tkinterdnd2
   ```
3. Ejecuta la aplicación:
   ```bash
   python pdf_image_extractor.py
   ```

## Cómo Usar

### Paso 1: Seleccionar Idioma
- En la parte superior de la aplicación, elige entre **Inglés** o **Español**
- La interfaz se actualizará inmediatamente al idioma seleccionado

### Paso 2: Agregar Archivos PDF
- **Arrastrar y Soltar**: Arrastra archivos PDF directamente al área designada
- **Explorar Archivos**: Haz clic en "Seleccionar Archivos" para elegir archivos PDF individuales
- **Explorar Carpeta**: Haz clic en "Seleccionar Carpeta" para agregar todos los PDFs de un directorio

### Paso 3: Configurar Salida
- **Carpeta de Salida**: Haz clic en "Seleccionar Carpeta" para elegir dónde se guardarán las imágenes
- **Formato de Imagen**: Elige entre formato PNG o JPG
- La carpeta de salida predeterminada es tu carpeta de Descargas

### Paso 4: Iniciar Extracción
- Haz clic en "INICIAR PROCESO DE EXTRACCIÓN" para comenzar
- La barra de progreso muestra el estado de la extracción
- Cada PDF crea su propia subcarpeta con las imágenes extraídas

## Estructura de Salida

```
Carpeta de Salida/
├── Archivo_PDF_1/
│   ├── 1.png (o 1.jpg)
│   ├── 2.png (o 2.jpg)
│   └── ...
├── Archivo_PDF_2/
│   ├── 1.png (o 1.jpg)
│   └── ...
└── ...
```

## Cómo Funciona

### Proceso de Extracción de Imágenes
1. **Extracción Directa de Imágenes**: La aplicación primero intenta extraer imágenes incrustadas del PDF
2. **Renderizado de Páginas**: Si no se encuentran imágenes, renderiza cada página del PDF como una imagen
3. **Optimización de Calidad**: Las páginas se renderizan a 2x resolución para mejor calidad

### Detalles Técnicos
- Usa **PyMuPDF (fitz)** para procesamiento de PDF
- **Pillow** para manipulación de imágenes
- **tkinterdnd2** para funcionalidad de arrastrar y soltar
- Procesamiento multihilo para evitar congelación de la interfaz

## Formatos de Archivo

### Entrada Soportada
- Archivos PDF (.pdf)

### Salida Soportada
- PNG: Compresión sin pérdida, mejor para gráficos
- JPG: Compresión con pérdida, mejor para fotos

## Solución de Problemas

### Problemas Comunes

**P: La aplicación no inicia**
- Asegúrate de tener Python 3.7+ instalado
- Instala todas las dependencias requeridas
- Verifica si tkinter está disponible (usualmente incluido con Python)

**P: Arrastrar y Soltar no funciona**
- Asegúrate de que tkinterdnd2 esté instalado
- Intenta usar el botón "Seleccionar Archivos" en su lugar

**P: No se extraen imágenes**
- El PDF podría no contener imágenes incrustadas
- La aplicación convertirá automáticamente las páginas en imágenes como alternativa

**P: La barra de progreso no se mueve**
- Los archivos PDF grandes pueden tardar tiempo en procesarse
- Verifica si la aplicación responde

### Mensajes de Error
- **"Por favor selecciona al menos un archivo PDF"**: Agrega archivos PDF antes de iniciar
- **"Por favor selecciona una carpeta de salida"**: Elige dónde guardar las imágenes
- **"No se puede crear la carpeta de salida"**: Verifica los permisos de la carpeta

## Crear un Ejecutable

Para crear un ejecutable independiente:

### Método 1: Usando build_exe.py
```bash
python build_exe.py
```

### Método 2: Usando build.bat (Windows)
```bash
build.bat
```

### Método 3: PyInstaller Manual
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "tkinterdnd2;tkinterdnd2" pdf_image_extractor.py
```

El ejecutable se creará en la carpeta `dist`.

## Atajos de Teclado

- **Ctrl+O**: Abrir diálogo de archivos (al hacer clic en el área de soltar)
- **Escape**: Cancelar diálogo de archivos

## Consejos de Rendimiento

- Para archivos PDF grandes, el proceso de extracción puede tardar varios minutos
- Los archivos PNG son más grandes pero de mayor calidad que los JPG
- El procesamiento secuencial de múltiples archivos previene problemas de memoria

## Soporte

Si encuentras algún problema:
1. Revisa la sección de solución de problemas arriba
2. Asegúrate de que todas las dependencias estén correctamente instaladas
3. Verifica que los archivos PDF no estén corruptos

## Licencia

Este proyecto es código abierto. Revisa el archivo de licencia para detalles.

## Historial de Versiones

- **v1.0**: Lanzamiento inicial con extracción básica de imágenes de PDF
- **v1.1**: Agregado soporte multilingüe (inglés/español)
- **v1.2**: Mejora de la interfaz con selector de idioma centrado
- **v1.3**: Manejo mejorado de errores y seguimiento de progreso

## Guía Rápida

### Para Principiantes
1. **Instalar Python**: Descarga e instala Python desde python.org
2. **Instalar Dependencias**: Ejecuta `pip install PyMuPDF Pillow tkinterdnd2`
3. **Ejecutar Aplicación**: Haz doble clic en `pdf_image_extractor.py`
4. **Seleccionar Idioma**: Elige tu idioma preferido en la parte superior
5. **Agregar PDFs**: Arrastra archivos PDF o haz clic para seleccionarlos
6. **Iniciar Extracción**: Haz clic en el botón azul grande para empezar

### Consejos de Uso
- **Organización**: Cada PDF crea su propia carpeta con las imágenes
- **Calidad**: Usa PNG para gráficos, JPG para fotos
- **Velocidad**: El procesamiento depende del tamaño y número de páginas del PDF
- **Espacio**: Asegúrate de tener suficiente espacio en disco para las imágenes extraídas
