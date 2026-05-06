#!/usr/bin/env python3
"""
Script alternativo para generar el EXE con manejo de errores mejorado
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Error: Se requiere Python 3.8 o superior")
        return False
    return True

def install_package(package_name, import_name=None):
    """Instala un paquete individualmente"""
    if import_name is None:
        import_name = package_name.lower()
    
    try:
        __import__(import_name)
        print(f"✓ {package_name} ya está instalado")
        return True
    except ImportError:
        print(f"Instalando {package_name}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                package_name, "--no-cache-dir", "--upgrade"
            ])
            print(f"✓ {package_name} instalado correctamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Error instalando {package_name}: {e}")
            return False

def install_dependencies():
    """Instala todas las dependencias necesarias"""
    print("=== Instalando dependencias ===\n")
    
    packages = [
        ("PyMuPDF", "fitz"),
        ("Pillow", "PIL"),
        ("tkinterdnd2", "tkinterdnd2"),
        ("PyInstaller", "PyInstaller")
    ]
    
    all_installed = True
    for package_name, import_name in packages:
        if not install_package(package_name, import_name):
            all_installed = False
    
    return all_installed

def create_spec_file():
    """Crea el archivo .spec personalizado"""
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['pdf_image_extractor.py'],
    pathex=[r'{os.getcwd()}'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinterdnd2',
        'tkinterdnd2.tkdnd',
        'PIL._tkinter_finder',
        'PIL.ImageTk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF Image Extractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('pdf_image_extractor.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✓ Archivo .spec creado correctamente")

def build_exe():
    """Construye el archivo EXE"""
    print("\n=== Construyendo archivo EXE ===")
    
    # Limpiar construcciones anteriores
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✓ Carpeta {folder} limpiada")
    
    # Ejecutar PyInstaller
    try:
        print("Iniciando PyInstaller...")
        subprocess.check_call([
            sys.executable, 
            '-m', 
            'PyInstaller', 
            '--clean',
            '--noconfirm',
            'pdf_image_extractor.spec'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✓ Construcción completada!")
        
        # Verificar el archivo
        exe_path = os.path.join('dist', 'PDF Image Extractor.exe')
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"✓ Archivo EXE generado: {exe_path}")
            print(f"✓ Tamaño: {size_mb:.2f} MB")
            return True
        else:
            print("✗ Error: No se encontró el archivo EXE")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Error durante la construcción: {e}")
        print("Intentando con configuración alternativa...")
        
        # Intentar con configuración más simple
        try:
            subprocess.check_call([
                sys.executable, 
                '-m', 
                'PyInstaller', 
                '--onefile',
                '--windowed',
                '--name=PDF Image Extractor',
                'pdf_image_extractor.py'
            ])
            
            exe_path = os.path.join('dist', 'PDF Image Extractor.exe')
            if os.path.exists(exe_path):
                print("✓ Construcción alternativa completada!")
                return True
        except:
            pass
        
        return False

def main():
    """Función principal"""
    print("=== Generador de EXE para PDF Image Extractor ===\n")
    
    # Verificar Python
    if not check_python_version():
        input("Presiona Enter para salir...")
        return
    
    # Verificar archivo principal
    if not os.path.exists('pdf_image_extractor.py'):
        print("✗ Error: No se encuentra pdf_image_extractor.py")
        print("Por favor ejecuta este script desde la misma carpeta")
        input("Presiona Enter para salir...")
        return
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n✗ Error: No se pudieron instalar todas las dependencias")
        input("Presiona Enter para salir...")
        return
    
    # Crear archivo .spec
    create_spec_file()
    
    # Construir EXE
    if build_exe():
        print("\n=== ¡ÉXITO! ===")
        print("El archivo EXE está listo en la carpeta 'dist'")
        print("Puedes copiarlo a cualquier computadora con Windows")
    else:
        print("\n=== ERROR ===")
        print("No se pudo generar el archivo EXE")
        print("Intenta ejecutar install_fix.bat primero")
    
    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
