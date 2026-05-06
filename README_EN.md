# PDF Image Extractor

A multilingual desktop application for extracting images from PDF files with support for Spanish and English languages.

## Features

- **Drag & Drop Support**: Simply drag PDF files into the application or click to browse
- **Batch Processing**: Process multiple PDF files at once
- **Image Format Selection**: Choose between PNG and JPG output formats
- **Multilingual Interface**: Switch between English and Spanish
- **Progress Tracking**: Visual progress bar during extraction
- **Automatic Folder Creation**: Creates subfolders for each PDF file
- **Fallback Option**: If no images are found, converts PDF pages to images

## Requirements

### Python Dependencies
Install the required packages using:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install PyMuPDF Pillow tkinterdnd2
```

### System Requirements
- Python 3.7 or higher
- Windows, macOS, or Linux
- Tkinter (usually included with Python)

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install PyMuPDF Pillow tkinterdnd2
   ```
3. Run the application:
   ```bash
   python pdf_image_extractor.py
   ```

## How to Use

### Step 1: Select Language
- At the top of the application, choose between **English** or **Spanish**
- The interface will update immediately to your selected language

### Step 2: Add PDF Files
- **Drag & Drop**: Drag PDF files directly onto the drop area
- **Browse Files**: Click "Select Files" to choose individual PDF files
- **Browse Folder**: Click "Select Folder" to add all PDFs from a directory

### Step 3: Configure Output
- **Output Folder**: Click "Select Folder" to choose where images will be saved
- **Image Format**: Choose between PNG or JPG format
- Default output folder is your Downloads folder

### Step 4: Start Extraction
- Click "START EXTRACTION PROCESS" to begin
- The progress bar shows extraction status
- Each PDF creates its own subfolder with extracted images

## Output Structure

```
Output Folder/
├── PDF_File_1/
│   ├── 1.png (or 1.jpg)
│   ├── 2.png (or 2.jpg)
│   └── ...
├── PDF_File_2/
│   ├── 1.png (or 1.jpg)
│   └── ...
└── ...
```

## How It Works

### Image Extraction Process
1. **Direct Image Extraction**: The application first tries to extract embedded images from the PDF
2. **Page Rendering**: If no images are found, it renders each PDF page as an image
3. **Quality Optimization**: Pages are rendered at 2x resolution for better quality

### Technical Details
- Uses **PyMuPDF (fitz)** for PDF processing
- **Pillow** for image manipulation
- **tkinterdnd2** for drag & drop functionality
- Multithreaded processing to prevent UI freezing

## File Formats

### Supported Input
- PDF files (.pdf)

### Supported Output
- PNG: Lossless compression, better for graphics
- JPG: Lossy compression, better for photos

## Troubleshooting

### Common Issues

**Q: The application won't start**
- Ensure Python 3.7+ is installed
- Install all required dependencies
- Check if tkinter is available (usually included with Python)

**Q: Drag & Drop isn't working**
- Make sure tkinterdnd2 is installed
- Try using the "Select Files" button instead

**Q: No images are extracted**
- The PDF might not contain embedded images
- The app will automatically convert pages to images as a fallback

**Q: Progress bar isn't moving**
- Large PDF files may take time to process
- Check if the application is responsive

### Error Messages
- **"Please select at least one PDF file"**: Add PDF files before starting
- **"Please select an output folder"**: Choose where to save the images
- **"Cannot create output folder"**: Check folder permissions

## Creating an Executable

To create a standalone executable:

### Method 1: Using build_exe.py
```bash
python build_exe.py
```

### Method 2: Using build.bat (Windows)
```bash
build.bat
```

### Method 3: Manual PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "tkinterdnd2;tkinterdnd2" pdf_image_extractor.py
```

The executable will be created in the `dist` folder.

## Keyboard Shortcuts

- **Ctrl+O**: Open file dialog (when clicking on drop area)
- **Escape**: Cancel file dialog

## Performance Tips

- For large PDF files, the extraction process may take several minutes
- PNG files are larger but higher quality than JPG
- Processing multiple files sequentially prevents memory issues

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify PDF files are not corrupted

## License

This project is open source. Check the license file for details.

## Version History

- **v1.0**: Initial release with basic PDF image extraction
- **v1.1**: Added multilingual support (English/Spanish)
- **v1.2**: Improved UI with centered language selection
- **v1.3**: Enhanced error handling and progress tracking
